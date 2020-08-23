DEBUG = True
SERVER_PORT = 9000
SQLALCHEMY_DATABASE_URI= 'mysql://root:wait20180808@127.0.0.1/mxweixin'
SQLALCHEMY_TRACK_MODIFICATIONS = False
AUTH_COOKIE_NAME = 'weixin_flask'
SQlALCHEMY_ECHO = True#打印所有sql语句
PAGE_SIZE = 50
PAGE_DISPLAY = 10
domain=''
#过滤url
IGNORE_URLS = [
    "^/user/login",
    '^/api'
]

API_INTERCEPT_URLS = {
    '^/api/question/question-random',
    '^/api/question/favourite',
    '^/api/question/note',
    '^/api/question/question-favorites',
    '^/api/question/question-notes',
    '^/api/question/question-history',
    '^/api/question/question-submit',
    '^/api/question/question-mistakes-collection',
}

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

MINA_APP = {
    'appid':'wx9da8c58ce9a91905',
    'appkey':'98ab675ba3891e4527e9ced86e94ebe6'
}

STATUS_MAPPING = {
    '1':'正常',
    '0':'删除'
}

UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/'
}
