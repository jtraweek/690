import app
import app.models   as models
import os
import unittest
import urllib
import tempfile

from app            import tgeni, db
from flask          import url_for
from unittest       import TestCase
from flask_login    import current_user, AnonymousUserMixin


class BaseTestCase(TestCase):
    """ Some base test case methods to be used for all test cases.
    """
    def setUp(self):
        tgeni.config.from_object('config.TestConfig')
        self.client = tgeni.test_client()
        db.drop_all()
        db.create_all()
        # Start with a fresh db.
        db.drop_all()
        db.create_all()
        # Ensure we are in testing mode.
        self.assertFalse(tgeni.debug)

    def tearDown(self):
        pass

    #=============================================
    #   Some helper functions
    #
    def register(self, username, email, password):
        return self.client.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
            )

    def login(self, username, password):
        return self.client.post(
            '/signin',
            data=dict(username=username, password=password),
            follow_redirects=True
            )

    def logout(self):
        return self.client.get(
            '/signout',
            follow_redirects=True
            )
    #=============================================




class ViewTestCase(BaseTestCase):

    def test_index(self):
        """ Test that the main index page renders.
        """
        response =  self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel Geni', str(response.data))

    def test_register(self):
        """ Test that a valid registration works.
        """
        response = self.register(username='test', email='testuser@email.web', password='testpwd')
        self.assertEqual(response.status_code, 200)
        user = models.User.query.filter_by(username='test').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'testuser@email.web')
        self.assertTrue(user.password_matches('testpwd'))

    def test_signin(self):
        """ Test that a user can sign in with valid credentials.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            response = self.login('testuser', 'testpwd')
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', str(response.data))
            self.assertTrue(current_user.is_authenticated)

    def test_signout(self):
        """ Test that a user can sign out properly.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            self.login('testuser', 'testpwd')
            response = self.logout()
            self.assertNotIn('testuser', str(response.data))
            self.assertFalse(current_user.is_authenticated)



if __name__ == '__main__':
    unittest.main()
