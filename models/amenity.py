#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base



class Amenity(BaseModel, Base):
    from sqlalchemy import Column, String
    from models import type_storage
    """Amenity class"""
    __tablename__ = 'amenities'
    if type_storage == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
