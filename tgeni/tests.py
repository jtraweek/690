import app
import app.models       as models
import os
import unittest
import urllib
import tempfile


class TestCase(unittest.TestCase):
    def setUp(self):
        app.tgeni.config.from_object('config.TestConfig')
        app.db.create_all()
        self.test_client = app.tgeni.test_client()
    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()

    #
    # Unit test cases
    #
    def test_user_creation(self):
        test_username = 'New User'
        test_email = 'test@email'
        test_pw = "it's a secret to everyone"
        user = app.models.User( username = test_username,
                                email    = test_email,
                                password = test_pw)
        app.db.session.add(user)
        # test lookup
        found_user = app.models.User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(found_user)
        # test fields
        self.assertEqual(found_user.username, test_username)
        self.assertEqual(found_user.email, test_email)
        self.assertTrue(found_user.password_matches(test_pw))

    def test_index_template(self):
        # 302 = redirect
        response = self.test_client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Travel Geni' in str(response.data))
        # 200 = OK
        response = self.test_client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Travel Geni' in str(response.data))

    def test_invalid_signin(self):
        # test invalid username
        response = self.test_client.post('/signin',
            data=dict(username='Unregistered', password='1234'),
            follow_redirects=True)
        self.assertTrue('Invalid username or password' in str(response.data))
        # test invalid password
        user = app.models.User( username = 'New User',
                                email    = 'test@email',
                                password = "it's a secret to everyone")
        app.db.session.add(user)
        response = self.test_client.post('/signin',
            data=dict(username='New User', password='1234'),
            follow_redirects=True)
        self.assertTrue('Invalid username or password' in str(response.data))

    def test_register_user(self):
        test_username = 'New User'
        test_email = 'test@email'
        test_pw = "it's a secret to everyone"
        # register new user
        response = self.test_client.post('/register',
            data=dict(username=test_username, email=test_email, password=test_pw),
            follow_redirects=True)
        # test lookup
        found_user = app.models.User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(found_user)
        # test fields
        self.assertEqual(found_user.username, test_username)
        self.assertEqual(found_user.email, test_email)
        self.assertTrue(found_user.password_matches(test_pw))

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
        trip1 = models.Trip(trip_name='New York', trip_length=7)
        trip2 = models.Trip(trip_name='Disneyworld', trip_length=13)
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
        found_trip_1 = app.models.Trip.query.filter_by(trip_name='New York').first()
        found_trip_2 = app.models.Trip.query.filter_by(trip_name='Disneyworld').first()
        self.assertTrue(user1 in found_trip_1.users)
        self.assertFalse(user2 in found_trip_1.users)
        self.assertTrue(user3 in found_trip_1.users)
        self.assertTrue(user4 in found_trip_1.users)
        self.assertFalse(user1 in found_trip_2.users)
        self.assertTrue(user2 in found_trip_2.users)
        self.assertFalse(user3 in found_trip_2.users)
        self.assertTrue(user4 in found_trip_2.users)





if __name__ == '__main__':
    unittest.main()
