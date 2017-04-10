'''
Created on Mar 3, 2017

@author: Default
'''
import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from test.datetimetester import DAY
from sqlalchemy.sql.operators import comma_op
 
engine = create_engine('sqlite:///travel_genie_4.db',echo=True)
 
Base = declarative_base() 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.


class UserProfile(Base):
    '''
    classdocs
    '''      
    __tablename__ = 'USER_PROFILE'

    USER_ID  = Column(String, primary_key=True)
    USER_PASSWD  = Column(String, nullable=False)
    USER_ACTIVE = Column(String, nullable=True)
    
    
class UserAddress(Base):
    '''
    classdocs
    '''
            
    __tablename__ = 'USER_ADDRESS'
 
    USER_ID = Column(String, ForeignKey('USER_PROFILE.USER_ID'))
    FIRST_NAME = Column(String, nullable=False)
    LAST_NAME = Column(String, nullable=False)
    ADDRESS = Column(String, nullable=False)
    EMAIL_ADDRESS = Column(String,  primary_key=True) 
    #EMAIL_ADDRESS = Column(String,  nullable=True)       
    user = relationship(UserProfile)
    
    
class UserTrip(Base):
    '''
    classdocs
    '''
           
    __tablename__ = 'USER_TRIP'

    USER_ID  = Column(String,ForeignKey('USER_PROFILE.USER_ID'))
    TRIP_ID  = Column(String, primary_key=True)
    TRIP_NAME = Column(String, nullable=True)
    TRIP_DESCRIPTION=Column(String, nullable=True)
    user = relationship(UserProfile)
   
    
class TripItiranery(Base):
    '''
    classdocs
    '''
           
    __tablename__ = 'TRIP_ITIRANERY'
  
    TRIP_ID  = Column(String, ForeignKey('USER_TRIP.TRIP_ID'))
    ITIRENERY_ID  = Column(String, primary_key=True)
    ACTIVITY_ID = Column(String, nullable=False)
    user_trip = relationship(UserTrip)
    
class ItiraneryActivity(Base):
    '''
    classdocs
    '''
   
    __tablename__ = 'ITIRANERY_ACTIVITY'
   
    ITIRENERY_ID  = Column(String, ForeignKey('TRIP_ITIRANERY.ITIRENERY_ID'))
    ACTIVITY_ID = Column(String,  primary_key=True)
    ACTIVITY_NAME = Column(String, nullable=True)
    ACTIVITY_DESCRIPTION = Column(String, nullable=True)
    DAY  = Column(String, nullable=True)
    DATE  = Column(String, nullable=True)
    BUDGET = Column(String, nullable=True)
    TRANSPORTATION = Column(String, nullable=True)
    ACCOMODATION = Column(String, nullable=True)
    COMPLETE = Column(String, nullable=True)
    COMMENTS = Column(String, nullable=True)
    trip_it = relationship(TripItiranery)
     
Base.metadata.create_all(engine)
