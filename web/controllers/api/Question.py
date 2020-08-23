import random

from flask import jsonify, g
from sqlalchemy import func

from application import db, app
from common.libs.Helper import get_current_time, iPagination
from common.libs.category.CategoryService import CategoryService
from common.libs.question.QuestionService import QuestionService
from common.models.CategoryQuestion import Question, CategoryQuestion
from common.models.member.MemberMistakes import MemberMistake
from common.models.member.MemberProgress import MemberProgres
from common.models.member.MemberFavourite import MemberFavourite
from common.models.member.MemberHistory import MemberHistory
from common.models.member.MemberNote import MemberNote
from common.models.member.MemberQuestionHistory import MemberQuestionHistory
from web.controllers.api import route_api, request

"""
传入type3id 拿所有题数据
"""
@route_api.route("/question/question-info",methods = [ "GET","POST" ])
def question():
    req = request.values
    type3_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type3_id==0 :
        resp['msg']='id无效'
        return resp

    question_info=Question.query.filter(Question.parent_id==type3_id)
    if not question_info:
        resp['msg']='不存在题目'
        return resp
    resp['data']=QuestionService.get_question(question_info)
    return jsonify( resp )










"""
5个基本按钮
"""



"""
随机练习
传入type1 id和token 随机练习的题数question_size
"""
@route_api.route("/question/question-random",methods = [ "GET","POST" ])
def question_random():
    req = request.values
    type1_id = int(req.get('id')) if req.get('id')and req.get('id').isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    question_size = int(req.get('question_size')) if req.get('question_size')and req.get('question_size').isdigit() else 50
    question_info=Question.query.filter(Question.type1_id==type1_id)
    if question_info.count()>question_size:
        question_info_list = []
        num_list = random.sample(range(question_info.count()),question_size)
        for i in num_list:
            question_info_list.append(question_info[i])
        question_info = question_info_list


    if not question_info:
        resp['msg']='不存在题目'
        return resp
    resp['data']=QuestionService.get_question(question_info)
    return jsonify( resp )



"""
传入type1 id和token 分页的page_size和页数page 获取所有错题信息
"""
@route_api.route("/question/question-mistakes-collection",methods = [ "GET","POST" ])
def question_mistakes_collection():
    req = request.values
    type1_id = int(req.get('id')) if req.get('id')and req.get('id').isdigit() else 0
    page_size = int(req.get('page_size')) if req.get('page_size')and req.get('page_size').isdigit() else 0
    page = int(req.get('page')) if req.get('page')and req.get('page').isdigit() else 0

    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    question_list = []
    member_mistakes_info=MemberMistake.query.filter(MemberMistake.type1_id==type1_id,MemberMistake.member_id==g.member_info.id)
    if member_mistakes_info:
        for i in range(member_mistakes_info.count()):
            q = Question.query.filter(Question.id==member_mistakes_info[i].question_id).first()
            question_list.append(q)

    if not question_list:
        resp['msg']='不存在题目'
        return resp

    page_params = {
        'total': len(question_list),
        'page_size': page_size,
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': ''
    }

    pages = iPagination(page_params)

    offset = (page - 1) * page_size
    end = page * page_size
    question_list = question_list[offset:end]


    resp['data']=QuestionService.get_question(question_list)
    return jsonify( resp )





"""
传入type1 id和token 获取所有收藏题目
"""
@route_api.route("/question/question-favorites",methods = [ "GET","POST" ])
def question_favorites():
    req = request.values
    type1_id = int(req.get('id')) if req.get('id')and req.get('id').isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    question_list = []
    member_favourite_info=MemberFavourite.query.filter(MemberFavourite.type1_id==type1_id,MemberFavourite.member_id==g.member_info.id)
    if member_favourite_info:
        for i in range(member_favourite_info.count()):
            q = Question.query.filter(Question.id==member_favourite_info[i].question_id).first()
            question_list.append(q)

    if not question_list:
        resp['msg']='不存在题目'
        return resp
    resp['data']=QuestionService.get_question(question_list)
    return jsonify( resp )


