# SSW-690 Project

## To install the required Python packages...
* At the command prompt: pip install -r requirements.txt

## Commands:
* At the command prompt: python manage.py [command], where command is one of the following:

command | function
------------ | -------------
dev | Runs the main TGeni application (development version).
test | Runs the unit tests.
cov | Runs the unit tests and generates a coverage report.
db_create | Creates the db tables based off the models.
db_drop | Drops all db tables. Good to use before creating a new database after changing the models.

## To run the unit tests...
* At the command prompt: python tests.py

## To run the TGeni app...
1. At the command prompt: python run.py
1. Wait for the server to start up.
1. Open the app in Chrome. (The server runs on 127.0.0.1:5000 by default.)

## Main views:
URL | view
------------ | -------------
/home (or just "/) | Welcome page
/signin | User sign-in page
/register | New user registration page
/signout | Sign-out current signed-in user
/index | User main page
/add_trip | Add Trip page
/edit_trip/[trip_id] | Update Trip page
