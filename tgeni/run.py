

import flask
import flask_sqlalchemy
import flask_login



tgeni = flask.Flask(__name__)
tgeni.config['SECRET_KEY'] = 'herp_derp'

# initialize database settings
tgeni.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tgeni.sqlite3'
db = flask_sqlalchemy.SQLAlchemy(tgeni)

# initialize login settings
login_mgr = flask_login.LoginManager()
login_mgr.login_view = 'signin'
login_mgr.init_app(tgeni)



class User(db.Model, flask_login.UserMixin):
    id       = db.Column(db.Integer,    primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email    = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, username, email, password):
        self.username = username
        self.email    = email
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % (self.username)

    # required methods for flask_login...
        
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id
 
        
        
@tgeni.route('/')
@flask_login.login_required
def home():
    return '<h1>Welcome User!</h1>'


@tgeni.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.Response('''
            <h1>Please enter your registration credentials:</h1>
            <form action="" method="post">
                <p><input type=text      name=username placeholder="username"></p>
                <p><input type=text      name=email    placeholder="email"></p>
                <p><input type=password  name=password placeholder="password"></p>
                <p><input type=submit    value="Register"></p>
            </form>
            ''')

    user = User(username = flask.request.form['username'],
                email    = flask.request.form['email'],
                password = flask.request.form['password'])
                
    db.session.add(user)
    db.session.commit()
    
    flask.flash('New user registered')
    return  flask.redirect(flask.url_for('home'))



@tgeni.route('/signin', methods=['GET', 'POST'])
def signin():
    if flask.request.method == 'GET':
        # render the user login form
        return flask.Response('''
            <h1>Please enter your login credentials:</h1>
            <form action="" method="post">
                <p><input type=text      name=username placeholder="username"></p>
                <p><input type=password  name=password placeholder="password"></p>
                <p><input type=submit    value="Sign In"></p>
            </form>
            ''')

    username = flask.request.form['username']
    password = flask.request.form['password']
    found_user = User.query.filter_by(username=username,password=password).first()
    

    if found_user:    
        flask_login.login_user(found_user)
        flask.flash('Logged in user')
        return flask.redirect(flask.url_for('home'))
    else:
        # username/password invalid
        flask.flash('Invalid username or password')
        return flask.redirect(flask.url_for('signin'))



@login_mgr.user_loader
def load_user(id):
    return User.query.get(int(id))


@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>Login failed.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'



if __name__ == '__main__':
    tgeni.run(debug=True)

