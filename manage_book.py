# coding=utf-8

from flask_script import Manager

from wsgi_api import app

manager = Manager(app)


@manager.command
def book():
    # 逻辑导入部分开始
    from script import book
    book.start()


@manager.option('-c', '--channel', dest='channel', default='')
def update_book(channel):
    import datetime
    print 'Start:', datetime.datetime.now()
    from script.base_book import BookUpdater
    channel = channel.lower()
    channel_class = getattr(getattr(__import__('script.%s_book' % channel), '%s_book' % channel), '%sBookSpider' % channel.capitalize())
    if not channel_class:
        print 'book channel not exist!'
        return
    updater = BookUpdater(channel_class)
    updater.pull_book()
    print 'End:', datetime.datetime.now()


@manager.command
def update_sina_book():
    from script import update_book
    update_book.start()


@manager.command
def update_kaixing_book():
    from script import kaixing_book
    import datetime
    print 'Start:', datetime.datetime.now()
    kaixing_book.pull_book()
    print 'End:', datetime.datetime.now()


@manager.command
def update_anzhi_book():
    from script import anzhi_book
    import datetime
    print 'Start:', datetime.datetime.now()
    anzhi_book.pull_book()


@manager.command
def update_jingyu_book():
    import datetime
    print 'Start:', datetime.datetime.now()
    from script import jingyu_book
    jingyu_book.pull_book()
    print 'End:', datetime.datetime.now()


@manager.command
def update_category():
    import datetime
    print 'Start:', datetime.datetime.now()
    from script import update_category
    update_category.update_book_category()
    print 'End:', datetime.datetime.now()


@manager.command
def update_book_cover():
    """更新书籍封面为七牛地址"""
    from models import db
    from lib.utils import upload_img_by_url
    query = db.session.execute('select cover, book_id from book').fetchall()
    update_list = []
    for book in query:
        if book.cover.startswith('http://ov2eyt2uw.bkt.clouddn.com'):
            continue
        new_cover = upload_img_by_url('book_cover_%s' % book.book_id, book.cover)
        print book, new_cover
        if new_cover != book.cover:
            update_list.append({'book_id': book.book_id, 'cover': new_cover})
    db.session.execute('update book set cover=:cover where book_id=:book_id', update_list)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
