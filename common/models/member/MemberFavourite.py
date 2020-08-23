# coding: utf-8
from sqlalchemy import Column, Integer
from flask_sqlalchemy import SQLAlchemy

from application import db


class MemberFavourite(db.Model):
    __tablename__ = 'member_favourite'

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    type1_id = db.Column(db.Integer)
    type3_id = db.Column(db.Integer)