# coding: utf-8
from sqlalchemy import Column, Integer
from flask_sqlalchemy import SQLAlchemy

from application import db


class MemberMistake(db.Model):
    __tablename__ = 'member_mistakes'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    member_id = db.Column(db.Integer)
    type1_id = db.Column(db.Integer)
