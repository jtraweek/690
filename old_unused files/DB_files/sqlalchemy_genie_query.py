'''
Created on Mar 3, 2017

@author: Default
'''


from sqlalchemy_genie_declarative import UserProfile, UserAddress, UserTrip, TripItiranery, ItiraneryActivity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///travel_genie_4.db',echo=False)

#Base = declarative_base()
#Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

class Query:

    def query_user_profile(self,userid):
        for userprofile in session.query(UserProfile).filter(UserProfile.USER_ID==userid).all():
            #print("UserProfile query ***************")
            #print(userprofile.USER_ID)
            #print(userprofile.USER_ACTIVE)
            return userprofile.USER_ID,userprofile.USER_ACTIVE
        
    def query_tripid_details(self,userid):          
        return [usertrip.__dict__ for usertrip in session.query(UserTrip).filter(userid).all()]
        
    def query_tripid_details_and_tripname(self,userid,tripname):        
        return [usertrip.__dict__ for usertrip in session.query(UserTrip).filter(UserTrip.USER_ID==userid)]
           
    def query_trip_it(self,tripid):        
        return [tripit.__dict__ for tripit in session.query(TripItiranery).filter(tripid).all()]
    
    def query_trip_id_activity(self,activitiid):    
        return [itactivity.__dict__ for itactivity in session.query(ItiraneryActivity).filter(activitiid).all()]