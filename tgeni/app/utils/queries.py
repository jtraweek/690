"""
    This module provides helper functions for common database queries.
"""
import app
import app.models       as models
from   app              import db
from   flask_login      import current_user
from   sqlalchemy       import (desc, asc)



#dmitriy for trip search by location
def search_trip_by_location(location_like):
    """ This function searches for trips that _partially_ match the passed-in
        string, based on trip title.
    """
    sz_like="%"+location_like+"%"
    return current_user.trips.location.ilike(sz_like)



def get_sorted_activities(trip):
    """ Returns the activities of a trip, sorted by date.
    """
    activities = trip.activities
    if activities:
        sorted_activities = sorted(activities, key=lambda act: act.length)
        return sorted_activities
    else:
        return []



def current_user_trips_sorted(descending=False):
    """ Retrieves the trips the current logged-in user is invited to, ordered
        by location (specified as ascending or descending).
    """
    sort_func = desc if descending else asc
    return current_user.trips.order_by(sort_func(models.Trip.location))
