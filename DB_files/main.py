'''
Created on Mar 24, 2017

@author: Default
'''
from sqlalchemy_genie_insert import Insert

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

insert=Insert();
insert.insert_user_profile(userid, passwd, active)
insert.insert_user_address(userid, fname, lname, address, emailaddress)
insert.insert_trip(userid, tripid, tripname, tripdescription)
insert.insert_trip_it(tripid, itid, activityid)
