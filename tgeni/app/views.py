
import flask
import os
import re
import uuid

import app.forms            as forms
import app.models           as models
import app.utils.queries    as queries

from   app                  import (tgeni, db, login_manager, uploaded_photos)
from   flask                import (Response, flash, redirect, render_template,
                                    request, url_for)
from   flask_login          import (login_required, login_user, logout_user,
                                    current_user)


@tgeni.route('/')
def index():
    """ This view serves as the homepage for a signed-in user.
    """
    return render_template('index.html')


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
        login_user(found_user)
        flash('Logged in user')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@tgeni.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))


@tgeni.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    if not user:
        return abort(404)

    form = forms.UpdateProfileForm(obj=user)
    if form.validate_on_submit():
        user.update(**form.data)
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html', form=form)


@tgeni.route('/itineraries', methods = ['GET', 'POST'])
@login_required
def itineraries():
    """ Displays all trips a user has created.
    """
    return _render_itineraries('itineraries',
                                get_trips= lambda: current_user.trips)


@tgeni.route('/discover_trips', methods = ['GET', 'POST'])
@login_required
def discover_trips():
    """Displays all trips that are marked complete. Allows filter by location.
    """
    return _render_itineraries('discover_trips',
                                get_trips= lambda: models.Trip.query.filter_by(complete=True))


@tgeni.route('/trip', methods = ['GET', 'POST'])
@tgeni.route('/trip/<trip_id>', methods = ['GET', 'POST'])
@login_required
def add_trip(trip_id=None):

    user = current_user

    if trip_id:
        trip = models.Trip.get(trip_id)
        if trip and trip in user.trips:
            new_trip = False
        else:
            return flask.abort(401)
    else:
        trip = models.Trip()
        new_trip = True

    trip.icon = trip.icon or 'original'
    form = forms.NewTripForm(obj=trip)

    if form.validate_on_submit(): # handles POST?
        form.populate_obj(trip)
        trip.icon = request.form['icon_choice'] or 'original'
        trip.invite(user)
        trip.save()
        return redirect(url_for('add_trip', trip_id=trip.trip_id))

    return render_template('trip.html',
                            form=form,
                            trip=trip,
                            new_trip=new_trip)


@tgeni.route('/trip/<trip_id>/add_activity', methods = ['GET', 'POST'])
@tgeni.route('/trip/<trip_id>/add_activity/<activity_id>', methods = ['GET', 'POST'])
@login_required
def add_activity(trip_id, activity_id=None):
    if trip_id is None:
        return flask.abort(401)

    if trip_id:
        trip = models.Trip.query.get(trip_id)
        if not trip or trip not in current_user.trips:
            return flask.abort(401)

    if activity_id:
        activity = models.Activity.query.get(activity_id)
        if activity and activity in current_user.activities:
            new_activity = False
        else:
            return flask.abort(401)
    else:
        activity = models.Activity()
        new_activity = True

    trip.icon = trip.icon or 'original'
    activity = models.Activity()
    ####------------------------------------------
    activity_form = forms.NewActivityForm(obj=activity)
    ####------------------------------------------
    if activity_form.validate_on_submit():
        activity_form.populate_obj(activity)
        db.session.add(activity)
        trip.activities.append(activity)
        db.session.commit()
        return redirect(url_for('add_activity',
                                    trip_id=trip_id,
                                    activity_id=None,
                                    new_trip=False))
    ####------------------------------------------
    return render_template('activity.html',
                            activity_form=activity_form,
                            trip=trip,
                            activity=activity,
                            new_activity=new_activity)


@tgeni.route('/trip/<trip_id>/photos', methods=['GET', 'POST'])
@login_required
def upload_photos(trip_id):

    trip = models.Trip.get(trip_id)
    user = current_user
    if user and trip and (trip in user.trips):
        pass # test that current_user is on trip
    else:
        return flask.abort(404)

    form = forms.TripPhotoUploadForm()
    if form.validate_on_submit():
        for photo in request.files.getlist('photo'):
            extension = os.path.splitext(photo.filename)[-1]
            filename = str(uuid.uuid4()) + extension  # generate a filename
            uploaded_photos.save(photo, name=filename)
            models.TripPhoto.create(filepath=filename, trip_id=trip.trip_id, trip=trip)
        return redirect(url_for('upload_photos', trip_id=trip_id))

    photo_filenames = [photo.filepath for photo in trip.photos]

    return render_template('upload_photos.html',
                            form=form,
                            trip=trip,
                            photo_filenames=photo_filenames)


@tgeni.route('/view_complete_trip/<trip_id>')
@login_required
def view_complete_trip(trip_id):
    """Displays information for a trip that has been marked complete
    """
    trip = models.Trip.query.get(trip_id)
    form = forms.NewTripForm(obj=trip)
    saved_activities = queries.get_sorted_activities(trip)
    return render_template('view_complete_trip.html', trip = trip, form = form, saved_activities = saved_activities)


@tgeni.route('/delete_trip/<trip_id>', methods=['GET','POST'])
@login_required
def delete_trip(trip_id):
    """Deletes trip from database
    """
    if not trip:
        flask.abort(404)
    else:
        win=app.utils.PopUp.Confirm(self.delete_tripid)
        win.mainloop()
    return redirect(url_for('itineraries'))

def delete_tripid(trip_id):
      trip = models.Trip.query.get(trip_id)
      db.session.delete(trip)
      db.session.commit()

@tgeni.route('/delete_activity/<activity_id>', methods = ['GET', 'POST'])
@login_required
def delete_activity(activity_id):
    """Deletes activity from database
    """
    if not activity:
        flask.abort(404)
    else:
         win=app.utils.PopUp.Confirm(self.delete_activityid)
         win.mainloop()
    return redirect('/edit_trip/')

def delete_activityid(activity_id):
    activity = models.Activity.query.get(activity_id)
    db.session.delete(activity)
    db.session.commit()

@tgeni.errorhandler(401)
def fail_login(er):
    return '<h2>401 error.</h2>'


@tgeni.errorhandler(404)
def not_found_404(er):
    return '<h2>Oh no, 404!</h2>'


@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))


def _render_itineraries(route_name, get_trips):
    """ Executes common logic for itinerary-related pages.
    """
    form = forms.SearchLocationForm()
    if form.validate_on_submit():
        search_filter = form.location_search.data
        return redirect(url_for(route_name, search=search_filter))
    else:
        unfiltered_trips = get_trips()
        # filter
        search_filter = request.args.get('search', '')
        if search_filter:
            unsorted_trips = \
                [tr for tr in unfiltered_trips
                     if re.search(search_filter, tr.location, re.IGNORECASE)
                        or
                        re.search(search_filter, tr.title, re.IGNORECASE)]
        else:
            unsorted_trips = unfiltered_trips
        # sort
        sortfunc_lookup = {
            'newest'  : (lambda ts: sorted(ts, key=lambda t: t.length, reverse=True)),
            'oldest'  : (lambda ts: sorted(ts, key=lambda t: t.length)),
            'location': (lambda ts: sorted(ts, key=lambda t: t.location))
        }
        #---------------------------------------
        sort_field = request.args.get('sort', '')
        sortfunc = sortfunc_lookup.get(sort_field, lambda ts: ts)
        trips = sortfunc(unsorted_trips)
        return render_template(route_name+'.html', trips=trips, form=form)


###########################################################################
#
#    Functions to be integrated
#
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

def add_number_of_likes_to_trip(trip_id):
    queries.add_number_of_likes_to_trip(trip_id)

def get_number_of_likes_for_trip(trip_id):
    return queries.get_number_of_likes_for_trip()
