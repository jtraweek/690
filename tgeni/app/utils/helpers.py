"""
    This module provides helper functions for the application code.
"""
import os
import uuid


def generate_filename(filename):
    """
    Generate a random filename.
    """
    extension = os.path.splitext(filename)[-1].lower()
    result = str(uuid.uuid4()) + extension
    return result


def get_sorted_activities(trip):
    """ Returns the activities of a trip, sorted by date.
    """
    activities = trip.activities
    if activities:
        sorted_activities = sorted(activities, key=lambda act: act.length)
        return sorted_activities
    else:
        return []
