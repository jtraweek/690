
from app         import db
from app.models  import User, Trip
from flask       import url_for
from flask_login import current_user, AnonymousUserMixin
from test.base   import BaseTestCase


class IndexViewTestCase(BaseTestCase):
    """
    """
    def test_index(self):
        """ Test that the main index page renders.
        """
        response =  self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel Geni', str(response.data))


class RegisterViewTestCase(BaseTestCase):
    """
    """
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
        user = User.query.filter_by(username='test').first()
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


class SigninViewTestCase(BaseTestCase):
    """
    """
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


class EditProfileViewTestCase(BaseTestCase):
    """
    """
    def setUp(self):
        super(EditProfileViewTestCase, self).setUp()
        # Add test users.
        self.user = User.create(
            username='test',
            email='test@email.web',
            password='pwd',
            bio='Some test bio info.')
        # Log in test user
        self.login(self.user.username, self.user.password)

    def test_edit_profile_signin_required(self):
        """ Try to access the page while not logged in.
        """
        self.logout()
        response =  self.client.get('/edit_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sign In', str(response.data))
        self.assertIn('Username', str(response.data))
        self.assertIn('Password', str(response.data))

    # def test_edit_profile_renders(self):
    #     with self.client:
    #         response =  self.client.get('/edit_profile', follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('Edit Profile', str(response.data))
    #         self.assertIn(self.user.username, str(response.data))
    #         self.assertIn(self.user.password, str(response.data))
    #         self.assertIn(self.user.email, str(response.data))
    #         self.assertIn(self.user.bio, str(response.data))


class SignoutViewTestCase(BaseTestCase):
    """
    """
    def test_signout(self):
        """ Test that a user can sign out properly.
        """
        self.register(username='testuser', email='testuser@email.web', password='testpwd')
        with self.client:
            self.login('testuser', 'testpwd')
            response = self.logout()
            self.assertNotIn('testuser', str(response.data))
            self.assertFalse(current_user.is_authenticated)


class ItinerariesViewTestCase(BaseTestCase):
    """
    """
    def setUp(self):
        super(ItinerariesViewTestCase, self).setUp()
        # Add some users.
        self.test_user = User.create(username='testuser', email='testuser@email.web', password='testpwd')
        # Add some trips.
        disney_world = Trip.create(title='Disney World', location='Florida', about='Going to Disney World!', length=7, complete=False, icon='castle')
        carnival     = Trip.create(title='Carnival',  location='Brazil',  about='asdf', length=10, complete=False, icon='city')
        everest      = Trip.create(title='Mt Everest', location='Nepal',  about='climbing Mt Everest', length=8, complete=True, icon='skiing')
        caribbean    = Trip.create(title='Boat Trip',  location='Caribbean', about='Sailing to the caribbean islands', length=14, complete=False, icon='sea')
        self.test_user.trips.extend((disney_world,carnival,everest,caribbean))
        self.test_user.save()
        # Log in test user
        self.login('testuser', 'testpwd')

    def test_itineraries_signin_required(self):
        """ Try to access the page while not logged in.
        """
        self.logout()
        response =  self.client.get('/itineraries', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sign In', str(response.data))
        self.assertIn('Username', str(response.data))
        self.assertIn('Password', str(response.data))

    def test_itineraries_renders(self):
        with self.client:
            response =  self.client.get('/itineraries', follow_redirects=True)
            self.assertIn('Itineraries', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertIn('Carnival', str(response.data))
            self.assertIn('Mt Everest', str(response.data))
            self.assertIn('Boat Trip', str(response.data))

    def test_itineraries_filtered_by_title(self):
        with self.client:
            response =  self.client.get('/itineraries?search=Dis', follow_redirects=True)
            self.assertIn('Itineraries', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertNotIn('Carnival', str(response.data))
            self.assertNotIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))

    def test_itineraries_filtered_by_location(self):
        with self.client:
            response =  self.client.get('/itineraries?search=Flo', follow_redirects=True)
            self.assertIn('Itineraries', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertNotIn('Carnival', str(response.data))
            self.assertNotIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))


class DiscoverTripsViewTestCase(BaseTestCase):
    """
    """
    def setUp(self):
        super(DiscoverTripsViewTestCase, self).setUp()
        # Add some users.
        self.test_user = User.create(username='testuser', email='testuser@email.web', password='testpwd')
        # Add some trips.
        self.disney_world = Trip.create(title='Disney World', location='Florida', about='Going to Disney World!', length=7, complete=True, icon='castle')
        self.carnival     = Trip.create(title='Carnival',  location='Brazil',  about='asdf', length=10, complete=False, icon='city')
        self.everest      = Trip.create(title='Mt Everest', location='Nepal',  about='climbing Mt Everest', length=8, complete=True, icon='skiing')
        self.caribbean    = Trip.create(title='Boat Trip',  location='Caribbean', about='Sailing to the caribbean islands', length=14, complete=False, icon='sea')
        self.test_user.trips.extend((self.disney_world,self.carnival,self.everest,self.caribbean))
        self.test_user.save()
        # Log in test user
        self.login('testuser', 'testpwd')

    def test_discover_trips_signin_required(self):
        """ Try to access the page while not logged in.
        """
        self.logout()
        response =  self.client.get('/discover_trips', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sign In', str(response.data))
        self.assertIn('Username', str(response.data))
        self.assertIn('Password', str(response.data))

    def test_discover_trips_renders(self):
        with self.client:
            response =  self.client.get('/discover_trips', follow_redirects=True)
            self.assertIn('Discover', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertNotIn('Carnival', str(response.data))
            self.assertIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))

    def test_discover_trips_updates(self):
        with self.client:
            self.carnival.update(complete=True)
            response =  self.client.get('/discover_trips', follow_redirects=True)
            self.assertIn('Discover', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertIn('Carnival', str(response.data))
            self.assertIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))

    def test_discover_trips_filtered_by_title(self):
        with self.client:
            response =  self.client.get('/discover_trips?search=ever', follow_redirects=True)
            self.assertIn('Discover', str(response.data))
            self.assertNotIn('Disney World', str(response.data))
            self.assertNotIn('Carnival', str(response.data))
            self.assertIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))

    def test_discover_trips_filtered_by_location(self):
        with self.client:
            response =  self.client.get('/discover_trips?search=flo', follow_redirects=True)
            self.assertIn('Discover', str(response.data))
            self.assertIn('Disney World', str(response.data))
            self.assertNotIn('Carnival', str(response.data))
            self.assertNotIn('Mt Everest', str(response.data))
            self.assertNotIn('Boat Trip', str(response.data))


class ErrorHandlerTestCase(BaseTestCase):
    """ Test HTTP error message pages.
    """
    def test_404(self):
        response =  self.client.get('/nonexistent')
        self.assertIn('Oh no, 404!', str(response.data))
