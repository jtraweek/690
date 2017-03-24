'''
Created on Mar 3, 2017

@author: Default
'''
 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from sqlalchemy_genie_declarative import UserProfile, UserAddress, UserTrip, TripItiranery, ItiraneryActivity
 
engine = create_engine('sqlite:///travel_genie_4.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base = declarative_base()
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

#new_user_profile,new_user_address,new_user_trip,new_trip_it,new_it_activity
 
class Insert:
     
    def insert_user_profile(self,userid,user_password,user_active):
        global new_user_profile 
        new_user_profile = UserProfile(USER_ID=userid,USER_PASSWD=user_password,USER_ACTIVE=user_active)
        session.add(new_user_profile)
        session.commit()
     
    def insert_user_address(self,userid,fname,lname,address,emailaddress): 
        global new_user_address
        new_user_address = UserAddress(USER_ID=userid, FIRST_NAME=fname,LAST_NAME=lname,ADDRESS=address,EMAIL_ADDRESS=emailaddress,user=new_user_profile)
        session.add(new_user_address)
        session.commit()
    
    def insert_trip(self,userid,tripid,tripname,tripdescription):
        global new_user_trip        
        new_user_trip = UserTrip(USER_ID=userid, TRIP_ID=tripid,TRIP_NAME=tripname,TRIP_DESCRIPTION=tripdescription,user=new_user_profile)
        session.add(new_user_trip)
        session.commit()
    
    def insert_trip_it(self, tripid,itid,activityid):
        global new_trip_it
        new_trip_it = TripItiranery(TRIP_ID=tripid, ITIRENERY_ID=itid,ACTIVITY_ID=activityid,user_trip=new_user_trip)
        session.add(new_trip_it)
        session.commit()
    
    def insert_it_acitvity(self,itid,activityid,activityname,activitydesc,day,date,budget,transportation,accomodation,complete,comments):
        global new_it_activity
        new_it_activity = ItiraneryActivity(ITIRENERY_ID=itid, ACTIVITY_ID=activityid,ACTIVITY_NAME=activityname,ACTIVITY_DESCRIPTION=activitydesc,DAY=day,DATE=date,
        BUDGET=budget,TRANSPORTATION=transportation,ACCOMODATION=accomodation,COMPLETE=complete,COMMENTS=comments,trip_it=new_trip_it)
        session.add(new_it_activity)
        session.commit()


  