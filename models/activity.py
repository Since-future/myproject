# -*- coding: utf-8 -*-
"""
Doc:

Created on 2017/9/15
@author: MT
"""
from base import db
from sqlalchemy.sql import func


class SignIn(db.Model):
    """签到记录表"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    last_sign_day = db.Column(db.Date)  # 上次签到日
    sign_days = db.Column(db.String(100), default='[]')  # 当月签到日列表
    multi_sign_bonus = db.Column(db.String(15), default='[]')  # 累计签到奖励领取列表
    created = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, user_id, last_sign_day, sign_days):
        self.user_id = user_id
        self.last_sign_day = last_sign_day
        self.sign_days = sign_days


class BindPhoneActivity(db.Model):
    """绑定手机送288阅币活动"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    created = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, user_id):
        self.user_id = user_id
