import os
import unittest

from app import (tgeni, db, crypt, models)


class TestCase(unittest.TestCase):

    def setUp(self):
        tgeni.config['TESTING'] = True
        tgeni.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.sqlite3'
        self.testapp = tgeni.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        test_username = 'New User'
        test_email = 'test@email'
        test_pw = "it's a secret to everyone"
        user = models.User( username = test_username,
                            email    = test_email,
                            password = test_pw)
        db.session.add(user)

        # test lookup
        found_user = models.User.query.filter_by(username=test_username).first()
        self.assertIsNotNone(found_user)
        # test fields
        self.assertEqual(found_user.username, test_username)
        self.assertEqual(found_user.email, test_email)
        self.assertTrue(found_user.password_matches(test_pw))



if __name__ == '__main__':
    unittest.main()
