# -*- coding: utf-8 -*-
"""
Doc: 更新书籍分类脚本
Created by MT at 2017/10/13
"""
from models import BookCategory, Book, db


def update_book_category():
    cate_dict = {cate.cate_name.encode('utf8'): cate.cate_id for cate in BookCategory.query.all()}

    for line in open('script/book_cate.txt').readlines():
        book_name, sex, cate_name = line.split()
        book = Book.query.filter_by(book_name=book_name).first()
        if not book:
            print "No book", book_name
            continue
        cate_id = cate_dict.get(cate_name)
        if not cate_id:
            print "No category", cate_name
            continue
        book.cate_id = cate_id
        book.channel_type = 1 if sex == '男' else 2
    db.session.commit()


def add_category():
    """增加分类"""
    cate_dict = {cate.cate_name.encode('utf8'): cate.cate_id for cate in BookCategory.query.all()}
    cate_str = {
        "现代都市": 1,
        "玄幻奇幻": 1,
        "武侠仙侠": 1,
        "军事历史": 1,
        "悬疑灵异": 1,
        "游戏竞技": 1,
        "科幻末世": 1,
        "现代言情": 3,
        "古代言情": 3,
        "总裁豪门": 3,
        "穿越架空": 3,
        "青春校园": 3,
        "耽美同人": 3,
    }
    for cate_name, parent in cate_str.iteritems():
        if cate_name not in cate_dict:
            db.session.add(BookCategory(cate_name, parent))
    db.session.commit()

