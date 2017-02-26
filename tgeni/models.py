

from flask_login import UserMixin



class User(UserMixin):
	
   def __init__(self, username, password):
      self.username = username
      self.password = password

   def is_active(self):
      return True

   def get_id(self):
      return self.username

   def is_anonymous(self):
      return False
      
       

def lookup_user(username):

   users = [
      ('Bill', 'bpwd'),
      ('Julie', 'jpwd'),
      ('Abu', 'jpwd'),
      ('Basil', 'jpwd'),
      ('Maryam', 'jpwd'),
      ('Dmitriy', 'jpwd'),
   ]   

   mock_database = {
      username_ : User(username_, password) 
         for (username_, password) in users
   }
   
   return mock_database.get(username)
   
   
        