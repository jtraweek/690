import app
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


if __name__ == '__main__':
    unittest.main()
