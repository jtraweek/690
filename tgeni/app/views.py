import flask
import flask_login
import app.models as models
from app import tgeni, db, login_manager


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

    user = models.User(username = flask.request.form['username'],
                        email    = flask.request.form['email'],
                        password = flask.request.form['password'])

    db.session.add(user)
    db.session.commit()

    flask.flash('New user registered')
    return flask.redirect(flask.url_for('home'))



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
    found_user = models.User.query.filter_by(username=username,password=password).first()


    if found_user:
        flask_login.login_user(found_user)
        flask.flash('Logged in user')
        return flask.redirect(flask.url_for('home'))
    else:
        # username/password invalid
        flask.flash('Invalid username or password')
        return flask.redirect(flask.url_for('signin'))



@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>Login failed.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'

