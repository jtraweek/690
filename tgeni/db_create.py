import app
import config
import os

# create the DB directory if needed
os.makedirs(config.DBDIR, exist_ok=True)

# create the DB for the development app
app.db.create_all()
print('development database created in ' + config.DBDIR)
