import re

from flask import request, redirect, g

from application import app
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']

    path = request.path
    pattern = re.compile('|'.join(ignore_check_login_urls))
    if pattern.match(path):
        return

    pattern = re.compile('|'.join(ignore_urls))
    if pattern.match(path):
        return

    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info#渲染变量

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))

    return

"""
判断用户是否已经登录
"""
def check_login():
    cookies = request.cookies
    auth_cookie = cookies.get(app.config['AUTH_COOKIE_NAME'],None)
    if auth_cookie is None:
        return False


    auth_info = auth_cookie.split("#")
    if len(auth_info) !=2:
        return False

    try:
        user_info = User.query.filter_by(uid = auth_info[1]).first()
    except Exception:
        return False

    if auth_info[0] != UserService.gene_auth_code(user_info):
        return False

    return user_info