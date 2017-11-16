import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    ''' ***The tests are written using the standard unittest package from the python standard library '''
    ''' The setup() and teardown() methods run before and after each test  '''
    ''' any method that have a name starting by test_  are executed as test ****'''
    
    def setUp(self):
        #The setUp() create an application configured for testing
        self.app = create_app('testing')
        # create its context
        self.app_cxt = self.app.app_context()
        #  an activate its context to ensure that tests have access to current_app like regular request
        self.app_cxt.push()
        # then create a brand-new database that the test can use it when necessary
        db.create_all()

    def tearDown(self):
        # notice well that the database and application context are removed
        db.session.remove()
        db.drop_all()
        self.app_cxt.pop()

    def test_app_exists(self):
        # testing if the current application instance exist
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        # testing if the application is running under testing configuration
        self.assertTrue(current_app.config['TESTING'])

