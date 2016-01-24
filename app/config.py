import os

root = os.path.abspath(os.path.dirname(__file__))

class Config:
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = '\\\xbcB\x01\xf7\x8b\x16\xb6:\xe7\xf8\x0bt\x9b\x8c\x9bF\x04\x00|\x05Xk3'
    WTF_CSRF_SECRET_KEY = 'a.\xdc\x95n\xbe&\xe4`\x94N\x1b\x18\xab\x1d\x827\x1f7\x9b\x15(Q\xbc'

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/florian/_/_development/git/projects/gabriel-cms/dev.db'

class Production(Config):
    DEBUG = False
    SECRET_KEY = '\xfb}\xc9v\n\x81\xa3U\x8f\x9cN\xb7n\xe7\xdf\x1et\xdc\x86\xe30\x0f\xc6\x13'
    WTF_CSRF_SECRET_KEY = '\xe8\x7f\x86\x1a\x93Uur~\x89\xa0\xda\xc9\x0c0t6\x9e\xd1\x197\x10m='
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/florian/_/_development/git/projects/gabriel-cms/prod.db'

config = {'development': Development,
          'production': Production,
          'default': Config}