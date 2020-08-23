# coding: utf-8
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

from application import db


class MemberQuestionHistory(db.Model):
    __tablename__ = 'member_question_history'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    mine_answer = db.Column(db.String(4500))
    type3_id = db.Column(db.Integer)
