# -*- coding: utf-8 -*-
import math

import xlrd as xlrd
from flask import Blueprint, request, jsonify

from application import app, db
from common.libs.Helper import ops_render, iPagination, get_current_time
from common.libs.question.QuestionService import QuestionService
from common.models.CategoryQuestion import CategoryQuestion,Question

route_question = Blueprint('question_page', __name__)
"""
专业
"""


@route_question.route("/type1_index")
def type1_index():
    resp_data = {}
    query = CategoryQuestion.query.filter(CategoryQuestion.category_type == 1)
    req = request.values
    if 'mix_kw' in req:
        rule = CategoryQuestion.name.ilike(f"%{req['mix_kw']}%")
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(CategoryQuestion.status == req['status'])

    if 'search_type' in req and int(req['search_type']) > -1:
        query = query.filter(CategoryQuestion.type == int(req['search_type']))
    page = request.values.get('p', '')
    total_pages = int(math.ceil(query.count() / app.config['PAGE_SIZE']))
    page = int(page) if page.isdigit() and int(page) > 0 and int(page) <= total_pages else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace(f'&p={page}', '')
    }

    pages = iPagination(page_params)

    offset = (page - 1) * app.config['PAGE_SIZE']
    end = page * app.config['PAGE_SIZE']
    profession_list = query.order_by(CategoryQuestion.id.desc()).all()[offset:end]
    resp_data['profession_list'] = profession_list
    resp_data['pages'] = pages
    resp_data['search_content'] = req.get('mix_kw', '')
    resp_data['search_status'] = req.get('status', '')
    resp_data['search_type']=req.get('search_type','')
    return ops_render("question/type1_index.html", resp_data)


@route_question.route("/type1_info")
def type1_info():
    id = request.values.get('id', "0")
    if id.isdigit():
        id = int(id)
    info = CategoryQuestion.query.filter_by(id=id).first()
    resp_data = {}
    resp_data['info'] = info
    return ops_render("question/type1_info.html", resp_data)


