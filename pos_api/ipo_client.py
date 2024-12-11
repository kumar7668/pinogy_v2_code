import base64
import hashlib
import hmac
import json
import time
import types
from urllib.parse import quote

import requests
from django.conf import settings

from .models import PoApiSession
from pinogy_app.middleware import get_user_ip


class IPOClient(object):
    def __init__(self, app_id="3"):
        self.host = getattr(settings, "PINOGY_API_HOST", "")
        self.access_key = getattr(settings, "PINOGY_ACCESS_KEY", "")
        self.secret_key = getattr(settings, "PINOGY_SECRET_KEY", "")
        self.token = self.get_token_from_db() or ""
        self.password = getattr(settings, "PINOGY_API_PASS", "")
        self.app_id = app_id
    
    def get_token_from_db(self):
        return PoApiSession.get_solo().token

    def add_token_in_db(self, token):
        obj = PoApiSession.get_solo()
        obj.token = token
        obj.save()

    def utctimestamp(self):
        """Create a UTC timestamp string.
        The timestamp is used to generate the signature and is passed with each
        API request as part of the access/secret key protocol.
        """
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def signature(self, resource_url, timestamp):
        """Create a signature string using the requested URL, timestamp, and
        secret key.
        A new signature is created and passed with each API request to verify
        the authenticity/validity of that request.
        """
        values = "".join([resource_url, timestamp])
        return base64.b64encode(
            hmac.new(self.secret_key.encode(), values.encode(), hashlib.sha256).digest()
        ).decode()

    def __getattr__(self, http_method):
        """Perform an API request and return a response object. `http_method` is
        looked up on the 'requests' module object and must be one of 'get',
        'post', 'put', or 'delete'.
        Parameters to a request may be passed as keyword arguments to this
        method.
        The output of a request can also be displayed in a web browser by
        passing show=True. To aid in reading JSON output in a browser, a browser
        plugin such as JSONView should be installed. More information at ...
        (https://addons.mozilla.org/en-us/firefox/addon/jsonview/
        Examples:
        >>> r = c.get("/apps/any/test")
        >>> r = c.get("/apps/any/test", show=True)
        >>> r = c.post("/apps/any/sessions", password="12345", show=True)
        """

        httpf = getattr(requests, http_method)

        def make_json_type(r):
            # if type(r.json) is types.MethodType:
            if isinstance(r.json, types.MethodType):
                # New versions of requests use a json() method. Preserve
                # backward compatibility.
                #
                # Do not call json() if Content-Type says
                # otherwise.
                r.json = (
                    r.json()
                    if "application/json" in r.headers["Content-Type"]
                    else None
                )
            return r

        def http_call(url, show=False, force_json=False, **args):
            ts = self.utctimestamp()
            islogin = args.pop("islogin", None)  # noqa
            args.update(
                accesskey=self.access_key,
                timestamp=ts,
                signature=self.signature(quote(url), ts),
                session=self.token,
                http_x_client_ip=get_user_ip()
            )

            # "params" (for GET requests - attaches arguments to the URL itself) and
            # "data" (for all other requests - passes arguments in the request body)
            # may not be used in the same request. Only one argument format may be used
            # per request.
            if force_json:
                method_args = dict(json=args)
            elif http_method.lower() in ["get", "delete"]:
                method_args = dict(params=args)
            else:
                method_args = dict(data=args)

                # for nested dicts/lists convert data arg to json
                if isinstance(args, dict):
                    for item in args.values():
                        if isinstance(item, (dict, list, tuple)):
                            method_args = dict(data=json.dumps(args))
            """
            if not url.startswith(self.host):
                r = httpf(self.host + quote(url), **method_args)
            else:
                r = httpf(url, **method_args)
            """

            r = httpf(self.host + quote(url), **method_args)
            r = make_json_type(r)
            if r.json and "token" in r.json:
                # Set the login session token
                self.token = r.json["token"]
                self.add_token_in_db(r.json["token"])

            if r.status_code != 200:
                error_code = r.json.get("error", None) if r.json else None

                if error_code in ["ERR_DATABASE_INTEGRITY_ERROR", "ERR_ACCESS_DENIED"]:
                    self.token = ""
                    self.add_token_in_db("")
                    relogin_result = self.relogin()
                    if relogin_result:
                        if "params" in method_args:
                            method_args["params"]["session"] = self.get_token_from_db()
                        else:
                            if not isinstance(method_args.get("data"), dict):
                                method_args["data"] = json.loads(
                                    method_args.get("data")
                                )
                                method_args["data"]["session"] = self.get_token_from_db()
                                method_args = dict(data=json.dumps(method_args["data"]))
                            else:
                                method_args["data"]["session"] = self.get_token_from_db()

                        r = httpf(self.host + quote(url), **method_args)
                        r = make_json_type(r)
            if show:
                self.show(r.text)
            return r

        return http_call

    def login(self, show=False):
        return self.post(
            "/apps/any/sessions",
            password=self.password,
            show=show,
            app_id=self.app_id,
            islogin=True,
        )

    def login_lmp_user(self, username, password, show=False):
        return self.post(
            "/apps/any/sessions",
            username=username,
            web_password=password,
            show=show,
            app_id=self.app_id,
            islogin=True,
        )

    def logout(self, show=False):
        r = self.delete("/apps/any/sessions/mine", show=show)
        self.token = ""
        return r

    # =======================================================================
    #    Retrieving data from Pinogy REST API
    # =======================================================================

    def relogin(self):
        # Makes five login attempts. In case of successful login, updates
        # the token in the object and in the database and returns True
        # Returns False in case of failure
        for i in range(1, 6):
            print(i, "ReLogin")
            result_login = self.login()
            if result_login.status_code == 200:
                token = result_login.json.get("token", None)
                if token:
                    self.token = token
                    self.add_token_in_db(token)
                    return True
                else:
                    return False
        return False

    def sync(self, sync_config):
        result = {}

        for resource, config in sync_config.items():
            result[resource] = self.sync_resource(config["tree"], config["url"])

        return result

    def sync_resource(self, config, url):
        result = []

        items = self.receive(url)

        for item in items:
            if "href" in item:
                item = self.receive(item["href"], False)

            result.append(item)

            for resource, resource_config in config.items():
                href = item.get("collections", {}).get(resource, None)

                if href:
                    item[resource] = self.sync_resource(resource_config, href)
                else:
                    item[resource] = []

        return result

    def receive(self, url, objects=True):
        url = url.replace(settings.PINOGY_API_HOST, "")

        result = self.get(url).json

        if objects:
            return result["objects"]
        else:
            return result
