import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TMPDIR  = os.path.join(BASEDIR, 'tmp/')

os.makedirs(TMPDIR, exist_ok=True)

class Config(object):
    SECRET_KEY = 'herp_derp'
    # set up password encryption
    BCRYPT_LOG_ROUNDS = 15
    # initialize database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(TMPDIR, 'tgeni.sqlite3')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(TMPDIR, 'tgeni_test.sqlite3')
