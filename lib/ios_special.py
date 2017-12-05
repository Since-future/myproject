#coding:utf8

from flask import current_app, request

def is_ios_special():
    m_id = request.args.get('m_id', 0, int)
    if m_id == 1:
        return request.args.get('platform') == 'ios' and request.args.get('v') in ['1.0.0']
    if m_id == 2:
        return request.args.get('platform') == 'ios' and request.args.get('v') in ['1.0.2']
    return request.args.get('platform') == 'ios' and request.args.get('v') in ['1.0.5'] # and request.args.get('is_appstore') == '1'
