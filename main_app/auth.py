# coding: utf-8
from flask.ext.login import LoginManager
from models.user import User
from flask import current_app, session
from lib.utils import get_kick_key

login_manager = LoginManager()


class UserInfo(object):
    def __init__(self, admin_id):
        self.id = admin_id

    def __unicode__(self):
        return u'%s' % (self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    kick_key = get_kick_key(user_id)
    # 检测是否是被注销用户
    kick_cache = current_app.redis.get(kick_key)
    print 'KICK======', kick_cache, session['device_id'], type(kick_cache), type(session['device_id'])
    if kick_cache is not None and kick_cache != session['device_id']:
        if 'user_id' in session:
            session.pop('user_id')
        if '_fresh' in session:
            session.pop('_fresh')
        current_app.redis.delete(kick_key)
        print 'kick'
        return None
    user = User.query.get(int(user_id))
    session['device_id'] = user.device_id
    return user
