import base64
import hashlib
import string
import random


class UserService():

    @staticmethod
    def gene_auth_code(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()
    @staticmethod
    def gene_pwd(pwd,salt):
        m = hashlib.md5()
        str = "%s-%s"%(base64.encodebytes(pwd.encode('utf-8')),salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()
    @staticmethod
    def gene_salt():
        return "".join(random.choices(string.ascii_letters+string.digits,k=16))
