import flask
import flask_sqlalchemy
import flask_login

tgeni = flask.Flask(__name__)
tgeni.config['SECRET_KEY'] = 'herp_derp'

# initialize database settings
tgeni.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/tgeni.sqlite3'
db = flask_sqlalchemy.SQLAlchemy(tgeni)

# initialize login settings
login_manager = flask_login.LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(tgeni)

# expose packages
from app import views, models
