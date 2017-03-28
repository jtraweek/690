import flask
import app.forms    as forms
import app.models   as models

from app   import (tgeni, db, login_manager)
from flask import (Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import (login_required, login_user, logout_user, current_user)

@tgeni.route('/')
def home_():
    return redirect(url_for('home'))

@tgeni.route('/home')
def home():
    return render_template('home.html')



@tgeni.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit(): # handles POST
        user = models.User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('New user registered')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)



@tgeni.route('/signin', methods=['GET', 'POST'])
def signin():
    form = forms.SigninForm()
    if form.validate_on_submit(): # handles POST
        found_user = form.found_user
        if found_user:
            login_user(found_user)
            flash('Logged in user')
            return redirect(url_for('index'))
        else:
            # username/password invalid
            flash('Invalid username or password', 'fail_login')
            return redirect(url_for('signin'))
    return render_template('login.html', form=form)



@tgeni.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('home'))

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
@login_required
def index():
    """ This view serves as the homepage for a signed-in user.
    """
    return render_template('index.html')

@tgeni.route('/add_trip', methods = ['GET', 'POST'])
@tgeni.route('/edit_trip/<trip_id>', methods = ['GET', 'POST'])
@login_required
def add_trip(trip_id=None):
    trip = models.Trip.query.get(trip_id) if trip_id else models.Trip()
    form = forms.NewTripForm(obj=trip)
    if form.validate_on_submit(): # handles POST?
        form.populate_obj(trip)
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_trip.html', form=form)

@tgeni.route('/view_trip', methods = ['GET', 'POST'])
@login_required
def view_trip():
    return render_template('view_trip.html')
