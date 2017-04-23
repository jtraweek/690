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


@manager.command
def demo():
    """ Runs the main TGeni application (dev version).
    """
    from app.models import (User, Trip, Activity, TripPhoto)
    app.db.drop_all()
    app.db.create_all()
    #
    add = app.db.session.add
    add_all = app.db.session.add_all
    commit = app.db.session.commit
    # Add some users.
    julie = User(username='julie', email='julie@mail.com', password='pwd')
    maryam = User(username='maryam', email='maryam@mail.com', password='pwd')
    william = User(username='william', email='william@mail.com', password='pwd')
    basil = User(username='basil', email='basil@mail.com', password='pwd')
    dmitriy = User(username='dmitriy', email='dmitriy@mail.com', password='pwd')
    aboubacar = User(username='aboubacar', email='aboubacar@mail.com', password='pwd')
    add_all([julie, maryam, william, basil, dmitriy, aboubacar])
    commit()
    # Add some trips.
    disney_world = Trip(title='Disney World', location='Florida', about='Going to Disney World!', length=7, complete=False)
    carnival     = Trip(title='Carnival',  location='Brazil',  about='asdf', length=10, complete=False)
    everest      = Trip(title='Mt Everest', location='Nepal',  about='climbing Mt Everest', length=8, complete=True)
    caribbean    = Trip(title='Boat Trip',  location='Caribbean', about='Sailing to the caribbean islands', length=14, complete=False)
    add_all([disney_world, carnival, everest, caribbean])
    commit()
    # invite travellers.
    disney_world.invite(julie, william, basil)
    carnival.invite(julie, maryam, basil, dmitriy)
    everest.invite(william, aboubacar)
    caribbean.invite(maryam, basil, dmitriy, aboubacar)
    commit()
    # Create activity
    epcot_center = Activity(title='Epcot Center',location='Epcot Center',length='1/10/2017',description='Visit the Epcot Center')
    space_mountain = Activity(title='Space Mountain',location='Disney',length='1/9/2017',description='Ride Space Mountain')
    base_camp = Activity(title='Base Camp',location='Everest',length='6/1/2017',description='camping and prep')
    climbing = Activity(title='Climbing',location='Everest',length='6/5/2017',description='climbing to the top!')
    peak = Activity(title='Peak',location='Everest',length='6/10/2017',description='reached to top!')
    commit()
    # Add activities to trips.
    disney_world.activities.append(epcot_center)
    disney_world.activities.append(space_mountain)
    everest.activities.append(climbing)
    everest.activities.append(base_camp)
    everest.activities.append(peak)
    commit()
    #
    run.main()
    app.db.drop_all()


if __name__ == '__main__':
    manager.run()
