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

def query_user_profile(userid):
    for userprofile in session.query(UserProfile).filter(UserProfile.USER_ID==userid).all():
        #print("UserProfile query ***************")
        #print(userprofile.USER_ID)
        #print(userprofile.USER_ACTIVE)
        return userprofile.USER_ID,userprofile.USER_ACTIVE
    
def query_tripid_details(userid):    
    for usertrip in session.query(UserTrip).filter(userid).all():
        #print("UserTrip query ***************")
        #print(usertrip.USER_ID)
        #print(usertrip.TRIP_ID)
        #print(usertrip.TRIP_NAME)
        #print(usertrip.TRIP_DESCRIPTION)
        return usertrip.dict

def query_trip_it(tripid): 
    global tripit   
    for tripit in session.query(TripItiranery).filter(tripid).all():
        #print("TripItiranery query ***************")
        #print(tripit.TRIP_ID)
        #print(tripit.ITIRENERY_ID)
        #print(tripit.ACTIVITY_ID)
        #return tripit.dict
        return tripit.dict

def query_trip_id_activity(activitiid):   
    for itactivity in session.query(ItiraneryActivity).filter(activitiid).all():
        #print("ItiraneryActivity query ***************")
        #print(itactivity.ITIRENERY_ID)
        #print(itactivity.ACTIVITY_ID)
        #print(itactivity.ACTIVITY_NAME)
        #print(itactivity.ACTIVITY_DESCRIPTION)
        #print(itactivity.DAY)
        #print(itactivity.DATE)
        return itactivity.dict