from django.core.cache import cache

class RedisClient:
    def write(self, key, value):
        try:
            cache.set(key, value)
            cache.persist(key)
            print("key is:", key)
            print("value is:", value)

        except Exception as e:
            print(e)

    def read(self, key):
        try:
            ret = cache.get(key)
        except Exception as e:
            print(e)

        return ret