# coding: utf-8
from base import db
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TEXT, MEDIUMTEXT
from book import Book

class BookShelf(db.Model):
    ''' 书架 '''
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), index=True)                   # 书籍ID
    name = db.Column(db.String(100))                                # 书架名称('myself', 'hot', 'new', 'recommend', 'finish') 
    user_id = db.Column(db.Integer())                               # 用户id, 用于myself 自己的书架
    ranking = db.Column(db.Integer(), default=0)                    # 用于排序
    rate = db.Column(db.Integer(), default=0)                       # 阅读进度(百分率分子)
    showed = db.Column(db.Boolean(), default=True)                  # 是否显示
    sex = db.Column(db.Integer(), server_default='0')               # 热门和新书需要区分男女频（1：男；2: 女)
    created = db.Column(db.DateTime, server_default=func.now())     # 创建时间
    updated = db.Column(db.DateTime, server_default=func.now())     # 更新时间 

    db.Index('ix_book_id_name_user_id', book_id, name, user_id, unique=True)

    def __init__(self, book_id, name, user_id, ranking, rate, showed, sex):
        self.book_id = book_id
        self.name = name
        self.user_id = user_id
        self.ranking = ranking
        self.rate = rate
        self.showed = showed
        self.sex = sex

    def to_admin_dict(self):
        book = Book.query.filter_by(book_id=self.book_id).first()
        return dict(id = self.id,
                    book_id = self.book_id,
                    book = book.to_admin_dict() if book else {},
                    name = self.name,
                    user_id = self.name,
                    ranking = self.ranking,
                    rate = self.rate,
                    showed = int(self.showed) if self.showed else 0,
                    sex = self.sex,
                    created = self.created.strftime('%Y-%m-%d %H:%M:%S'))

class BookShelfName(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    updated = db.Column(db.DateTime, server_default=func.now())
    created = db.Column(db.DateTime, server_default=func.now())

    def __init__(self, name, nickname):
        self.name = name
        self.nickname = nickname

    def to_admin_dict(self):
        return dict(id = self.id,
                    name = self.name,
                    nickname = self.nickname,
                    created = self.created.strftime('%Y-%m-%d %H:%M:%S'),
                    updated = self.updated.strftime('%Y-%m-%d %H:%M:%S'))
