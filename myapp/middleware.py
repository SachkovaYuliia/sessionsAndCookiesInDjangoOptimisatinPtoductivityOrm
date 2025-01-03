from django.utils.cache import patch_cache_control
from django.middleware.cache import CacheMiddleware

class AnonymousCacheMiddleware(CacheMiddleware):
    def process_response(self, request, response):
        if not request.user.is_authenticated:
            patch_cache_control(response, public=True, max_age=60*15)
        return response
