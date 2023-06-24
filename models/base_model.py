#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import uuid
import models
from datetime import datetime

Base = declarative_base()

class BaseModel:
    """ Base Model for all other classes """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """ Instantiation of base model class 
        Args:
            *args: arguments
            **kwargs: keyword arguments
        Attributes:
            id: id of the instance
            created_at: time of creation
            updated_at: time of update
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """ Returns a string representation of the instance """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()

    def save(self):
        """ Updates the public instance attribute updated_at"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ Create a dict of instance attributes
        and update the public instance
        Returns:
            a dict of instance attributes
        """
        new_dict = dict(self.__dict__)
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in new_dict.keys():
            del new_dict['_sa_instance_state']
        return new_dict

    def delete(self):
        """ Delete the current instance from the storage """
        models.storage.delete(self)

