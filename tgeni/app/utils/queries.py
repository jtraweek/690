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
