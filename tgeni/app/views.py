import flask
import app.models as models

from app   import (tgeni, db, login_manager)
from flask import (Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import (login_required, login_user, logout_user)
from flask.ext.login import current_user

@tgeni.route('/')
def home():
    return redirect(url_for('index'))

@tgeni.route('/index')
def index():
    return render_template('index.html')

@tgeni.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = models.User(username = request.form['username'],
                        email    = request.form['email'],
                        password = request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('New user registered')
    return redirect(url_for('index'))

@tgeni.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        # render the user login form
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    found_user = models.User.query.filter_by(username=username).first()
    if found_user and found_user.password_matches(password):
        login_user(found_user)
        flash('Logged in user')
        return redirect(url_for('index'))
    else:
        # username/password invalid
        flash('Invalid username or password')
        return redirect(url_for('signin'))

@tgeni.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>Login failed.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'
    
@tgeni.route('/index')
def create_trip():
    if current_user.is_authenticated():
        return redirect(url_for('edit_trip'))
    else:
        return redirect(url_for('register'))

@tgeni.route('/edittrip', methods = ['GET', 'POST'])
def edit_trip():
    if request.method == 'GET':
        return '<h2>Edit trip page.</h2>'
    trip = models.Trip(request.form["trip_name"], request.form["trip_length"])
    db.session.add(trip)
    db.session.commit()
    return '<h2>Edit trip page.</h2>'
