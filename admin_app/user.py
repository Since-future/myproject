# coding=utf-8

from flask import Blueprint, request
from flask.ext.login import login_required, current_user
from models import User, UserBalanceLog
from models import db
from models import Book 
import json
from lib import utils
from datetime import datetime, timedelta

bp = Blueprint("user", __name__)

@bp.route('/index')
def index():
    return 'user is ok.'

@bp.route('/list')
@login_required
def list():
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))
    sql = 'select count(*) from user'
    total = db.session.execute(sql).scalar() or 0
    users = User.query.order_by(User.created.desc()).paginate(page_no, per_page=num, error_out=False).items
    user_list = [user.to_admin_dict() for user in users]
    return json.dumps({'code':0, 'data': user_list, 'total': total})

@bp.route('/search')
@login_required
def search():
    user_id = request.args.get('user_id', 0, int)
    phone = request.args.get('phone', 0, int)
    if user_id:
        user = User.query.filter_by(id=user_id).first()
    elif phone:
        user = User.query.filter_by(phone=phone).first()
    else:
        user = None
    if user:
        data = user.to_admin_dict()
    else:
        data = {}
    return json.dumps({'code':0, 'data': data})

def get_sina_buy_list(source, page_no, num):
    today = datetime.today()
    begin = request.args.get('begin', today.strftime('%Y-%m-%d'))
    end = request.args.get('end', today.strftime('%Y-%m-%d'))
    end = (datetime.strptime(end, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')

    books = Book.query.filter_by(source=source).all()
    book_ids = tuple([int(book.book_id) for book in books])
    sql = 'select count(*) from user_balance_log where exec_type=2 and remark="buy book" \
            and book_id in %s and created_time between "%s" and "%s"' %(str(book_ids), begin, end)
    total = int(db.session.execute(sql).scalar() or 0)

    ios_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" \
            and book_id in %s and created_time between "%s" and "%s" and platform="ios"'\
            %(str(book_ids), begin, end)
    ios_money = int(db.session.execute(ios_money_sql).scalar() or 0)

    total_ios_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" \
            and book_id in %s and platform="ios"'\
            %(str(book_ids))
    total_ios_money = int(db.session.execute(total_ios_money_sql).scalar() or 0)

    android_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" \
            and book_id in %s and created_time between "%s" and "%s" and platform="android"'\
            %(str(book_ids), begin, end)
    android_money = int(db.session.execute(android_money_sql).scalar() or 0)

    total_android_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" \
            and book_id in %s and platform="android"'\
            %(str(book_ids))
    total_android_money = int(db.session.execute(total_android_money_sql).scalar() or 0)

    logs = UserBalanceLog.query.filter(UserBalanceLog.exec_type==2, 
                                       UserBalanceLog.remark=='buy book',
                                       UserBalanceLog.book_id.in_(book_ids),
                                       UserBalanceLog.created_time.between(begin, end)).order_by(UserBalanceLog.created_time.desc()).paginate(page_no, per_page=num, error_out=False).items
    log_list = [log.to_admin_dict() for log in logs]

    return json.dumps({'code': 0, 'data': log_list, 'total': total, 'ios_money': ios_money, 'total_ios_money': total_ios_money, 'android_money': android_money, 'total_android_money': total_android_money})

@bp.route('/buy_list')
@login_required
def buy_list():
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))
    user_id = request.args.get('user_id', 0, int)
    source = request.args.get('source', '')

    today = datetime.today()
    begin = request.args.get('begin', today.strftime('%Y-%m-%d'))
    end = request.args.get('end', today.strftime('%Y-%m-%d'))
    end = (datetime.strptime(end, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')

    if current_user.email == 'sina':
        return get_sina_buy_list('sina', page_no, num)
    elif current_user.email == 'kaixing':
        return get_sina_buy_list('kaixing', page_no, num)
    elif current_user.email == 'jingyu':
        return get_sina_buy_list('jingyu', page_no, num)

    sql = 'select count(*) from user_balance_log where exec_type=2 and remark="buy book" '
    logs = UserBalanceLog.query.filter_by(exec_type=2, remark='buy book')

    total_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" '
    ios_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" and platform="ios" '
    android_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" and platform="android" '
    applet_money_sql = 'select sum(money) from user_balance_log where exec_type=2 and remark="buy book" and platform="applet" '
    if user_id:
        sql += 'and user_id=%s ' %(user_id)
        total_money_sql += 'and user_id=%s ' %(user_id)
        ios_money_sql += 'and user_id=%s ' %(user_id)
        android_money_sql += 'and user_id=%s ' %(user_id)
        applet_money_sql += 'and user_id=%s ' %(user_id)
        logs = logs.filter_by(user_id=user_id)
    if source:
        books = Book.query.filter_by(source=source).all()
        book_ids = tuple([int(book.book_id) for book in books])
        if not book_ids:
            book_ids = (-1, -2)
        sql += 'and book_id in %s ' %(str(book_ids))
        total_money_sql += 'and book_id in %s ' %(str(book_ids))
        ios_money_sql += 'and book_id in %s ' %(str(book_ids))
        android_money_sql += 'and book_id in %s ' %(str(book_ids))
        applet_money_sql += 'and book_id in %s ' %(str(book_ids))
        logs = logs.filter(UserBalanceLog.book_id.in_(book_ids))


    sql += ' and created_time between "%s" and "%s"' %(begin, end)
    total_money_sql += ' and created_time between "%s" and "%s"' %(begin, end)
    ios_money_sql += ' and created_time between "%s" and "%s"' %(begin, end)
    android_money_sql += ' and created_time between "%s" and "%s"' %(begin, end)
    applet_money_sql += ' and created_time between "%s" and "%s"' %(begin, end)

    logs = logs.filter(UserBalanceLog.created_time.between(begin, end))
    logs = logs.order_by(UserBalanceLog.created_time.desc()).paginate(page_no, per_page=num, error_out=False).items

    print sql
    total = int(db.session.execute(sql).scalar() or 0)
    total_money = int(db.session.execute(total_money_sql).scalar() or 0)
    ios_money = int(db.session.execute(ios_money_sql).scalar() or 0)
    android_money = int(db.session.execute(android_money_sql).scalar() or 0)
    applet_money = int(db.session.execute(applet_money_sql).scalar() or 0)

    log_list = [log.to_admin_dict() for log in logs]
    return json.dumps({'code':0, 'data': log_list, 'total': total, 'total_money': total_money, 'ios_money': ios_money, 'android_money': android_money, 'applet_money': applet_money})

@bp.route('/recharge_list')
@login_required
def recharge_list():
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))
    user_id = request.args.get('user_id', 0, int)
    today = datetime.today()
    begin = request.args.get('begin', today.strftime('%Y-%m-%d'))
    end = request.args.get('end', today.strftime('%Y-%m-%d'))
    end = (datetime.strptime(end, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')

    sql = 'select count(*) from user_balance_log where exec_type=1 and remark="recharge" '
    logs = UserBalanceLog.query.filter_by(exec_type=1, remark='recharge')
    if user_id:
        sql += 'and user_id=%s ' %(user_id)
        logs = logs.filter_by(user_id=user_id)

    sql += 'and created_time between "%s" and "%s" ' %(begin, end)
    logs = logs.filter(UserBalanceLog.created_time.between(begin, end))

    total = db.session.execute(sql).scalar() or 0
    logs = logs.order_by(UserBalanceLog.created_time.desc()).paginate(page_no, per_page=num, error_out=False).items
    log_list = [log.to_admin_dict() for log in logs]
    return json.dumps({'code':0, 'data': log_list, 'total': total})
