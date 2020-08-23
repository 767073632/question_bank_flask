



from application import app

"""
配置拦截器
"""
import web.interceptors.AuthInterceptor
import web.interceptors.ErrorInterceptor
import web.interceptors.ApiAuthInterceptor
"""
配置蓝图
"""
from web.controllers.account.Account import route_account
from web.controllers.finance.Finance import route_finance
from web.controllers.question.Question import route_question
from web.controllers.index import route_index
from web.controllers.member.Member import route_member
from web.controllers.stat.Stat import route_stat
from web.controllers.user.user import route_user
from web.controllers.api import route_api
from web.controllers.upload.Upload import route_upload

app.register_blueprint(route_index,url_prefix='/')
app.register_blueprint(route_user,url_prefix='/user')
app.register_blueprint(route_account,url_prefix='/account')
app.register_blueprint(route_finance,url_prefix='/finance')
app.register_blueprint(route_question,url_prefix='/question')
app.register_blueprint(route_member,url_prefix='/member')
app.register_blueprint(route_stat,url_prefix='/stat')
app.register_blueprint(route_api,url_prefix='/api')
app.register_blueprint(route_upload,url_prefix='/upload')