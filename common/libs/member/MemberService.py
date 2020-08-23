# -*- coding: utf-8 -*-
import hashlib,requests,random,string,json
from application import  app
from common.models.member import Member


class MemberService():

    @staticmethod
    def geneAuthCode( member_info = None ):
        m = hashlib.md5()
        str = "%s-%s-%s" % ( member_info.id, member_info.salt,member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ( "".join( keylist ) )

    @staticmethod
    def getWeChatOpenId( code ):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid

    @staticmethod
    def check_member_login(auth_cookie):


        if auth_cookie is None:
            return False

        auth_info = auth_cookie.split("#")
        if len(auth_info) != 2:
            return False

        try:
            member_info = Member.query.filter_by(id=auth_info[1]).first()
        except Exception:
            return False

        if member_info is None:
            return False

        if auth_info[0] != MemberService.geneAuthCode(member_info):
            return False

        if member_info.status != 1:
            return False

        return member_info
