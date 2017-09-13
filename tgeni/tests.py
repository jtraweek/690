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

    def test_register_renders(self):
        response =  self.client.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Register', str(response.data))
        self.assertIn('Sign Up', str(response.data))

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

    def test_register_username_taken(self):
         self.register(username='test', email='testuser@email.web', password='testpwd')
         response = self.register(username='test', email='testuser@email.web', password='testpwd')
         self.assertIn('Username already take', str(response.data))

    def test_register_missing_input(self):
        """ Test register with required fields left blank.
        """
        response = self.register(username='', email='testuser@email.web', password='testpwd')
        self.assertIn('This field is required.', str(response.data))
        response = self.register(username='test', email='', password='testpwd')
        self.assertIn('This field is required.', str(response.data))
        response = self.register(username='test', email='testuser@email.web', password='')
        self.assertIn('This field is required.', str(response.data))

    def test_register_missing_input(self):
        response = self.register(username='test', email='invalidemail', password='testpwd')
        self.assertIn('Invalid email address.', str(response.data))

    def test_signin_renders(self):
        response =  self.client.get('/signin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sign In', str(response.data))
        self.assertIn('Username', str(response.data))
        self.assertIn('Password', str(response.data))

    def test_signin(self):
        """ Test that a user can sign in with valid credentials.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            response = self.login('testuser', 'testpwd')
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', str(response.data))
            self.assertTrue(current_user.is_authenticated)

    def test_signin_invalid_username(self):
        """ Test signin with a nonexistent user.
        """
        with self.client:
            response = self.login('testuser', 'testpwd')
            self.assertIn('Invalid username or password', str(response.data))
            self.assertFalse(current_user.is_authenticated)

    def test_signin_invalid_password(self):
        """ Test signin with mismatched password.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            response = self.login('testuser', 'wrongpwd')
            self.assertIn('Invalid username or password', str(response.data))
            self.assertFalse(current_user.is_authenticated)

    def test_signin_missing_input(self):
        """ Test signin with required fields left blank.
        """
        with self.client:
            response = self.login('', '')
            self.assertIn('This field is required.', str(response.data))
            self.assertFalse(current_user.is_authenticated)
            response = self.login('provided', '')
            self.assertIn('This field is required.', str(response.data))
            self.assertFalse(current_user.is_authenticated)
            response = self.login('', 'provided')
            self.assertIn('This field is required.', str(response.data))
            self.assertFalse(current_user.is_authenticated)

    def test_signout(self):
        """ Test that a user can sign out properly.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            self.login('testuser', 'testpwd')
            response = self.logout()
            self.assertNotIn('testuser', str(response.data))
            self.assertFalse(current_user.is_authenticated)



class ErrorHandlerTestCase(BaseTestCase):

    def test_404(self):
        response =  self.client.get('/nonexistent')
        self.assertIn('Oh no, 404!', str(response.data))



if __name__ == '__main__':
    unittest.main()
