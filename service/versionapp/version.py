from .redis import RedisClient

class Version:
    resultCode = ''
    message = ''
    def set_version(self, appid, version):
        redis_obj = RedisClient()
        redis_obj.write(appid, version, 60*60)

        self.resultCode = "OK"
        self.message = redis_obj.read(appid)

    def get_version(self, appid, version, userid):
        redis_obj = RedisClient()
        redis_obj.read(appid, version, userid)

