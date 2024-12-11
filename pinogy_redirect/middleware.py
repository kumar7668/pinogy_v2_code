from django import http
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from .utils import log_404
from .models import Redirect, RedirectApplication

class Redirect404Middleware(MiddlewareMixin):

    def handle_404(self, request, response):
        path = request.get_full_path()
        redirect_url = None

        # Define a list of paths to exclude from redirection
        excluded_paths = [
            '/static/',
            '/media/',
            '.webp',
            '.jpg',
            '.png',
            '.css',
            '.js',
        ]
        # Check if the path should be excluded from redirection
        if any(prefix in path for prefix in excluded_paths):
            return response  # Skip redirection for excluded paths
        
        # check in Redirect Model if redirection is available or not 
        # for requested and Removing trailing slash paths ( if available )
        check_paths = [
            path,
        ]
        if path.endswith('/'):
            # remove trailing slash if query parameters are not available
            check_paths.append(path.rstrip('/'))
        elif '/?' in path:
            # remove trailing slash if queryoarameters availble, also add queryparameter back
            check_paths.append(path[:path.rfind('/')]+path[path.rfind('/')+1:])

        redirects = Redirect.objects.filter(site__id__exact=settings.SITE_ID, old_path__in=check_paths)

        if redirects.exists():
            redirect_url = redirects.first()
        else:
            app_hook = RedirectApplication.objects.get_redirected_path(old_path=path)
            if app_hook:
                return http.HttpResponsePermanentRedirect(app_hook)

        # if redirect =_url found in db then redirect to that
        if redirect_url is not None:
            if redirect_url.new_path == '':
                return http.HttpResponseGone()
            return http.HttpResponsePermanentRedirect(redirect_url.new_path)

        # if path do not have language code but it prefx is enabled in setting then addcode to path 
        if path[0:4] != f'/{settings.LANGUAGE_CODE}/' and settings.PREFIX_DEFAULT_LANGUAGE:
            path = f'/{settings.LANGUAGE_CODE}' + path
            return HttpResponsePermanentRedirect(path)

        # if language code is available in path and prefix is off then remove from url 
        if path.startswith(f'/{settings.LANGUAGE_CODE}/') and not settings.PREFIX_DEFAULT_LANGUAGE:
            return http.HttpResponsePermanentRedirect(path.replace('/{}/'.format(settings.LANGUAGE_CODE),  '/'))

        # Save 404 path in DB
        log_404(path=path)

        # Return cusotm 404 page
        context = {
            "status_code": response.status_code,
            "message": "Page not found"
        }
        return render(request, 'pinogy_redirect/error_page.html', context, status=response.status_code)

    def process_response(self, request, response):

        if response.status_code == 404:
            return self.handle_404(request, response)

        if settings.DEBUG != True and response.status_code in [500, 403]:
            message = ''
            if response.status_code == 500:
                message = "Internal server error"
            elif response.status_code == 403:
                message = "Forbidden"

            context = {
                "status_code": response.status_code,
                "message": message
            }
            return render(request, 'pinogy_redirect/error_page.html', context, status=response.status_code)

        return response