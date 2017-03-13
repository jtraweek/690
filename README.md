# SSW-690 Project

## To create the database...
1. At the command prompt: python db_create.py
1. A .sqlite3 file should be created.
1. If the .sqlite3 file already exists, you may have to delete it.
1. TODO: We may want to eventually implement database migration procedures.

## To install the required Python packages...
* At the command prompt: pip install -r requirements.txt

## To run the unit tests...
* At the command prompt: python tests.py

## To run the TGeni app...
1. At the command prompt: python run.py
1. Wait for the server to start up.
1. Open the app in Chrome. (The server runs on 127.0.0.1:5000 by default.)

## Main views:
URL | view
------------ | -------------
/index | main welcome page
/ | redirects to /index
/signin | User sign-in page
/register | New user registration page
/signout | Sign-out current signed-in user
/edittrip | Update Trip page
