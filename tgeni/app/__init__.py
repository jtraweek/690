import flask
import flask_bcrypt
import flask_login
import flask_sqlalchemy

tgeni = flask.Flask(__name__)
tgeni.config['SECRET_KEY'] = 'herp_derp'

# set up password encryption
tgeni.config['BCRYPT_LOG_ROUNDS'] = 15
crypt = flask_bcrypt.Bcrypt(tgeni)

# initialize database settings
tgeni.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/tgeni.sqlite3'
db = flask_sqlalchemy.SQLAlchemy(tgeni)

# initialize login settings
login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(tgeni)

# expose packages
from app import views, models
