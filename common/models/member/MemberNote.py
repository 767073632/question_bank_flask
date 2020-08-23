# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from application import db


class MemberNote(db.Model):
    __tablename__ = 'member_notes'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    type1_id = db.Column(db.Integer)
    type3_id = db.Column(db.Integer)
    question_id = db.Column(db.ForeignKey('question.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    notes = db.Column(db.String(4000), nullable=False, server_default=db.FetchedValue(), info='会员手机号码')
    question = db.relationship('Question', primaryjoin='MemberNote.question_id == Question.id', backref='member_notes')


