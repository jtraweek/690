from app         import db
from app.models  import User
from flask       import url_for
from flask_login import current_user, AnonymousUserMixin
from test.base   import BaseTestCase


class EditProfileViewTestCase(BaseTestCase):
    """
    """
    def test_edit_profile_signin_required(self):
        """ Try to access the page while not logged in.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            response =  self.client.get('/edit_profile', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sign In', str(response.data))
            self.assertIn('Username', str(response.data))
            self.assertIn('Password', str(response.data))

    def test_edit_profile_renders(self):
        user = dict(
            username='testuser',
            email='testuser@email.web',
            password='testpwd')
        self.register(**user)
        with self.client:
            response = self.login(username=user['username'], password=user['password'])
            response = self.client.get('/edit_profile', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Edit Profile',   str(response.data))
            self.assertIn(user['username'], str(response.data))
            self.assertIn(user['email'],    str(response.data))

    def test_edit_profile_change(self):
        old_data = dict(
            username='testuser',
            email='testuser@email.web',
            password='testpwd')
        new_data = dict(
            username='newuser',
            email='new@email.web',
            bio='new biographical info')
        self.register(**old_data)
        with self.client:
            response = self.login(username=old_data['username'], password=old_data['password'])
            response = self.client.post('/edit_profile',
                                        follow_redirects=True,
                                        data=new_data)
            self.assertIn(new_data['username'], str(response.data))
            self.assertIn(new_data['email'],    str(response.data))
            self.assertIn(new_data['bio'],      str(response.data))
