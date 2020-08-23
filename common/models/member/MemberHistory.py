# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, func
from flask_sqlalchemy import SQLAlchemy


from application import db


class MemberHistory(db.Model):
    __tablename__ = 'member_history'

    id = db.Column(db.Integer, primary_key=True)
    type1_id = db.Column(db.Integer)
    created_time = db.Column(db.DateTime('%Y-%m-%d %H:%M:%S'))
    member_id = db.Column(db.Integer)
    type3_id = db.Column(db.Integer)


