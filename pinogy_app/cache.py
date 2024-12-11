from django.core.cache.backends.redis import RedisCache

class RedisCache(RedisCache):

    def validate_key(self, key):
        pass
