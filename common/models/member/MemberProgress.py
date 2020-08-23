# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from application import db


class MemberProgres(db.Model):
    __tablename__ = 'member_progress'

    id = db.Column(db.Integer, primary_key=True)
    type1 = db.Column(db.Integer)
    type2 = db.Column(db.Integer)
    type3 = db.Column(db.ForeignKey('category_question.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    count = db.Column(db.Integer, server_default=db.FetchedValue())
    member_id = db.Column(db.Integer)

    category_question = db.relationship('CategoryQuestion', primaryjoin='MemberProgres.type3 == CategoryQuestion.id', backref='member_progress')
