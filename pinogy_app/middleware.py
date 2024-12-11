from django.http import HttpResponsePermanentRedirect
from urllib.parse import urlparse, urlunparse
import threading

user_ip_storage = threading.local()

class UserIPMiddleware:
    """
    Middleware that extracts the user's IP address and stores it in thread-local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = self.get_client_ip(request)

        # Store the IP in thread-local storage
        user_ip_storage.ip = user_ip
        response = self.get_response(request)
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
def get_user_ip():
    return getattr(user_ip_storage, 'ip', None)

class LowercaseURLMiddleware:
    """ 
    Middleware for converting uppercase URL slug to lowercase, redirecting only on 404 or 400 responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        EXEMPT_PATHS = ('/admin/', '/static/', '/media/')
        
        original_path = request.get_full_path()
        parsed_url = urlparse(original_path)

        # Skip exempted paths
        if parsed_url.path.startswith(EXEMPT_PATHS):
            return self.get_response(request)

        response = self.get_response(request)

        # Redirect only for 404 or 400 responses
        if response.status_code in {404, 400, 403, 500}:
            lowercased_path = parsed_url._replace(path=parsed_url.path.lower())
            lowercased_url = urlunparse(lowercased_path)

            # Redirect only if the path is different
            if original_path != lowercased_url:
                return HttpResponsePermanentRedirect(lowercased_url)

        return response