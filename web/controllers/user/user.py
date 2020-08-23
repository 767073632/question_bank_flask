import json

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, g

from application import app, db
from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    resp_suc = {'code': 200, 'msg': '登录成功', "data": {}}
    resp_err = {'code': -1, 'msg': '请输入正确的用户名和密码', "data": {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        return jsonify(resp_err)

    if login_pwd is None or len(login_pwd) < 1:
        return jsonify(resp_err)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        return jsonify(resp_err)

    if user_info.login_pwd != UserService.gene_pwd(pwd=login_pwd,salt=user_info.login_salt):
        return jsonify(resp_err)

    response = make_response(json.dumps(resp_suc))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.gene_auth_code(user_info),user_info.uid))

    return response

@route_user.route('/logout')
def logout():
    response = make_response( redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response

@route_user.route( "/edit" ,methods=["POST","GET"])
def edit():
    if request.method == 'GET':
        return ops_render("user/edit.html")

    resp= {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code']=-1
        resp['msg']='请输入正确的用户名'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code']=-1
        resp['msg']='请输入正确的邮箱'
        return jsonify(resp)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)

@route_user.route( "/reset-pwd",methods=['POST',"GET"])
def resetPwd():
    if request.method=='GET':
        return ops_render( "user/reset_pwd.html" )

    resp= {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resp['code']=-1
        resp['msg']='请输入正确的原密码'
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code']=-1
        resp['msg']='请输入不少于6位的新密码'
        return jsonify(resp)

    if old_password ==new_password:
        resp['code']=-1
        resp['msg']='新密码不能等于旧密码'
        return jsonify(resp)

    user_info = g.current_user

    if user_info.login_pwd!=UserService.gene_pwd(old_password,user_info.login_salt):
        resp['code']=-1
        resp['msg']='请输入正确的原密码'
        return jsonify(resp)
    user_info.login_pwd = UserService.gene_pwd(new_password,user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s#%s"%(UserService.gene_auth_code(user_info),user_info.uid))
    return response