@route_question.route("/type1_set", methods=['POST', 'GET'])
def type1_set():
    if request.method == 'GET':
        val = request.values
        id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
        info = CategoryQuestion.query.filter_by(id=id).first()
        resp_data = {}
        if info:
            resp_data['info'] = info
        else:
            resp_data['info'] = None

        return ops_render('question/type1_set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    print(req)
    id = int(req['id']) if req.get('id', '') and req.get('id', '').isdigit() else 0
    app.logger.info(id)
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else 0
    is_free = req['is_free'] if 'is_free' in req else 0
    is_hot = req['is_hot'] if 'is_hot' in req else 0
    type = req['type'] if 'type' in req else 1
    main_image = req['main_image'] if 'main_image' in req else''

    if name is None or len(name) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入2位以上的专业名称'
        return jsonify(resp)

    if price is None or not price.isdigit():
        resp['code'] = -1
        resp['msg'] = '价格需要纯数字'
        return jsonify(resp)

    category_info = CategoryQuestion.query.filter(CategoryQuestion.id != id, CategoryQuestion.name == name).first()
    if category_info:
        resp['code'] = -1
        resp['msg'] = '专业名已存在'
        return jsonify(resp)
    category_info = CategoryQuestion.query.filter(CategoryQuestion.id == id).first()
    if not category_info:
        category_info = CategoryQuestion()
        category_info.created_time = get_current_time()
    category_info.name = name
    category_info.type = int(type)
    category_info.category_type = 1
    category_info.is_hot = int(is_hot)
    category_info.is_free = int(is_free)
    category_info.price = price
    category_info.creat_time = get_current_time()
    category_info.main_image=main_image

    db.session.add(category_info)
    db.session.commit()
    return resp


@route_question.route('/type1_ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '操作成功'}
    val = request.values
    id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
    act = val.get('act', '')
    if id < 1:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    category_info = CategoryQuestion.query.filter_by(id=id).first()
    if not category_info:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act == 'remove':
        category_info.status = 0
    if act == 'recover':
        category_info.status = 1

    db.session.add(category_info)
    db.session.commit()
    return jsonify(resp)


"""
章节
"""


@route_question.route("/type2_index")
def type2_index():
    resp_data = {}
    req = request.values
    if req.get('parent_id', '1').isdigit():
        parent_id = int(req.get('parent_id', '1'))
    else:
        parent_id = 1
    query = CategoryQuestion.query.filter(CategoryQuestion.category_type == 2,
                                          CategoryQuestion.parent_category_id == parent_id)
    if 'mix_kw' in req:
        rule = CategoryQuestion.name.ilike(f"%{req['mix_kw']}%")
        query = query.filter(rule)

    if 'search_type' in req and int(req['search_type']) > -1:
        query = query.filter(CategoryQuestion.type == int(req['search_type']))
    page = request.values.get('p', '')
    total_pages = int(math.ceil(query.count() / app.config['PAGE_SIZE']))
    page = int(page) if page.isdigit() and int(page) > 0 and int(page) <= total_pages else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace(f'&p={page}', '')
    }

    pages = iPagination(page_params)

    offset = (page - 1) * app.config['PAGE_SIZE']
    end = page * app.config['PAGE_SIZE']
    profession_list = query.order_by(CategoryQuestion.name).all()[offset:end]
    resp_data['profession_list'] = profession_list
    resp_data['pages'] = pages
    resp_data['search_content'] = req.get('mix_kw', '')
    resp_data['parent_id'] = parent_id
    return ops_render("question/type2_index.html", resp_data)


@route_question.route("/type2_set", methods=['POST', 'GET'])
def type2_set():
    if request.method == 'GET':
        val = request.values
        id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
        parent_id = int(val['parent_id']) if val.get('parent_id', '') and val.get('parent_id', '').isdigit() else 1
        info = CategoryQuestion.query.filter_by(id=id).first()
        resp_data = {}
        if info:
            resp_data['info'] = info
            parent_id = info.parent_category_id
        else:
            resp_data['info'] = None
        resp_data['parent_id'] = parent_id
        return ops_render('question/type2_set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    id = int(req['id']) if req.get('id', '') and req.get('id', '').isdigit() else 0
    parent_id = int(req['parent_id']) if req.get('parent_id', '') and req.get('parent_id', '').isdigit() else 1
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else 0
    is_free = req['is_free'] if 'is_free' in req else 0
    is_hot = req['is_hot'] if 'is_hot' in req else 0
    if name is None or len(name) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入2位及以上的章节名称'
        return jsonify(resp)
    query = CategoryQuestion.query.filter(CategoryQuestion.parent_category_id == parent_id)

    category_info = query.filter(CategoryQuestion.id != id, CategoryQuestion.name == name).first()
    if category_info:
        resp['code'] = -1
        resp['msg'] = '章节名已存在'
        return jsonify(resp)

    category_info = query.filter(CategoryQuestion.id == id).first()
    if not category_info:
        category_info = CategoryQuestion()
        category_info.created_time = get_current_time()

    category_info.name = name
    category_info.category_type = 2
    category_info.is_hot = int(is_hot)
    category_info.is_free = int(is_free)
    category_info.price = price
    category_info.creat_time = get_current_time()
    category_info.parent_category_id = parent_id
    db.session.add(category_info)
    db.session.commit()
    return resp


@route_question.route('/type2_ops', methods=['POST'])
def type2_ops():
    resp = {'code': 200, 'msg': '操作成功'}
    val = request.values
    id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
    act = val.get('act', '')
    if id < 1:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    category_info = CategoryQuestion.query.filter_by(id=id).first()
    if not category_info:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act not in ['remove','recover','true_remove']:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act == 'remove':
        category_info.status = 0
    if act == 'recover':
        category_info.status = 1
    if act == 'true_remove':
        parent = category_info
        while parent.parent_category:
            parent.parent_category.count -= category_info.count
            db.session.add(parent.parent_category)
            parent=parent.parent_category

        db.session.execute(f'DELETE FROM category_question WHERE (id = {category_info.id})')

        db.session.commit()
        return jsonify(resp)

    db.session.add(category_info)
    db.session.commit()
    return jsonify(resp)


"""
小节
"""


@route_question.route("/type3_index")
def type3_index():
    resp_data = {}
    req = request.values
    if req.get('parent_id', '1').isdigit():
        parent_id = int(req.get('parent_id', '1'))
    else:
        parent_id = 1
    query = CategoryQuestion.query.filter(CategoryQuestion.category_type == 3,
                                          CategoryQuestion.parent_category_id == parent_id)
    if 'mix_kw' in req:
        rule = CategoryQuestion.name.ilike(f"%{req['mix_kw']}%")
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(CategoryQuestion.status == req['status'])

    if 'search_type' in req and int(req['search_type']) > -1:
        query = query.filter(CategoryQuestion.type == int(req['search_type']))
    page = request.values.get('p', '')
    total_pages = int(math.ceil(query.count() / app.config['PAGE_SIZE']))
    page = int(page) if page.isdigit() and int(page) > 0 and int(page) <= total_pages else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace(f'&p={page}', '')
    }

    pages = iPagination(page_params)

    offset = (page - 1) * app.config['PAGE_SIZE']
    end = page * app.config['PAGE_SIZE']
    profession_list = query.order_by(CategoryQuestion.name).all()[offset:end]
    resp_data['profession_list'] = profession_list
    resp_data['pages'] = pages
    resp_data['search_content'] = req.get('mix_kw', '')
    parent_id=[CategoryQuestion.query.filter(CategoryQuestion.id==parent_id).first().parent_category_id,parent_id]
    resp_data['parent_id'] = parent_id
    return ops_render("question/type3_index.html", resp_data)


@route_question.route("/type3_set", methods=['POST', 'GET'])
def type3_set():
    if request.method == 'GET':
        val = request.values
        id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
        parent_id = int(val['parent_id']) if val.get('parent_id', '') and val.get('parent_id', '').isdigit() else 1
        info = CategoryQuestion.query.filter_by(id=id).first()
        resp_data = {}
        if info:
            resp_data['info'] = info
            parent_id = info.parent_category_id
        else:
            resp_data['info'] = None
        parent_id = [CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category_id,
                     parent_id]
        resp_data['parent_id'] = parent_id
        return ops_render('question/type3_set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    id = int(req['id']) if req.get('id', '') and req.get('id', '').isdigit() else 0
    parent_id = int(req['parent_id']) if req.get('parent_id', '') and req.get('parent_id', '').isdigit() else 1
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else 0
    is_free = req['is_free'] if 'is_free' in req else 0
    is_hot = req['is_hot'] if 'is_hot' in req else 0
    if name is None or len(name) < 2:
        resp['code'] = -1
        resp['msg'] = '请输入2位及以上的小节名称'
        return jsonify(resp)
    query = CategoryQuestion.query.filter(CategoryQuestion.parent_category_id == parent_id)

    category_info = query.filter(CategoryQuestion.id != id, CategoryQuestion.name == name).first()
    if category_info:
        resp['code'] = -1
        resp['msg'] = '小节名已存在'
        return jsonify(resp)

    category_info = query.filter(CategoryQuestion.id == id).first()
    if not category_info:
        category_info = CategoryQuestion()
        category_info.created_time = get_current_time()

    category_info.name = name
    category_info.category_type = 3
    category_info.is_hot = int(is_hot)
    category_info.is_free = int(is_free)
    category_info.price = price
    category_info.creat_time = get_current_time()
    category_info.parent_category_id = parent_id

    db.session.add(category_info)
    db.session.commit()
    parent_id = [CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category_id,
                 parent_id]
    resp['parent_id'] = parent_id
    return resp


@route_question.route('/type3_ops', methods=['POST'])
def type3_ops():
    resp = {'code': 200, 'msg': '操作成功'}
    val = request.values
    id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
    act = val.get('act', '')
    if id < 1:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    category_info = CategoryQuestion.query.filter_by(id=id).first()
    if not category_info:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act == 'remove':
        category_info.status = 0
    if act == 'recover':
        category_info.status = 1

    db.session.add(category_info)
    db.session.commit()
    return jsonify(resp)





"""
题目
"""


@route_question.route("/question_index")
def question_index():
    resp_data = {}
    req = request.values
    if req.get('parent_id', '1').isdigit():
        parent_id = int(req.get('parent_id', '1'))
    else:
        parent_id = 1
    query = Question.query.filter(Question.parent_id == parent_id)
    if 'mix_kw' in req:
        rule = Question.name.ilike(f"%{req['mix_kw']}%")
        query = query.filter(rule)


    if 'search_type' in req and int(req['search_type']) > -1:
        query = query.filter(Question.type == int(req['search_type']))
    page = request.values.get('p', '')
    total_pages = int(math.ceil(query.count() / app.config['PAGE_SIZE']))
    page = int(page) if page.isdigit() and int(page) > 0 and int(page) <= total_pages else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace(f'&p={page}', '')
    }

    pages = iPagination(page_params)

    offset = (page - 1) * app.config['PAGE_SIZE']
    end = page * app.config['PAGE_SIZE']
    profession_list = query.order_by(Question.name).all()[offset:end]
    resp_data['profession_list'] = profession_list
    resp_data['pages'] = pages
    resp_data['search_content'] = req.get('mix_kw', '')

    parent_id = [CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category.parent_category_id,CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category_id,
                 parent_id]
    resp_data['parent_id'] = parent_id
    return ops_render("question/question_index.html", resp_data)


@route_question.route("/question_set", methods=['POST', 'GET'])
def question_set():
    if request.method == 'GET':
        val = request.values
        id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
        parent_id = int(val['parent_id']) if val.get('parent_id', '') and val.get('parent_id', '').isdigit() else 1
        info = Question.query.filter_by(id=id).first()
        resp_data = {}
        if info:
            resp_data['info'] = info
            parent_id = info.parent_id
            if info.type=='1' or info.type=='2':
                choices_list = info.choices.split("#$")[:-1]
                choices = []
                for i in range(len(choices_list)):
                    choices.append([chr(ord('A')+i),choices_list[i]])
                resp_data["end_chr"] = chr(ord('A')+i+1)
                resp_data["choices"]=choices

        else:
            resp_data['info'] = None
        parent_id = [
            CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category.parent_category_id,
            CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category_id,
            parent_id]
        resp_data['parent_id'] = parent_id
        return ops_render('question/question_set.html', resp_data)

    resp = {'code': 200, 'msg': '操作成功', "data": {}}
    req = request.values
    print(req.get('id', '').isdigit())
    id = int(req['id']) if req.get('id', '') and req.get('id', '').isdigit() else 0
    name = req['name'] if 'name' in req else ''
    type = req['type'] if 'type' in req else 1
    parent_id = int(req['parent_id']) if req.get('parent_id', '') and req.get('parent_id', '').isdigit() else 1
    choices = req['choices'] if 'choices' in req else ''
    answer = req['answer'] if 'answer' in req else ''
    explanation = req['explanation'] if 'explanation' in req else ''

    # if name is None or len(name) < 2:
    #     resp['code'] = -1
    #     resp['msg'] = '请输入2位及以上的小节名称'
    #     return jsonify(resp)
    query = Question.query.filter(Question.parent_id == parent_id)
    question_info = query.filter(Question.id != id, Question.name == name).first()
    print(question_info,id)
    if question_info:
        resp['code'] = -1
        resp['msg'] = '题目名已存在'
        return jsonify(resp)

    question_info = query.filter(Question.id == id).first()
    if not question_info:
        question_info = Question()
        question_info.created_time = get_current_time()
        parent = CategoryQuestion.query.filter(CategoryQuestion.id==parent_id).first()
        parent.count+=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count+=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count+=1
        db.session.add(parent)
    #
    question_info.name = name
    question_info.type = type
    question_info.parent_id = parent_id
    if type=='1' or type=='2':
        question_info.choices = choices
    question_info.answer = answer
    question_info.explanation = explanation
    question_info.type1_id = QuestionService.get_type1_id_from(parent_id)
    db.session.add(question_info)
    db.session.commit()
    parent_id = [CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category.parent_category_id,CategoryQuestion.query.filter(CategoryQuestion.id == parent_id).first().parent_category_id,
                 parent_id]
    resp['parent_id'] = parent_id
    return resp


@route_question.route('/question_ops', methods=['POST'])
def question_ops():
    resp = {'code': 200, 'msg': '操作成功'}
    val = request.values
    id = int(val['id']) if val.get('id', '') and val.get('id', '').isdigit() else 0
    act = val.get('act', '')
    if id < 1:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    question_info = Question.query.filter_by(id=id).first()
    if not question_info:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)
    if act not in ['true_remove']:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        return jsonify(resp)

    if act == 'true_remove':
        parent_id = question_info.parent.id
        db.session.execute(f'DELETE FROM question WHERE (id = {question_info.id})')
        parent = CategoryQuestion.query.filter(CategoryQuestion.id==parent_id).first()
        parent.count-=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count-=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count-=1
        db.session.add(parent)
        db.session.commit()
        return jsonify(resp)

    return jsonify(resp)


