# coding=utf-8

from flask import Blueprint, request
from flask.ext.login import login_required
from models import Banner
from models import db
import json
from lib import utils

bp = Blueprint("other", __name__)

@bp.route('/index')
def index():
    return 'other is ok.'

@bp.route('/banner_list')
@login_required
def banner_list():
    page_no = int(request.args.get("page_no", 1))
    num = int(request.args.get("num", 20))
    page_no = 1
    num = 20
    sql = 'select count(*) from banner'
    total = db.session.execute(sql).scalar() or 0
    banners = Banner.query.paginate(page_no, per_page=num, error_out=False).items
    banner_list = [banner.to_admin_dict() for banner in banners]
    return json.dumps({'code':0, 'data': banner_list, 'total': total})

@bp.route('/add_banner', methods=['POST', 'GET'])
@login_required
def add_banner():
    if request.method == 'GET':
        data = request.args.to_dict()
    else:
        data = request.form.to_dict()
    bn = Banner(data)
    db.session.add(bn)
    db.session.commit()
    return json.dumps({'code': 0, 'data': bn.to_admin_dict()})

@bp.route('/update_banner', methods=['POST', 'GET'])
@login_required
def update_banner():
    _id = request.form.get('id', 0, int) or request.args.get('id', 0, int)
    bn = Banner.query.filter_by(id=_id).first()
    if not bn:
        return json.dumps({'code': 1, 'msg': 'id: %s banner is not exist.' %(_id)})
    if request.method == 'GET':
        data = request.args.to_dict()
    else:
        data = request.form.to_dict()

    bn.update(data)
    db.session.add(bn)
    db.session.commit()
    return json.dumps({'code': 0, 'data': bn.to_admin_dict()})
