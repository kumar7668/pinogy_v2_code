import json
import base64
import asyncio
import concurrent.futures
import django.http
import logging

from django.core.cache import cache

from typing import Optional

from pos_api import utils
from pos_api.exception import ApiException, ApiException401
from pos_api.ipo_client import IPOClient

loop = asyncio.get_event_loop()
pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
logger = logging.getLogger(__name__)

RESOURCE_CACHE_TIMEOUT = 60 * 60 * 24
POSTAL_REGION_CODE_CACHE_KEY = 'pos_api:pos_client:region_data:{country_id}'

class PWAPI(object):
    quippets_uri = "/queries/"

    def __init__(self):
        self.client = IPOClient()
        # a = self.client.login()
        if not self.client.token:
            self.client.add_token_in_db("WR40iUnjm+fxj3WZtQ/4XA/nEO67")

    def _return_json(self, http_response):
        """Return JSON from HTTP response, or raise an error."""
        r = http_response
        if r.status_code == 200:
            return r.json
        elif r.status_code == 401:
            raise ApiException401(r.status_code, r)
        elif r.status_code == 404:
            raise django.http.Http404("Page not found")
        elif r.status_code != 500:
            if isinstance(r.json, dict):
                error_data = dict(error=r.json)
            else:
                error_data = json.loads(r.json) if r.json is not None else {}

            # if error_data.get('error',{}).get('type') == 'token_refresh':
            #     self.token_refresh()
            raise ApiException(r.status_code, error_data)
        else:
            raise Exception("API error {0}: {1}".format(r.status_code, r.content))

    def __get_resource(self, resource_uri, data=None):
        data = self._preprocess(data) if data else {}
        r = self.client.get("/apps/pet_tracker" + resource_uri, timeout=3,**data)
        return self._return_json(r)

    def __post_resource(self, resource_uri, data=None):
        data = self._preprocess(data) if data else {}
        r = self.client.post("/apps/pet_tracker" + resource_uri, timeout=3, **data)
        return self._return_json(r)

    def _preprocess(self, data):
        res = {}
        for key, val in data.items():
            # filter empty fields
            if val is not None:
                res[key] = val

            if isinstance(val, dict):
                res[key] = self._preprocess(val)

        return res

    def post_queries(self, **kwargs):
        resource_uri = self.quippets_uri + kwargs.pop('quippet_name')
        return self.__post_resource(resource_uri, kwargs.get('quippet_params'))
    
    def cache_post_queries(self, **kwargs):
        resource_uri = self.quippets_uri + kwargs.pop("quippet_name")
        
        cache_key = "fetch_post_queries_{}_{}".format(
            resource_uri, kwargs.get("quippet_params")
        )
        cache_result = cache.get(cache_key)
        if cache_result:
            return cache_result
        else:
            result = self.__post_resource(resource_uri, kwargs.get("quippet_params"))
            cache.set(cache_key, result, 60 * 60)
            return result

    def get_queries(self, **kwargs):
        resource_uri = self.quippets_uri + kwargs.pop("quippet_name")
        return self.__get_resource(resource_uri, kwargs.get("quippet_params"))

    def get_file(self, pet_type_id):
        r = self.client.post(
            '/apps/pet_tracker/queries/read__tbl__vw_files_with_in_band_contents', timeout=3,
            qp_file_id=",".join(map(str, pet_type_id))
        )
        return self._return_json(r)

    def get_breeds(self, offset=0, **kwargs):
        resource_uri = '/api/pet_breeds'
        r = self.client.get(resource_uri, limit=1000, offset=offset, timeout=3, force_json=True, **kwargs)
        return self._return_json(r)

    def get_breed(self, slug):
        resource_uri = f'/api/pet_breeds/{slug}'
        r = self.client.get(resource_uri, timeout=3)
        return self._return_json(r)
    
    def get_pet_types(self):
        r = self.client.get("/api/pet_types", timeout=3)
        return self._return_json(r)

    def get_pets_status_list(self):
        r = self.client.get(
            "/api/pet_statuses",
            force_json=True,
            timeout=3
        )
        return json.loads(r.text)

    def get_locations(self):
        r = self.client.get("/api/locations", timeout=3)
        return self._return_json(r)

    def get_pets(self, **kwargs):
        resource_uri = "/pet_search"
        return self.__get_resource(resource_uri, kwargs.get("quippet_params"))

    def get_pet(self, pet_id, qp_public_call=True):
        quippet_params = utils.get_base_quippet_params()
        quippet_params["qp_public_call"] = qp_public_call
        quippet_params["qp_pet_id"] = pet_id

        r = self.get_pets(quippet_params=quippet_params)
        pet_list = r.get("pets", None)

        if not pet_list or len(pet_list) != 1:
            raise django.http.Http404("Page not found")        
        else:
            return pet_list[0]
    
    def get_pet_filters(self, **kwargs):
        if not kwargs:
            kwargs = {}

        r = self.client.get('/api/pet_filters', timeout=3, **kwargs)
        return self._return_json(r)

    def get_photos_meta(self, pet_id):
        r = self.client.get(f'/api/pets/{pet_id}/images', timeout=3)
        return self._return_json(r)
    
    def get_videos_meta(self, pet_id):
        r = self.client.get(f'/api/pets/{pet_id}/videos', timeout=3)
        return self._return_json(r)

    def get_similar_pets(self, **kwargs):
        resource_uri = f"/api/pet_breeds/{kwargs.pop('breed_slug')}/similar_pets"
        r = self.client.get(resource_uri, fields_include = ['litter'], timeout=3, **kwargs)
        return self._return_json(r)

    def get_available_pets(self, **kwargs):
        resource_uri = f"/api/pet_breeds/{kwargs.pop('breed_slug')}/available_pets"
        r = self.client.get(resource_uri, fields_include = ['litter'], **kwargs)
        return self._return_json(r)
    
    def get_pet_addons(self, pet_id):
        r = self.client.get('/api/pet_addons', 
            pet_id=pet_id,
            fields=["*", "product", "product.images", "variation", "variation.products", "variation.fields","variation.fields.values","product.child_trees", "product.child_trees.product", "product.product_prices", "variation.products.product_prices", "variation.products.images"],
            force_json=True,
            timeout=3,
        )
        return self._return_json(r)

    def get_txn(self, txn_id):
        r = self.client.get(
            "/api/v1/txns/{}".format(txn_id), timeout=3
        )
        return json.loads(r.text)

    def complete_summary(self, data):
        r = self.client.post(
            '/api/v1/txns', timeout=3,
            **data
        )
        return json.loads(r.text)

    def update_txn(self, txn_id, data):
        r = self.client.put(
            "/api/v1/txns/{}".format(txn_id),
            **data
        )
        return json.loads(r.text)

    def pay(self, transaction_id, token, expiry, cost, cardholder, method):
        path = '/api/v1/txns/{}/payments'.format(transaction_id)
        payment_response =  self._return_json(
            self.client.post(
                path,
                payments=[dict(
                    txnpay_amount=cost,
                    txnpay_payment_method_id=method,
                    txnpay_attrs=dict(cardconnect=dict(
                        token=token,
                        expiry=expiry,
                        cardholder=cardholder
                    )))]
            )
        )
        return payment_response
    
    def send_receipt(self, transaction_id, email):
        path = f"/api/v1/send_receipt/{transaction_id}"
        return self._return_json(self.client.post(path,email=email))

    def get_pet_data(self, pet_id):
        response = self.client.get('/api/pets/{}'.format(pet_id), timeout=3)
        return self._return_json(response)
    
    def get_brands_details(self):
        brands = self.client.get(
            '/api/mfg_brands',
            header={"content-type": "application/json"},
            fields=["id", "name", "images", "slug", ],
            order_by="name",
            force_json=True,
            limit=200,
            is_featured=True,
            timeout=3,
        )
        return self._return_json(brands)
    
    def get_brand_image(self, brand_id, brand_image_id):
        image = self.client.get(
            "/api/mfg_brands/{}/images/{}".format(brand_id, brand_image_id),
            include_contents=True, timeout=3
        )
        return self._return_json(image)
    
    def get_promotion_image(self, promotion_id, promotion_image_id):
        r = self.client.get(
            f'/api/promotions/{promotion_id}/images/{promotion_image_id}',
            include_contents=True, timeout=3
        )
        return self._return_json(r) 

    def get_promotions_list(self,kind:None):
        r = self.client.get(
            '/api/promotions',
            fields=["*", "images.*"],
            force_json=True,
            is_published=True,
            is_active_now=True,
            prom_is_mfd=False,
            is_temp=False,
            timeout=3,
            limit=1000,
            kinds=kind

        )
        return json.loads(r.text)

    def get_promotion_by_id(self, promotion_id):
            cache_key = 'promotion_details_{0}'.format(promotion_id)
            cache_result = cache.get(cache_key)
            if not cache_result:
                promotion = self._return_json(self.client.get(
                    '/api/promotions/{0}'.format(promotion_id),
                    header={"content-type": "application/json"},
                    fields=[
                        "*",
                        "images",
                        "videos",
                    ],
                    force_json=True,
                    timeout=3,
                ))
                cache.set(cache_key, promotion, 3600)
            else:
                promotion = cache_result
            return promotion

    def get_promotions_image_by_id(self,promotion_image_id, promotion_id):
        r = self.client.get(
            f'/api/promotions/{promotion_id}/images/{promotion_image_id}',
            include_contents=True
        )
        return self._return_json(r)

    def get_promotions_video_by_id(self, promotion_id, promotion_video_id):
        r = self.client.get(
            f'/api/promotions/{promotion_id}/videos/{promotion_video_id}',
            include_contents=True, timeout=3
        )
        return self._return_json(r)  

    def get_stores(self, is_public=True, is_enabled=True):
        r = self.client.get(
            '/api/stores',
            is_public=is_public,
            is_enabled=is_enabled, timeout=3
        )
        return self._return_json(r)

    def get_website_data(self, **kwargs):
        resource_uri = '/api/websites/mine'
        r = self.client.get(resource_uri, timeout=3, **kwargs)
        return self._return_json(r)
    
    def send_page_data(self, page_data):
        resource_uri = '/api/websites/mine'
        r = self.client.put(resource_uri, **page_data)
        return self._return_json(r)
    
    def get_integration_settings(self):
        r = self.client.get(
            '/apps/any/integration_settings', timeout=3
        )
        return self._return_json(r)

    def save_lead_conversations(self, data):
        def send_lead():
            file_loaded = None
            msg_data = {}
            data.pop('captcha', '')
            
            for item in list(data):
                if 'filer' in str(type(data[item])):
                    with open(data[item].path, 'rb') as f:
                        file_loaded = base64.b64encode(
                            f.read()).decode('utf-8')
                        file_name = data[item].name
                    data[item].delete()
                # 0 Not included because it removes sms_okay/email_me_more 
                # that is not valid for forms like pet etc 
                elif data[item] not in ['', None]:
                    msg_data[item] = data[item]

            resp = self.client.post(
                '/api/lead_conversations',
                data=msg_data,
            )

            if resp.status_code == 200 and file_loaded:
                file_msg = {"contents": str(
                    file_loaded), "description": " ", "filename": str(file_name)}
                resp = json.loads(resp.content)
                lead_conversations_id = resp['id']
                url = '/api/lead_conversations/{}/attachments'.format(
                    lead_conversations_id)
                api_result = self.client.post(
                    url,
                    file=file_msg
                )

        loop.run_in_executor(pool, send_lead)


    def consumer_validation(self, data):
        path = '/api/verifications'
        r =self.client.post(path,**data)
        return r

    def consumer_code_verifications(self,data,verification_id):
        path = '/api/verifications/{}'.format(verification_id)
        r =self.client.put(path,**data)
        return r
    
    
    def get_pet_type_image(self, pet_type_id: str):
        r = self.client.get("/api/pet_types/{}/images".format(pet_type_id), timeout=3)
        return self._return_json(r)


    def create_pet_box_visit(self, pet_id: int, start_at: str, finish_at: str, email: str, phone: str, shop_window: int, email_me_more: int, sms_okay: int, reservation: int, first_name: str, last_name:str, location_id: Optional[int] = None, notes: Optional[str] = None):
        r = self.client.post(
            '/api/pet_box_visits',
            lead_data=dict(
                email=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                shop_window=shop_window,
                sms_okay=sms_okay,
                email_me_more=email_me_more,
                reservation=reservation,
            ),
            pet_id=pet_id,
            start_at=start_at,
            finish_at=finish_at,
            visit_box_type_id=1,
            location_id=location_id,
            notes=notes
        )
        return self._return_json(r)


    def get_pet_box_visits_schedule(self, start_at, finish_at, location_id=None, visit_box_id=None):
        try:
            cache_key = "fetch_pet_box_visits_schedule_{}_{}_{}_{}".format(start_at, finish_at, location_id, visit_box_id)
            cache_result = cache.get(cache_key)
            if cache_result:
                return cache_result
            else:
                r = self.client.get(
                    '/api/pet_box_visits_schedule',
                    start_at=start_at,
                    finish_at=finish_at,
                    location_id=location_id,
                    visit_box_id=visit_box_id, timeout=3
                )
                result = self._return_json(r)
                cache.set(cache_key, result, 60 * 60)
                return result
        except Exception as e:
             logger.error("An error occurred:", e)
             return {}

    def get_pet_types_adcard(self, pet_type_id):
        r = self.client.get('/api/pet_types/{}/adcard_media'.format(pet_type_id), timeout=3)
        if r.status_code==404:
                return []
        else:
            return self._return_json(r)
        
    def get_websites_setting(self,  integratio_setting_id : str):
        r = self.client.get("/api/websites/{}".format(integratio_setting_id),fields_include="pet_type_web_options")
        return self._return_json(r)
    
    def verify_unsubscribe_token(self, token):
        r = self.client.get("/api/unsubscribe_tokens/{}".format(token))
        return self._return_json(r)
    
    def Marketing_emails(self):
        r = self.client.get("/api/marketing_lists")
        return self._return_json(r)
    
    def unsubscribe_marketing_lists(self, data):
        token = data['token']
        r = self.client.put("/api/unsubscribe_tokens/{}".format(token),**data)
        return self._return_json(r)
    

    def subscribe_marketing_lists(self, data):
        token = data['token']
        r = self.client.put("/api/subscribe_tokens/{}".format(token),**data)
        return self._return_json(r)
    def get_postal_regions(self, country_id=231):
        cache_key = POSTAL_REGION_CODE_CACHE_KEY.format(country_id=country_id)
        result = cache.get(cache_key)
        if result is None:
            r = self.client.post(
                '/apps/any/queries/read__tbl__postal_regions',
                qp_prgn_country_id=country_id
            )
            result = json.loads(r.text)['objects']
            cache.set(cache_key, result, RESOURCE_CACHE_TIMEOUT)
        return result
