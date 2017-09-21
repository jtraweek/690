
from app        import db
from app.models import User
from test.base  import BaseTestCase


class CRUDMixinTestCase(BaseTestCase):

    def test_create(self):
        test_user = User.create(username='test_user',
                                        email='test_user@email.web',
                                        password='pwd')
        self.assertEqual(test_user.username, 'test_user')
        self.assertEqual(test_user.email, 'test_user@email.web')
        self.assertTrue(test_user.password_matches('pwd'))

    def test_get(self):
        test_user = User.create(username='test_user',
                                        email='test_user@email.web',
                                        password='pwd')
        lookup_user = User.get(test_user.id)
        self.assertIsNotNone(test_user)

    def test_update(self):
        test_user = User.create(username='test_user',
                                        email='test_user@email.web',
                                        password='pwd')
        test_user.update(username='different_name', email='different@email.web')
        self.assertEqual(test_user.username, 'different_name')
        self.assertEqual(test_user.email, 'different@email.web')

    def test_delete(self):
        user_id = 42
        test_user = User.create(
                                id=user_id,
                                username='test_user',
                                email='test_user@email.web',
                                password='pwd')
        self.assertIsNotNone(User.get(user_id))
        test_user.delete()
        self.assertIsNone(User.get(user_id))
