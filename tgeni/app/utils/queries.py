import app
import app.models       as models

from app import db

#dmitriy for trip search by location
def search_trip_by_location(location_like):
    """ This function searches for trips that _partially_ match the passed-in
        string, based on trip title.
    """

    sz_like="%"+location_like+"%"

    trips = models.Trip.query.filter(models.Trip.location.ilike(sz_like)).all()

    return trips


def get_sorted_activities(trip):
    """ Returns the activities of a trip, sorted by date.
    """
    activities = trip.activities
    if activities:
        sorted_activities = sorted(activities, key=lambda act: act.length)
        return sorted_activities
    else:
        return []
