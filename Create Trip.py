# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 00:12:41 2017

@author: Julie

All url routes, .html templates, and database variable names are open for change in order
to integrate the function properly into the site.

"""
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

tgeni = Flask(__name__)
#need to set up configuration for database uri and add config string
db = SQLAlchemy(tgeni)

#Create class for trips
class Trip(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    trip_name = db.Column(db.String)
    trip_length = db.Colum(db.Integer)
    
    def __init__(self, trip_name, trip_length):
        self.trip_name = trip_name
        self.trip_length = trip_length
        
    def __repr__(self):
        return "User %s" % self.trip_name
"""
 If user is logged in, their username should be passed to the new trip index page (which may be the homepage). This 
 will allow us to easily check if someone is logged when they try and create a new trip.
"""
@tgeni.route("/new_trip/<username>")                                                     
def new_trip_index(username = None):
    if username != None:
        return render_template("new_trip.html")                                 #If user is logged in, render the form template
    else:
        return redirect(url_for("new_user"))                                    #If user is not logged in, direct them to the new user page

@tgeni.route("/create_new_trip", methods = ["POST"])
def create_new_trip():
    trip = Trip(request.form["trip_name"], request.form["trip_length"])
    db.session.add(trip)
    db.session.commit()
    return redirect(url_for("trip_page"))                                       #If database addition is successful, route to the new trip's Intinerary page
    
if __name__ == "__main__":
    tgeni.run()