@route_question.route('/upload_the_execl', methods=['POST'])
def upload_the_execl_file():
    resp = {'code': 200, 'msg': '操作成功'}
    file = request.files['file']
    parent_id = request.values.get('parent_id',1)
    type1_id = QuestionService.get_type1_id_from(parent_id)
    print(file.filename)  # 打印文件名
    if file.filename.split(".")[1]!='xlsx':
        resp['msg']='文件格式错误'
        return resp
    f = file.read()  # 文件内容
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字
    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    nrows = table.nrows  # 获取该sheet中的有效行数
    ncols = table.ncols  # 获取该sheet中的有效列数
    for i in range(2,nrows):
        q = Question()
        q.name = table.cell_value(i,0)

        parent = CategoryQuestion.query.filter(CategoryQuestion.id==parent_id).first()
        parent.count+=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count+=1
        db.session.add(parent)
        parent = parent.parent_category
        parent.count+=1
        db.session.add(parent)

        if table.cell_value(i,1) in ['单选题','多选题']:
            q.type = 1 if table.cell_value(i,1)=='单选题' else 2
            choices=[]
            for j in range(2,7):
                if table.cell_value(i,j):
                    choices.append(table.cell_value(i,j))
            q.choices = '#$'.join(choices)+'#$'
            q.answer = table.cell_value(i, 7)
        if table.cell_value(i,1)=='判断题':
            q.type=4
            q.answer = '1' if table.cell_value(i, 7)=='正确' else '0'
        if table.cell_value(i, 1) == '问答题':
            q.type=3
            q.answer = table.cell_value(i, 7)
        if table.cell_value(i,1) not in ['单选题','多选题','判断题','问答题']:
            resp['msg']='不支持类型'+table.cell_value(i,1)
            return resp
        q.parent_id = int(request.values['parent_id'])
        q.type1_id = type1_id
        q.explanation = table.cell_value(i, 8)
        q.created_time = get_current_time()
        db.session.add(q)
    db.session.commit()
    return resp