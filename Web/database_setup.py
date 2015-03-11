__author__ = 'Alex_lai'

import sys
from sqlalchemy import Column, ForeignKey, Integer, String

# will be used in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# in order to create foreign key relationship
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    # representation of table in the database
    __tablename__ = 'restaurant'
    # representation of column in the table
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
	
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'         : self.id,
       }
 
class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 
	
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'course'         : self.course,
       }
	   
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

"""
add data to empty database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

// change directory first, and then import modules in setup file
import sys
sys.path.append('C:\PyCharmFolder\Test1')
from foo import util,bar

>>> from database_setup import Base, Restaurant, MenuItem
>>> engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

>>> Base.metadata.bind = engine

>>> DBSession = sessionmaker(bind = engine)
>>> session  = DBSession()
>>> FirstRest = Restaurant(name = "Pizza hunt")
>>> session.add(FirstRest)
>>> session.commit()
>>> session.query(Restaurant).all()
[<database_setup.Restaurant object at 0x0000000003ADC5F8>]

// add Menuitem to Restaurant
>>> cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural cheese", course = "Entree", price ="$8.99", restaurant = FirstRest)
>>> session.add(cheesePizza)
>>> session.commit()
>>> session.query(MenuItem).all()
[<database_setup.MenuItem object at 0x0000000003ADC5C0>]

// do query.
session.query(table_name).filter_by(name = '')  -> return a list
session.query(table_name).filter_by(id = 8).one() -> return one entry.

// do update
after we find the entry we can make a change.
then use
making update efficiently, before we do join tables, we check existence in the first table.

session.add(query_entry) // same like add data
session.commit()

// do deleter
1. find entry
2. session.delete(entry)
3. session.commit()

"""


