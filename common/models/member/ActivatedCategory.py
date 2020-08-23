# coding: utf-8
from sqlalchemy import Column, Integer
from flask_sqlalchemy import SQLAlchemy

from application import db


class ActivatedCategory(db.Model):
    __tablename__ = 'activated_category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
