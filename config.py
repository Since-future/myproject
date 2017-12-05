# coding: utf-8

class BaseConfig:
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    SECRET_KEY = 'CmNDp9oi9uj2OeW2P0E1w932lk'

    CELERY_BROKER = {
        'SMS': 'redis://localhost:6379/3',  # 短信发送队列
    }



    REDIS_SETTINGS = {
        'HOST': '127.0.0.1',
        'PORT': 6379,
        'DB':1,
    }

class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1ji0dfjioi9q3t5uh9dasbaslpg@127.0.0.1/myproject'
    PORT = 6666
    
    LOGGING = {  # 配置日志
    #    'SMTP':{ #邮箱日志发送， 如果没有配置， 则不开启
    #        'HOST': 'smtp.exmail.qq.com',  #smtp 服务器地址
    #        'TOADDRS': ['296779442@qq.com'], #smtp 收件人
    #        'SUBJECT': u'[myproject] error from api', #smtp 主题
    #        'USER': 'xxdebug@pv.cc', #smtp账号
    #        'PASSWORD': 'jNy2dD5QWmxe19Xg', #smtp账号密码
    #    },  
        'FILE':{ #文件日志， 如果没有对应的配置，则不开启
            'PATH':'/root/data/log/myproduct.log',
            'MAX_BYTES': 1024 * 1024 * 10, #单个文件大小默认10M 
            'BACKUP_COUNT': 5, #文件滚动数量，默认5
        }
    }




