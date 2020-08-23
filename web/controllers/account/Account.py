import math

from flask import Blueprint, render_template, request, redirect, jsonify
from sqlalchemy import or_

from application import app, db
from common.libs.Helper import ops_render, iPagination, get_current_time
from common.libs.user.UserService import UserService
from common.models.User import User

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    query = User.query
    req = request.values
    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike(f"%{req['mix_kw']}%"),User.mobile.ilike(f"%{req['mix_kw']}%"))
        query =query.filter(rule)

    if 'status' in req and int(req['status']) >-1:
        query = query.filter(User.status==req['status'])
    page = request.values.get('p', '')
    total_pages = int(math.ceil(query.count() / app.config['PAGE_SIZE']))
    page = int(page) if page.isdigit() and int(page) > 0 and int(page) <= total_pages else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace(f'&p={page}','')
    }

    pages = iPagination(page_params)

    offset = (page - 1) * app.config['PAGE_SIZE']
    end = page * app.config['PAGE_SIZE']
    user_list = query.order_by(User.uid.desc()).all()[offset:end]

    resp_data['user_list'] = user_list
    resp_data['pages'] = pages
    resp_data['search_content'] = req.get('mix_kw','')
    return ops_render('account/index.html', resp_data)


@route_account.route("/info")
def info():
    resp_data = {}
    val = request.values
    uid = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
    if uid < 1:
        return redirect('/account/index')
    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect('/account/index')
    resp_data['info'] = info
    return ops_render('account/info.html', resp_data)


@route_account.route("/set", methods=['GET', 'POST'])
def set():
    if request.method == 'GET':
        val = request.values
        uid = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
        info = User.query.filter_by(uid=uid).first()
        resp_data = {}
        if info:
            resp_data['info'] = info
        else:
            resp_data['info'] = None

        return ops_render('account/set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    uid = int(req['id']) if req.get('id', '') and req.get('id', '').isdigit() else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入2位以上的用户名'
        return jsonify(resp)

    if mobile is None or len(mobile) < 11:
        resp['code'] = -1
        resp['msg'] = '请输入不少于11位的电话'
        return jsonify(resp)

    if login_name is None or len(nickname) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入2位以上的登录名'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入6位以上的密码'
        return jsonify(resp)

    if email is None or len(email) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入正确的邮箱'
        return jsonify(resp)

    user_info = User.query.filter(User.uid != uid,User.login_name == login_name).first()
    if user_info:
        app.logger.info(uid)
        app.logger.info(user_info)
        resp['code'] = -1
        resp['msg'] = '登录用户名已存在'
        return jsonify(resp)
    user_info = User.query.filter(User.uid == uid).first()
    if not user_info:
        user_info=User()
        user_info.created_time = get_current_time()
        user_info.login_salt = UserService.gene_salt()
    user_info.login_pwd = UserService.gene_pwd(login_pwd, user_info.login_salt)
    user_info.nickname = nickname
    user_info.login_name = login_name
    user_info.email = email
    user_info.mobile = mobile
    user_info.updated_time = get_current_time()
    db.session.add(user_info)
    db.session.commit()
    return resp

@route_account.route('/ops',methods=['POST'])
def ops():
    resp = {'code':200,'msg':'操作成功'}
    val = request.values
    uid = int(val['uid']) if val.get('uid', '') and val.get('uid', '').isdigit() else 0
    act = val.get('act','')
    if uid < 1:
        resp['code']=-1
        resp['msg']='操作失败'
        return jsonify(resp)
    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        resp['code']=-1
        resp['msg']='操作失败'
        return jsonify(resp)
    if act not in ['remove','recover']:
        resp['code']=-1
        resp['msg']='操作失败'
        return jsonify(resp)
    if act=='remove':
        user_info.status = 0
    if act=='recover':
        user_info.status = 1

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)