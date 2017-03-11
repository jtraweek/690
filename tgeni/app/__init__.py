import config
import flask
import flask_bcrypt
import flask_login
import flask_sqlalchemy

tgeni = flask.Flask(__name__)
tgeni.config.from_object('config.Config')

# set up password encryption
crypt = flask_bcrypt.Bcrypt(tgeni)

# initialize database settings
db = flask_sqlalchemy.SQLAlchemy(tgeni)

# initialize login settings
login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(tgeni)

# expose packages
from app import views, models
