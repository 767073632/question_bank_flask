import base64
import hashlib
import string
import random

from flask import g

from common.libs.Helper import get_current_time
from common.models.CategoryQuestion import CategoryQuestion
from common.models.member import MemberProgress
from common.models.member.MemberFavourite import MemberFavourite
from common.models.member.MemberNote import MemberNote
from common.models.member.MemberProgress import MemberProgres
from common.models.member.MemberQuestionHistory import MemberQuestionHistory


class QuestionService():

    @staticmethod
    def get_type1_id_from(type3_id):
        type3 = CategoryQuestion.query.filter_by(id = type3_id).first()
        if not type3:
            return False
        type2 = type3.parent_category
        if not type2:
            return False
        type1 = type2.parent_category
        if type1:
            return type1.id
        return False


    @staticmethod
    def get_question(question_info):
        question_list = []
        if hasattr(g,'member_info'):
            member_id = g.member_info.id
        else:
            member_id=0
        if type(question_info)==list:
            lenth = len(question_info)
        else :
            lenth = question_info.count()
        for i in range(lenth):
            # print(question_info.count(),i,dict(question_info[i]))
            if question_info[i].type!='1':
                continue
            dict_question = dict(question_info[i])
            id = str(dict_question['id'])
            dict_question['testId'] = id
            dict_question['feedId'] = id
            dict_question['favorite'] = True if MemberFavourite.query.filter(MemberFavourite.question_id==id,MemberFavourite.member_id==member_id).first() else False
            dict_question['comments'] = MemberNote.query.filter(MemberNote.question_id==id,MemberNote.member_id==member_id).first().notes if MemberNote.query.filter(MemberNote.question_id==id,MemberNote.member_id==member_id).first() else ""
            dict_question['examId'] = id
            dict_question['questionId'] = id
            dict_question['qid'] = id
            dict_question['qbid'] = id
            dict_question['examAsk'] = dict_question['name']
            dict_question['examType'] = 'A'
            dict_question['examRight'] = dict_question['answer'][0] if dict_question['answer'][0] in ['A','B','C','D','E'] else 'A'
            mine_answer = MemberQuestionHistory.query.filter(MemberQuestionHistory.member_id==member_id,MemberQuestionHistory.question_id==dict_question['id']).first()
            dict_question['examMine'] = mine_answer.mine_answer if mine_answer else ''
            dict_question['examResolve'] = dict_question['explanation']
            dict_question['tempAnswer'] = dict_question['explanation']
            choices = dict_question['choices'].replace('\n','').split("#$")[:-1]
            newAnswer = []
            for j in range(len(choices)):
                newAnswer.append({'name':chr(ord('A')+j),"checked": False,"value": choices[j]})

            dict_question['newAnswer']=newAnswer
            dict_question['round']=''
            dict_question['productType']='ZHIYEYISHI'
            dict_question['examAnswer']=''
            dict_question['newExamAsk']={"imgs":[],'examAsk':dict_question['name']}
            dict_question['resolve']={"imgs":[],'examResolve':dict_question['explanation']}
            for key in ['id', 'name', 'answer', 'type', 'choices', 'explanation']:
                dict_question.pop(key)
            question_list.append(dict_question)

        return question_list

    @staticmethod
    def get_history_from(member_history_info):
        history_list = []
        for i in range(member_history_info.count()):
            dict_history = {}
            get_current_time()
            dict_history['created_time'] = str(member_history_info[i].created_time)
            type3_id = member_history_info[i].type3_id
            type3 = CategoryQuestion.query.filter(CategoryQuestion.id ==type3_id).first()
            type3_name = type3.name
            type2_name = type3.parent_category.name
            type1_name = type3.parent_category.parent_category.name
            finished_num = MemberProgres.query.filter(MemberProgres.member_id==g.member_info.id,MemberProgres.type3==type3_id).first()
            dict_history['finished_num'] = finished_num.count if finished_num else 0
            question_num = CategoryQuestion.query.filter(CategoryQuestion.id==type3_id).first()
            dict_history['question_num'] = question_num.count if question_num else 0
            dict_history['path'] = "/".join([type1_name,type2_name,type3_name])
            dict_history['type3_id'] = type3_id
            history_list.append(dict_history)

        return history_list