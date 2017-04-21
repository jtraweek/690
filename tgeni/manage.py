import app
import config
import os
import run
import unittest

from coverage           import coverage
from flask_script       import Manager
from flask_migrate      import Migrate, MigrateCommand

migrate = Migrate(app.tgeni, app.db)
manager = Manager(app.tgeni)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    """ Runs the main TGeni application (dev version).
    """
    run.main()


@manager.command
def test():
    """Runs the unit tests.
    """
    tests  = unittest.TestLoader().discover('.', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return 0 if result.wasSuccessful() else 1


@manager.command
def cov():
    """Runs the unit tests with coverage.
    """
    cov_report = coverage(branch=True, include=['app/*', 'app/utils/*'])
    cov_report.start()
    if test() == 0:
        cov_report.stop()
        cov_report.save()
        print('Coverage Report:')
        directory = os.path.join(config.BASEDIR, 'coverage')
        cov_report.report()
        cov_report.html_report(directory=directory)
        cov_report.erase()
        return 0
    else:
        return 1


@manager.command
def db_create():
    """Create the db tables based off the models.
    """
    # create the DB directory if needed
    os.makedirs(config.DBDIR, exist_ok=True)
    # create the DB for the development app
    app.db.create_all()
    print('Development database created in: ' + config.DBDIR)


@manager.command
def db_drop():
    """Drop all db tables. Good to use before creating
    """
    app.db.drop_all()



if __name__ == '__main__':
    manager.run()
