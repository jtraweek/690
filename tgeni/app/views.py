import flask
import app.forms    as forms
import app.models   as models
import app.utils.queries as queries

from app   import (tgeni, db, login_manager)
from flask import (Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import (login_required, login_user, logout_user, current_user)



##########################################################################
#
#   login/logout views
#
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
    return redirect(url_for('index'))



##########################################################################
#
#   function to retrieve the current user based on the login
#
@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))



##########################################################################
#
#   error views
#
@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>401 error.</h2>'

@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'



##########################################################################
#
#   user views
#
@tgeni.route('/')
def index_():
    """ This view serves as the homepage for a signed-in user.
    """
    return redirect(url_for('index'))

@tgeni.route('/index')
def index():
    """ This view serves as the homepage for a signed-in user.
    """
    return render_template('index.html')

@tgeni.route('/add_trip', methods = ['GET', 'POST'])
@tgeni.route('/edit_trip/<trip_id>', methods = ['GET', 'POST'])
@login_required
def add_trip(trip_id=None):
    trip = models.Trip.query.get(trip_id) if trip_id else models.Trip()
    activity = models.Activity()
    saved_activities = trip.activities if trip.activities else []
    form = forms.NewTripForm(obj=trip)
    activity_form = forms.NewActivityForm(obj=activity)
    if form.validate_on_submit(): # handles POST?
        form.populate_obj(trip)
        trip.invite(current_user)
        db.session.add(trip)
        db.session.commit()
        return render_template('trip.html', form = form, activity_form=activity_form, saved_activities=saved_activities)
    elif activity_form.validate_on_submit():
        activity.trip_id = trip_id
        activity_form.populate_obj(activity)
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('add_trip', trip_id=trip_id))
    return render_template('trip.html', form=form, activity_form=activity_form, saved_activities=saved_activities)

@tgeni.route('/add_activity', methods = ['GET', 'POST'])
@login_required
def add_activity():
    activity = models.Activity()
    activity_form = forms.NewActivityForm(obj=activity)
    if activity_form.validate_on_submit():
        activity_form.populate_obj(activity)
        db.session.add(activity)
        db.session.commit()
    return render_template('add_activity.html', activity_form = activity_form)

@tgeni.route('/itineraries', methods = ['GET', 'POST'])
@login_required
def itineraries():
    return render_template('itineraries.html')

@tgeni.route('/complete_trip/<trip_id>', methods = ['GET', 'POST'])
@login_required
def complete_trip(trip_id):
    """ Marks the specified trip as "complete" so that it can be viewed at the
        Discover Trip page.
    """
    trip = models.Trip.query.get(trip_id)
    if trip and trip in current_user.trips:
        trip.complete = True
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('itineraries'))
    else:
        return flask.abort(401)

@tgeni.route('/admin/delete/<int:trip_id>', methods=['GET','POST'])
@login_required
def delete_trip(trip_id):
    trip = models.Trip.query.get(trip_id)
    if not trip:
        flask.abort(404)
    if request.method == 'POST':
        db.session.delete(trip)
        db.session.commit()
        flash('Trip was deleted successfully', 'success')
        return redirect(url_for('index.html'))
    return render_template('trip_delete.html', trip_title=trip.title, trip_id=trip_id)

#dmitriy for trip search by location
def search_trip_by_location(location_like):

    trips = queries.search_trip_by_location(location_like)

    if not trips:
        flash('Trips not found', 'success')
         #don't know the real html file for search_trip func
        return redirect(url_for('trip_search.html'))
    else:
        flash('Trips was found successfully', 'success')
    #don't know the real html file for search_trip func
    return render_template('trip_search.html', trips)
