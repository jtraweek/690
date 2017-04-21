import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TMPDIR  = os.path.join(BASEDIR, 'tmp/')
DBDIR   = TMPDIR

class Config(object):
    # anti-forgery stuff
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'herp_derp'
    # set up password encryption
    BCRYPT_LOG_ROUNDS = 15
    # initialize database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(TMPDIR, 'tgeni.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False   # silence this warning

class TestConfig(Config):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 3
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(TMPDIR, 'tgeni_test.sqlite3')
