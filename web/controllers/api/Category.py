from flask import request, jsonify

from common.libs.category.CategoryService import CategoryService
from common.models.CategoryQuestion import CategoryQuestion, Question
from web.controllers.api import route_api


@route_api.route("/category/type1",methods = [ "GET","POST" ])
def type1():
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    category_1=CategoryQuestion.query.filter(CategoryQuestion.category_type==1)
    resp['data']=CategoryService.get_json_type1(category_1)
    return jsonify( resp )


@route_api.route("/category/type23",methods = [ "GET","POST" ])
def type23():
    req = request.values
    type1_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    category_2=CategoryQuestion.query.filter(CategoryQuestion.parent_category_id==type1_id)
    if not category_2:
        resp['msg']='不存在子目录'
        return resp
    resp['data']=CategoryService.get_json_type23(category_2)
    return jsonify( resp )
