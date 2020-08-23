# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from application import db


class CategoryQuestion(db.Model):
    __tablename__ = 'category_question'

    id = db.Column(db.Integer, primary_key=True)
    category_type = db.Column(db.Integer, nullable=False, info="类目级别(1,'专业'), (2,'大章节'),(3,'小章节'')")
    type = db.Column(db.Integer, info="类目大类(1,'统考类专业课'), (2,'专业硕士')")
    main_image = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    is_hot = db.Column(db.Integer, server_default=db.FetchedValue(), info='(1,热门),(0,不热门)')
    is_free = db.Column(db.Integer, server_default=db.FetchedValue(), info='(1,免费),(0,不免费)')
    creat_time = db.Column(db.DateTime, nullable=False)
    parent_category_id = db.Column(db.ForeignKey('category_question.id'), index=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='(1,正常)(0,删除)')
    name = db.Column(db.String(45))
    price = db.Column(db.String(45))
    count = db.Column(db.Integer,server_default=db.FetchedValue())

    parent_category = db.relationship('CategoryQuestion', remote_side=[id], primaryjoin='CategoryQuestion.parent_category_id == CategoryQuestion.id', backref='category_questions')


    @property
    def type_desc(self):
        type_mapping = {
            "1":"统考类专业课",
            "2":"专业硕士"
        }
        return type_mapping[str(self.type)]




    def keys(self):
        return ['id','type','is_hot','is_free','status','name','price','count']
    def __getitem__(self, item):
        return getattr(self,item)

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    type1_id = db.Column(db.Integer)
    parent_id = db.Column(db.ForeignKey('category_question.id', ondelete='CASCADE'), nullable=False, index=True)
    answer = db.Column(db.String(4500))
    name = db.Column(db.String(4500))
    type = db.Column(db.String(45), info='(1,单选题)(2,多选题)(3,问答题)(4,判断题)')
    choices = db.Column(db.String(4500))
    explanation = db.Column(db.String(4500))
    created_time = db.Column(db.DateTime, nullable=False)


    parent = db.relationship('CategoryQuestion', primaryjoin='Question.parent_id == CategoryQuestion.id', backref='questions')






    def keys(self):
        return ['id','name','answer','type','choices','explanation']

    def __getitem__(self, item):
        return getattr(self,item)