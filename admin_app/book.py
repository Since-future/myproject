# coding=utf-8

from flask import Blueprint, request
from flask.ext.login import login_required, current_user
from models import Book, BookCategory, BookVolume, BookChapters
from models import db
import json
from lib import utils

bp = Blueprint("book", __name__)

@bp.route('/list')
@login_required
def list():
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))
    sql = 'select count(*) from book'
    total = db.session.execute(sql).scalar() or 0
    if current_user.email == 'sina':
        books = Book.query.filter_by(source='sina').paginate(page_no, per_page=num, error_out=False).items
    elif current_user.email == 'kaixing':
        books = Book.query.filter_by(source='kaixing').paginate(page_no, per_page=num, error_out=False).items
    elif current_user.email == 'jingyu':
        books = Book.query.filter_by(source='jingyu').paginate(page_no, per_page=num, error_out=False).items
    else:
        books = Book.query.filter().paginate(page_no, per_page=num, error_out=False).items
    book_list = [book.to_admin_dict() for book in books]
    return json.dumps({'code':0, 'data': book_list, 'total': total})

def book_to_dict(book):
    cate = BookCategory.query.filter_by(cate_id=book.cate_id).first()
    cate_name = cate.cate_name if cate else str(self.cate_id)
    source = ''
    if book.source == 'sina':
        source = u'新浪阅读'
    elif book.source == 'kaixing':
        source = u'恺兴阅读'
    elif book.source == 'zhangyue':
        source = u'掌阅'
    elif book.source == 'jingyu':
        source = u'鲸鱼阅读'
    elif book.source == 'anzhi':
        source = u'安之'
    else:
        source = book.source

    return dict(
                book_id = book.book_id,
                channel_book_id = book.channel_book_id,
                book_name = book.book_name,
                cate_id = cate_name,
                channel_type = book.channel_type,
                author_name = book.author_name,
                chapter_num = book.chapter_num,
                is_publish = book.is_publish,
                status = book.status,
                create_time = book.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                cover = book.cover if book.cover else '',
                intro = book.intro if book.intro else '',
                word_count = book.word_count,
                update_time = book.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                created = book.created.strftime('%Y-%m-%d %H:%M:%S'),
                source = source,
                showed = int(book.showed)
                )


@bp.route('/search')
@login_required
def search():
    book_name = request.args.get('book_name', '')
    author_name = request.args.get('author_name', '')
    book_id = request.args.get('book_id', 0, int)
    channel_type = request.args.get('channel_type', 0, int)
    is_publish = request.args.get('is_publish', 0, int)
    status = request.args.get('status', 0, int)
    cate_id = request.args.get('cate_id', 0, int)
    source = request.args.get('source', '')

    page_no = request.args.get("page_no", 1, int)
    num = request.args.get("num", 20, int)
    sql = 'select * from book where 1=1 '
    total_sql = 'select count(*) from book where 1=1 '
    if book_name:
        sql = sql + ' and book_name like "%%%s%%" ' %(book_name)
        total_sql += ' and book_name like "%%%s%%" ' %(book_name)
    if author_name:
        sql = sql + ' and author_name like "%%%s%%" ' %(author_name)
        total_sql += ' and author_name like "%%%s%%" ' %(author_name)
    if book_id:
        sql = sql + ' and book_id=%s ' %(book_id)
        total_sql += ' and book_id=%s ' %(book_id)
    if channel_type:
        sql = sql + ' and channel_type=%s ' %(channel_type)
        total_sql += ' and channel_type=%s ' %(channel_type)
    if is_publish:
        sql = sql + ' and is_publish=%s ' %(is_publish)
        total_sql += ' and is_publish=%s ' %(is_publish)
    if status:
        sql = sql + ' and status=%s ' %(status)
        total_sql += ' and status=%s ' %(status)
    if cate_id:
        sql = sql + ' and cate_id=%s ' %(cate_id)
        total_sql += ' and cate_id=%s ' %(cate_id)
    if source:
        sql = sql + ' and source="%s" ' %(source)
        total_sql += ' and source="%s" ' %(source)

    sql = sql + ' limit %s, %s' %(num*(page_no - 1), num)
    print sql

    total = db.session.execute(total_sql).scalar() or 0
    results = db.session.execute(sql).fetchall()
    data = [ book_to_dict(book) for book in results ]
    return json.dumps({'code': 0, 'data': data, 'total': total})

