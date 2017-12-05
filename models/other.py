# coding: utf-8
from datetime import datetime

from sqlalchemy.sql.schema import PrimaryKeyConstraint

from base import db
from sqlalchemy.sql import func
import json

class Banner(db.Model):
    """广告表"""
    id              = db.Column(db.Integer(), primary_key=True)
    title           = db.Column(db.String(100))
    platform        = db.Column(db.String(50))
    activity        = db.Column(db.String(50))
    ios_activity    = db.Column(db.String(50))
    params          = db.Column(db.String(150)) # 客户端需要参数,保存字典,暂时需要{'book_id':111, 'book_name': u''}
    sex             = db.Column(db.Integer(), default=1) # 0: 所有 1：男；2: 女
    url             = db.Column(db.String(150))
    banner_url      = db.Column(db.String(150))
    level           = db.Column(db.Integer(), default=0)
    showed          = db.Column(db.Boolean(), default=False)
    modified        = db.Column(db.DateTime(), server_default=func.now())
    created         = db.Column(db.DateTime(), server_default=func.now())
    m_id            = db.Column(db.Integer(), server_default='-1')

    def __init__(self, data):
        self.title = data.get('title', '')
        self.platform = data.get('platform', '')
        self.activity = data.get('activity', '')
        self.ios_activity = data.get('ios_activity', '')
        self.params = json.dumps(json.loads(data.get('params', json.dumps({}))))
        self.sex = int(data.get('sex', 0))
        self.url = data.get('url', '')
        self.banner_url = data['banner_url']
        self.level = int(data.get('level', 0))
        self.showed = 1 if int(data.get('showed', 0)) else 0
        self.m_id = int(data.get('m_id', -1))

    def update(self, data):
        print data
        self.title = data.get('title', '')
        self.platform = data.get('platform', '')
        self.activity = data.get('activity', '')
        self.ios_activity = data.get('ios_activity', '')
        self.params = json.dumps(json.loads(data.get('params', json.dumps({}))))
        self.sex = int(data.get('sex', 0))
        self.url = data.get('url', '')
        self.banner_url = data['banner_url']
        self.level = int(data.get('level', 0))
        self.showed = 1 if int(data.get('showed', 0)) else 0
        self.m_id = int(data.get('m_id', -1))
        self.modified = datetime.now()



    def to_admin_dict(self):
        return dict(id = self.id,
                    title = self.title,
                    platform = self.platform,
                    activity = self.activity,
                    ios_activity = self.ios_activity,
                    params = json.loads(self.params),
                    sex = self.sex,
                    url = self.url,
                    banner_url = self.banner_url,
                    level = self.level,
                    showed = int(self.showed),
                    created = self.created.strftime('%Y-%m-%d %H:%M:%S'),
                    modified = self.modified.strftime('%Y-%m-%d %H:%M:%S'))
    
    
    def to_dict(self):
        return dict(id = self.id,
                    title = self.title,
                    platform = self.platform,
                    activity = self.activity,
                    ios_activity = self.ios_activity,
                    params = json.loads(self.params),
                    sex = self.sex,
                    url = self.url,
                    banner_url = self.banner_url,
                    level = self.level
                    )
