"""
    This module provides helper functions for the application code.
"""



def get_sorted_activities(trip):
    """ Returns the activities of a trip, sorted by date.
    """
    activities = trip.activities
    if activities:
        sorted_activities = sorted(activities, key=lambda act: act.length)
        return sorted_activities
    else:
        return []
