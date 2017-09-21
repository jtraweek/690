
from app         import tgeni, db
from app.models  import User
from flask       import url_for
from unittest    import TestCase
from flask_login import current_user, AnonymousUserMixin


class BaseTestCase(TestCase):
    """ Some base test case methods to be used for all test cases.
    """
    def setUp(self):
        tgeni.config.from_object('config.TestConfig')
        self.client = tgeni.test_client()
        # Start with a fresh db.
        db.drop_all()
        db.create_all()
        # Ensure we are in testing mode.
        self.assertFalse(tgeni.debug)

    def tearDown(self):
        db.drop_all()

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
