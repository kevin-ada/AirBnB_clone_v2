#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base

from models.base_model import BaseModel

Base = declarative_base()


class State(BaseModel, Base):
    """ Represents a state for a MySQL database """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