"""
传入type1 id和token 获取所有笔记
"""
@route_api.route("/question/question-notes",methods = [ "GET","POST" ])
def question_notes():
    req = request.values
    type1_id = int(req.get('id')) if req.get('id')and req.get('id').isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    question_list = []
    member_notes_info=MemberNote.query.filter(MemberNote.type1_id==type1_id,MemberNote.member_id==g.member_info.id)
    if member_notes_info:
        for i in range(member_notes_info.count()):
            q = Question.query.filter(Question.id==member_notes_info[i].question_id).first()
            question_list.append(q)

    if not question_list:
        resp['msg']='不存在题目'
        return resp
    resp['data']=QuestionService.get_question(question_list)
    return jsonify( resp )



"""
传入type1 id和token 获取所有历史
"""
@route_api.route("/question/question-history",methods = [ "GET","POST" ])
def question_history():
    req = request.values
    type1_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp

    member_history_info=MemberHistory.query.filter(MemberHistory.type1_id==type1_id,MemberHistory.member_id==g.member_info.id)
    if not member_history_info:
        resp['msg']='不存在历史记录'
        resp['code']=-1
        return resp
    resp['data']=QuestionService.get_history_from(member_history_info)
    return jsonify( resp )
















"""
问题 按钮接口
"""

"""
收藏
"""
@route_api.route("/question/favourite",methods = [ "GET","POST" ])
def favourite():
    req = request.values
    question_id = int(req.get('question_id',0)) if req.get('question_id',0)and req.get('question_id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if question_id==0 :
        resp['msg']='id无效'
        return resp

    question_info=Question.query.filter(Question.id==question_id).first()
    if not question_info:
        resp['msg']='不存在题目'
        return resp
    favourite_info = MemberFavourite.query.filter(MemberFavourite.question_id==question_id).first()
    if favourite_info:
        db.session.delete(favourite_info)
    else:
        favourite_info = MemberFavourite()
        favourite_info.member_id = g.member_info.id
        favourite_info.question_id=question_id
        favourite_info.type1_id = QuestionService.get_type1_id_from(question_info.parent_id)
        favourite_info.type3_id = question_info.parent_id
        db.session.add(favourite_info)

    db.session.commit()
    return jsonify( resp )



"""
笔记
"""
@route_api.route("/question/note",methods = [ "GET","POST" ])
def note():
    req = request.values
    question_id = int(req.get('question_id',0)) if req.get('question_id',0)and req.get('question_id',0).isdigit() else 0
    notes = req.get('notes','')
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if question_id==0 :
        resp['msg']='id无效'
        return resp

    question_info=Question.query.filter(Question.id==question_id).first()
    if not question_info:
        resp['msg']='不存在题目'
        return resp
    notes_info = MemberNote.query.filter(MemberNote.question_id==question_id).first()
    if not notes_info:
        notes_info = MemberNote()
    notes_info.member_id = g.member_info.id
    notes_info.question_id=question_id
    notes_info.type1_id = QuestionService.get_type1_id_from(question_info.parent_id)
    notes_info.type3_id = question_info.parent_id
    notes_info.notes = notes
    db.session.add(notes_info)

    db.session.commit()
    return jsonify( resp )







"""
提交做题数据
"""

@route_api.route("/question/question-submit",methods = [ "GET","POST" ])
def question_submit():
    req = request.values
    type3_id = int(req.get('type3_id',0)) if req.get('type3_id',0)and req.get('type3_id',0).isdigit() else 0

    question_id_list = eval(req.get('question_id_list',''))
    answer_list = eval(req.get('answer_list',''))
    resp = { 'code':200 ,'msg':'成功~','data':{} }


    if not type3_id:
        resp['code']=-1
        resp['msg']='信息格式不正确'
        return jsonify( resp )

    if CategoryQuestion.query.filter(CategoryQuestion.id==type3_id).first().category_type==1:
        return jsonify( resp )

    if not type(question_id_list) ==list:
        resp['code']=-1
        resp['msg']='信息格式不正确'
        return jsonify( resp )

    if not type(answer_list) ==list:
        resp['code']=-1
        resp['msg']='信息格式不正确'
        return jsonify( resp )

    if not len(question_id_list)==len(answer_list):
        resp['code']=-1
        resp['msg']='信息格式不正确'
        return jsonify( resp )

    count =0
    # 存入member_question_histroy中
    for i in range(len(question_id_list)):
        member_question_info = MemberQuestionHistory.query.filter(MemberQuestionHistory.question_id==question_id_list[i],MemberQuestionHistory.member_id==g.member_info.id).first()
        if not member_question_info:
            count+=1
            member_question_info = MemberQuestionHistory()
            member_question_info.member_id=g.member_info.id
            member_question_info.question_id = question_id_list[i]
            member_question_info.type3_id = type3_id
        member_question_info.mine_answer = answer_list[i]
        q = Question.query.filter(Question.id==question_id_list[i]).first()
        #加入错题集
        if q.answer!=answer_list[i]:
            member_mistake_info = MemberMistake.query.filter(MemberMistake.member_id==g.member_info.id,MemberMistake.question_id==question_id_list[i]).first()
            if not member_mistake_info:
                member_mistake_info = MemberMistake()
                member_mistake_info.question_id = question_id_list[i]
                member_mistake_info.type1_id = QuestionService.get_type1_id_from(type3_id)
                member_mistake_info.member_id = g.member_info.id
                db.session.add(member_mistake_info)
        db.session.add(member_question_info)
    #存入member_progress
    member_progress_info =MemberProgres.query.filter(MemberProgres.type3==type3_id,MemberProgres.member_id==g.member_info.id).first()
    if not member_progress_info:
        member_progress_info = MemberProgres()
        member_progress_info.type3=type3_id
        member_progress_info.type1=QuestionService.get_type1_id_from(type3_id)
        member_progress_info.type2 = CategoryQuestion.query.filter(CategoryQuestion.parent_category_id==member_progress_info.type1).first().id
        member_progress_info.count=0
        member_progress_info.member_id = g.member_info.id
    member_progress_info.count+=count

    # 存入member_history中
    member_history = MemberHistory.query.filter(MemberHistory.type3_id==type3_id,MemberHistory.member_id==g.member_info.id).first()
    if not member_history:
        member_history = MemberHistory()
        member_history.member_id = g.member_info.id
        member_history.type3_id=type3_id
        member_history.type1_id = QuestionService.get_type1_id_from(type3_id)
    member_history.created_time = get_current_time()
    db.session.add(member_history)
    db.session.add(member_progress_info)
    db.session.commit()
    return jsonify( resp )


"""
清空错题数据
"""
@route_api.route("/question/question-mistakes-collection-empty",methods = [ "GET","POST" ])
def mistakes_collection_empty():
    req = request.values
    type1_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp
    sql = f'delete from mxweixin.member_mistakes  where (type1_id ={type1_id} and member_id={g.member_info.id});'
    db.session.execute(sql)
    db.session.commit()
    return jsonify( resp )

"""
获取错题总数
"""
@route_api.route("/question/question-mistakes-collection-count",methods = [ "GET","POST" ])
def mistakes_collection_count():
    req = request.values
    type1_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp
    mistakes_info = MemberMistake.query.filter(MemberMistake.type1_id == type1_id,MemberMistake.member_id == g.member_info.id)

    resp['count'] = mistakes_info.count()
    return jsonify( resp )




"""
获取type1的总进度
"""
@route_api.route("/question/question-mastery",methods = [ "GET","POST" ])
def mistakes_mastery():
    req = request.values
    type1_id = int(req.get('id',0)) if req.get('id',0)and req.get('id',0).isdigit() else 0
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    if type1_id==0 :
        resp['msg']='id无效'
        return resp
    data ={}
    data['count'] = CategoryQuestion.query.filter(CategoryQuestion.id==type1_id).first().count
    auth_cookie = request.headers.get("Authorization")
    if not auth_cookie:
        print(123)
        data['mastery'] = 0
    else:
        member_id = int(auth_cookie.split("#")[1])
        mastery_info = MemberProgres.query.filter(MemberProgres.member_id==member_id,MemberProgres.type1==type1_id)
        count = 0
        for i in range(mastery_info.count()):
            count += mastery_info[i].count
        data['mastery'] = count
    data['mastery_%'] = '%.0f'%(data['mastery']/data['count']*100)
    resp['data']=data
    return jsonify( resp )