@bp.route('/get_source_type')
@login_required
def get_source_type():
    data = [
        {'source_type': 'sina', 'source_type_name': u'新浪阅读'},
        {'source_type': 'kaixing', 'source_type_name': u'恺兴阅读'},
        {'source_type': 'jingyu', 'source_type_name': u'鲸鱼阅读'},
        {'source_type': 'zhangyue', 'source_type_name': u'掌阅阅读'},
        {'source_type': 'anzhi', 'source_type_name': u'安之阅读'},
    ]
    return json.dumps({'code':0, 'data': data})

@bp.route('/chapter_list')
@login_required
def chapter_list():
    book_id = request.args.get('book_id', 0, int)
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))

    if not book_id:
        return json.dumps({'code': -2, 'msg': u'参数错误'})
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return json.dumps({'code': -1, 'msg': u'无此书籍信息'})
    book_volume = BookVolume.query.filter_by(book_id=book_id).first()
    if book_volume:
        sql = 'select count(*) from book_chapters where book_id=%s and volume_id=%s' %(book_id, book_volume.volume_id)
        book_chapters = BookChapters.query.filter_by(book_id=book_id, volume_id=book_volume.volume_id).paginate(page_no, per_page=num, error_out=False).items
    else:
        sql = 'select count(*) from book_chapters where book_id=%s' %(book_id)
        book_chapters = BookChapters.query.filter_by(book_id=book_id).paginate(page_no, per_page=num, error_out=False).items
    chapters = [ chapter.to_admin_dict() for chapter in book_chapters ]
    total = db.session.execute(sql).scalar() or 0
    return json.dumps({'code':0, 'data': chapters, 'total': total})

@bp.route('/update_chapter_money', methods=['POST', 'GET'])
@login_required
def update_chapter_money():
    _id = request.form.get('id', 0, int) or request.args.get('id', 0, int)
    money = request.form.get('money', 0, int) or request.args.get('money', 0, int) 
    if _id:
        chapter = BookChapters.query.filter_by(id=_id).first()
        if chapter:
            chapter.money = money
            db.session.add(chapter)
            db.session.commit()
            return json.dumps({'code': 0, 'data': chapter.to_admin_dict()})
        else:
            return json.dumps({'code': 1, 'msg': 'chapter is not exist.'})
    else:
        return json.dumps({'code': 1, 'msg': 'id is null.'})

@bp.route('/update_book_chapter_money', methods=['POST', 'GET'])
@login_required
def update_book_chapter_money():
    money = request.form.get('money', 0, int) or request.args.get('money', 0, int) 
    book_id = request.form.get('book_id', 0, int) or request.args.get('book_id', 0, int)
    if not book_id:
        return json.dumps({'code': -2, 'msg': u'参数错误'})
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return json.dumps({'code': -1, 'msg': u'无此书籍信息'})
    book_volume = BookVolume.query.filter_by(book_id=book_id).first()
    if book_volume:
        sql = 'update book_chapters set money=%s where book_id=%s and volume_id=%s' %(money, book_id, book_volume.volume_id)
    else:
        sql = 'update book_chapters set money=%s where book_id=%s' %(money, book_id)
    db.session.execute(sql)
    db.session.commit()
    return json.dumps({'code':0, 'msg': 'ok.'})

@bp.route('/category_list')
@login_required
def category_list():
    page_no = request.args.get("page_no", 1, int)
    num = request.args.get("num", 20, int)
    showed = request.args.get('showed', 0, int)

    sql = 'select count(*) from book_category where 1=1 '
    query = BookCategory.query
    if showed:
        sql += ' and showed=1 '
        query = query.filter_by(showed=1)

    total = db.session.execute(sql).scalar() or 0

    book_categorys = query.paginate(page_no, per_page=num, error_out=False).items
    book_categorys_list = [book_category.to_admin_dict() for book_category in book_categorys]
    return json.dumps({'code':0, 'data': book_categorys_list, 'total': total})

@bp.route('/update_category', methods=['POST', 'GET'])
@login_required
def update_category():
    cate_id = request.form.get('cate_id', 0, int) or request.args.get('cate_id', 0, int)
    icon = request.form.get('icon', '') or request.args.get('icon', '')
    book_cate = BookCategory.query.filter_by(cate_id=cate_id).first()
    if book_cate:
        book_cate.icon = icon
        db.session.add(book_cate)
        db.session.commit()
        return json.dumps({'code': 0, 'data': book_cate.to_admin_dict()})
    else:
        return json.dumps({'code': 1, 'msg': '%s category is not exist.' %(cate_id)})
