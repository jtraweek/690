

import flask
import flask_login
import models



tgeni = flask.Flask(__name__)
tgeni.config['SECRET_KEY'] = 'herp_derp'


login_mgr = flask_login.LoginManager()
login_mgr.login_view = 'sign_in'
login_mgr.init_app(tgeni)


@tgeni.route('/')
@tgeni.route('/hello')
def hello_world():
   return '<h1>Hello, World!</h1>'

@tgeni.route('/home')
@flask_login.login_required
def home():
   return '<h1>Login successful. Welcome!</h1>'


@tgeni.route('/login', methods=['GET', 'POST'])
def sign_in():
   if flask.request.method == 'POST':
      username = flask.request.form['username']
      password = flask.request.form['password']

      user = models.lookup_user(username)

      if user and user.password == password:
         flask_login.login_user(user)
         return flask.redirect(flask.url_for('home'))
      else:
         # username/password invalid
         return flask.abort(401)

   else:
      # render the user login form
      return flask.Response('''
        <form action="" method="post">
            <p><input type=text     name=username placeholder="username"></p>
            <p><input type=password name=password placeholder="password"></p>
            <p><input type=submit   value="Sign In"></p>
        </form>
        ''')


@login_mgr.user_loader
def load_user(username):
   return models.lookup_user(username)


@tgeni.errorhandler(401)
def fail_login(er):
   return '<h2>Login failed.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
   return '<h2>Oh no, 404!</h2>'



if __name__ == '__main__':
   tgeni.run()

