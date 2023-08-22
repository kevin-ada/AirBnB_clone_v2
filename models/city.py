#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base

from models.base_model import BaseModel

Base = declarative_base()


class City(BaseModel, Base):
    """ This reperesents a table cities in our MySQL db """
    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

