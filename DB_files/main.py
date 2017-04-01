'''
Created on Mar 24, 2017

@author: Default
'''
from sqlalchemy_genie_insert import Insert
from sqlalchemy_genie_query import Query
from sqlalchemy_genie_declarative import UserProfile, UserAddress, UserTrip, TripItiranery, ItiraneryActivity

if __name__ == '__main__':
    pass



userid="dmitriy1"
tripid="13"
tripname="russia_trip"
tripdescription="trip to russia"
itid="3"
activityid="3"
fname="dmitriy"
lname="grishin"
address="Tinton Falls"
emailaddress="dgrishin1@stevens.edu"
passwd="admin"
active="A"

"""

insert=Insert();
insert.insert_user_profile(userid, passwd, active)
insert.insert_user_address(userid, fname, lname, address, emailaddress)
insert.insert_trip(userid, tripid, tripname, tripdescription)
insert.insert_trip_it(tripid, itid, activityid)

"""
query=Query()
trips=query.query_tripid_details_and_tripname(userid,tripname)

#for trip in enumerate(trips):
   # print (trip)
    
for trip in trips:
    print (trip['USER_ID'])
    print (trip['TRIP_ID'])
    print (trip['TRIP_NAME'])
    print (trip['TRIP_DESCRIPTION'])
    
    


