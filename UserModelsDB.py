class User(db.Model):
    """ User database model
        Class to hold database records for registered users. This class
        handles password hashing and login functionality.
    """
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String,  unique=True)
    email     = db.Column(db.String,  unique=True)
    _password = db.Column(db.String(128)) # hashed
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)

    def __repr__(self):
        return '<UserCompleteInfo User %r FirstName %r LastName %r>' % (self.username, self.firstname, self.lastname)

    # functionality to hash passwords
    @sqlalchemy.ext.hybrid.hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext_password):
        self._password = crypt.generate_password_hash(plaintext_password)

    def password_matches(self, plaintext_password):
        return crypt.check_password_hash(self._password, plaintext_password)

    # required methods for flask_login...
    ###
    def is_active(self):
        return True
    ###
    def get_id(self):
        return self.id
    
 #   Here I am proposing a change only to database to add extra fields like first name and last name
  
    def sign_out_eq():
	con = sqlite3.connect('users.db')
	cur = con.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,\
	username VARCHAR(100), password VARCHAR(100),\
	firstname VARCHAR(100), lastname VARCHAR(100), \
	hash VARCHAR(100) )')
	
	
	con.commit()
	con.close()
			
