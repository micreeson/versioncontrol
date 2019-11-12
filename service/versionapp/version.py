from .redis import RedisClient

class ReturnObject:
    resultCode = ''
    version = ''
    releaseNote = ''
    message = ''
    releaseDate = ''

    def clear(self):
        self.resultCode = ''
        self.version = ''
        self.releaseNote = ''
        self.message = ''
        self.releaseDate = ''


class Version:
    retrun_obj = ReturnObject()
    redis_obj = RedisClient()

    def set_version(self, appid, version, note, date):
        self.retrun_obj.clear()
        self.save_app_version(appid, version)
        self.save_app_version_release_note(appid, note, version)
        self.save_app_version_date(appid, date, version)

        self.retrun_obj.resultCode = "OK"
        self.retrun_obj.version = self.read_latest_version(appid)
        self.retrun_obj.releaseNote = self.read_latest_note(appid)

    def save_app_version_release_note(self, appid, note, version):
        # 记录当前app的版本号的发布说明
        key = self.gen_release_note_key(appid, version)
        self.redis_obj.write(key, note)


    def save_app_version_date(self, appid, date, version):
        # 记录当前app的版本号的发布说明
        key = self.gen_release_date_key(appid, version)
        self.redis_obj.write(key, date)

    def save_app_version(self, appid, version):
        # 记录当前app的最新版本号
        key = self.gen_version_key(appid)
        self.redis_obj.write(key, version)

    #设置某个app的用户版本信息
    def save_user_version(self, appid, userid):
        key = self.gen_user_version_key(appid, userid)
        current_ver = self.read_latest_version(appid)
        self.redis_obj.write(key, current_ver)

    #获取某个app的用户的版本信息
    def get_user_version(self, appid, userid):
        key = self.gen_user_version_key(appid, userid)
        version = self.redis_obj.read(key)

        return version

    #根据appid和userid生成key，用来存放当前用户的版本号
    def gen_user_version_key(self, appid, userid):
        if appid is None or userid is None:
            return None

        return 'VERSIONCONTROL#' + appid + '#' + userid

    # 根据appid和version生成key，用来存放app的版本的发布信息
    def gen_release_note_key(self, appid, userid):
        if appid is None or userid is None:
            return None

        return 'VERSIONCONTROL#' + appid + '#' + userid + '#NOTE'

    # 根据appid生成key，用来存放app的版本号
    def gen_version_key(self, appid):
        if appid is None:
            return None

        return 'VERSIONCONTROL#' + appid

    #根据appid生成发布日期的保存key
    def gen_release_date_key(self, appid, version):
        if appid is None or version is None:
            return None

        return 'VERSIONCONTROL#' + appid + '#' + version + '#DATE'

    #获取app的最新版本号
    def read_latest_version(self, appid):
        key = self.gen_version_key(appid)
        return self.redis_obj.read(key)

    #获取app最新版本的发布说明
    def read_latest_note(self, appid):
        version = self.read_latest_version(appid)
        key = self.gen_release_note_key(appid, version)
        note = self.redis_obj.read(key)

        return note

    #获取app最新版本的发布日期
    def read_latest_date(self, appid):
        version = self.read_latest_version(appid)
        key = self.gen_release_date_key(appid, version)
        note = self.redis_obj.read(key)

        return note

    #获取指定用户的版本信息，判断用户是否已经获取版本信息，新用户返回版本号和发布说明，已经获取过的用户返回错误
    def get_version(self, appid, userid):
        self.retrun_obj.clear()
        #appid是否存在，不存在则返回错误
        latest_version = self.read_latest_version(appid)
        if latest_version is None:
            self.retrun_obj.resultCode = "False"
            self.retrun_obj.message = "Invalid appid"
            return False

        #用户是否已经获取过版本信息，如果没有获取过说明是新用户，需要返回版本号和发布说明，并保存已获取的状态
        #如果已经获取过版本信息，但与app最新的版本号不一致，也需要返回新版本的版本号和发布说明
        user_version = self.get_user_version(appid, userid)
        if user_version is None or user_version != latest_version:
            self.save_user_version(appid, userid)
            self.retrun_obj.resultCode = "False"
            self.retrun_obj.message = "Get new version"
            self.retrun_obj.version = self.read_latest_version(appid)
            self.retrun_obj.releaseNote = self.read_latest_note(appid)
            self.retrun_obj.releaseDate = self.read_latest_date(appid)
        else:
            self.retrun_obj.resultCode = "OK"
            self.retrun_obj.message = "Latest version"

    # 获取指定用户的版本信息，判断用户是否已经获取版本信息，新用户返回版本号和发布说明，已经获取过的用户返回错误
    def get_latest_version(self, appid):
        self.retrun_obj.clear()
        # appid是否存在，不存在则返回错误
        latest_version = self.read_latest_version(appid)
        if latest_version is None:
            self.retrun_obj.resultCode = "False"
            self.retrun_obj.message = "Invalid appid"
            return False

        self.retrun_obj.resultCode = "OK"
        self.retrun_obj.message = "Latest version"
        self.retrun_obj.version = self.read_latest_version(appid)
        self.retrun_obj.releaseNote = self.read_latest_note(appid)
        self.retrun_obj.releaseDate = self.read_latest_date(appid)

        return True

