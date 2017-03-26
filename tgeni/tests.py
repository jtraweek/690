import app
import app.models   as models
import os
import unittest
import urllib
import tempfile

from app            import tgeni, db
from flask          import url_for
from flask_testing  import TestCase
from flask_login    import current_user


class BaseTestCase(TestCase):
    """ Some base test case methods to be used for all test cases.
    """
    def create_app(self):
        tgeni.config.from_object('config.TestConfig')
        return tgeni

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class LoginTestCase(BaseTestCase):

    def test_register(self):
        test_username = 'New_User'
        test_email    = 'test@email'
        test_pw       = 'testpw'
        # post the new user
        with self.client:
            self.client.post(url_for("register"),
                             data={"username": test_username,
                                   "email"   : test_email,
                                   "password": test_pw })
        # test lookup
        found_user = models.User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(found_user)
        # test fields
        self.assertEqual(found_user.username, test_username)
        self.assertEqual(found_user.email, test_email)
        self.assertTrue(found_user.password_matches(test_pw))

    def test_signin(self):
          test_username = 'New_User'
          test_email    = 'test@email'
          test_pw       = 'testpw'
          # add a test user
          db.session.add(models.User(username=test_username,
                                     email   =test_email,
                                     password=test_pw))
          # log in
          with self.client:
              response = self.client.post(url_for("signin"),
                               data={"username": test_username,
                                     "password": test_pw })
              self.assert_redirects(response, url_for('index'))
              # test fields
              self.assertEqual(current_user.username, test_username)
              self.assertEqual(current_user.email, test_email)
              self.assertTrue(current_user.password_matches(test_pw))

    def test_signin_invalid_username(self):
          # log in
          with self.client:
              response = self.client.post(url_for("signin"),
                               data={"username": 'Invalid',
                                     "password": 'Invalid' },
                               follow_redirects=True)
              # test fields
              self.assertIn('Invalid username or password', str(response.data))

    def test_signin_invalid_password(self):
          test_username = 'New_User'
          test_email    = 'test@email'
          test_pw       = 'testpw'
          # add a test user
          db.session.add(models.User(username=test_username,
                                     email   =test_email,
                                     password=test_pw))
          # log in
          with self.client:
              response = self.client.post(url_for("signin"),
                               data={"username": 'Invalid',
                                     "password": 'Invalid' },
                               follow_redirects=True)
              # test fields
              self.assertIn('Invalid username or password', str(response.data))




class TestCase(BaseTestCase):


    def test_home(self):
        with self.client:
            response = self.client.get(url_for("home"),
                                        follow_redirects=True)
            # test fields
            self.assertIn('Travel Geni', str(response.data))


    def test_user_trip_data(self):
        # add users to db
        user1 = models.User(username='George', email='user1@mail.web', password='pwd')
        user2 = models.User(username='Dave', email='user2@mail.web', password='pwd')
        user3 = models.User(username='Shelly', email='user3@mail.web', password='pwd')
        user4 = models.User(username='Bart', email='user4@mail.web', password='pwd')
        app.db.session.add(user1)
        app.db.session.add(user2)
        app.db.session.add(user3)
        app.db.session.add(user4)
        app.db.session.commit()
        # add trips to db
        trip1 = models.Trip(title='Empire State Bldg', location='NY', about='Visiting NY', length=2)
        trip2 = models.Trip(title='Disneyworld', location='Orlando FL', about='Visiting the Epcot Center.', length=4)
        app.db.session.add(trip1)
        app.db.session.add(trip2)
        app.db.session.commit()
        # add users to trips
        trip1.users.append(user1)
        trip1.users.append(user3)
        trip1.users.append(user4)
        trip2.users.append(user2)
        trip2.users.append(user4)
        app.db.session.commit()
        # check that users were added to trips
        found_trip_1 = app.models.Trip.query.filter_by(title='Empire State Bldg').first()
        found_trip_2 = app.models.Trip.query.filter_by(title='Disneyworld').first()
        self.assertTrue(user1 in found_trip_1.users)
        self.assertFalse(user2 in found_trip_1.users)
        self.assertTrue(user3 in found_trip_1.users)
        self.assertTrue(user4 in found_trip_1.users)
        self.assertFalse(user1 in found_trip_2.users)
        self.assertTrue(user2 in found_trip_2.users)
        self.assertFalse(user3 in found_trip_2.users)
        self.assertTrue(user4 in found_trip_2.users)
        # check back-references
        self.assertTrue(found_trip_1 in user1.trips)
        self.assertFalse(found_trip_1 in user2.trips)
        self.assertTrue(found_trip_1 in user3.trips)
        self.assertTrue(found_trip_1 in user4.trips)
        self.assertFalse(found_trip_2 in user1.trips)
        self.assertTrue(found_trip_2 in user2.trips)
        self.assertFalse(found_trip_2 in user3.trips)
        self.assertTrue(found_trip_2 in user4.trips)





if __name__ == '__main__':
    unittest.main()
