#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String

Base = declarative_base()

class BaseModel:
    """Defines the BaseModel class.

    Attributes:
        user_id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """

    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("user_password", None)
        return my_dict

    def delete(self, transaction_id, transaction_user_id):
        """Delete the current instance from storage."""
        storage_instance = models.storage 
        return storage_instance.delete_transaction(transaction_id, transaction_user_id)

    def remove_account(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
        

    def check_user(email, user_password):
        """retrives current instance from storage"""
        return  models.storage.get_user(email, user_password)

    def get_types(transaction_user_id, column_name):
        """retrives all instance of distinct types in the colunm"""
        return models.storage.all_distinct_types(transaction_user_id, column_name)
    
    def search(transaction_user_id, column_name, filter_value=None, start_date=None, end_date=None, min_amount=None, max_amount=None):
        """Retrieve rows based on specified criteria.

        Args:
            transaction_user_id (str): The user ID associated with the transaction.
            column_name (str): The name of the column to filter by.
            filter_value (str, optional): The value to filter the specified column by.
            start_date (str, optional): The start date of the date range.
            end_date (str, optional): The end date of the date range.
            min_amount (float, optional): The minimum amount value for the amount range.
            max_amount (float, optional): The maximum amount value for the amount range.

        Returns:
            list: List of rows matching the given criteria.
        """
        # Check for compulsory arguments
        if not transaction_user_id or not column_name:
            raise ValueError("transaction_user_id and column_name are compulsory arguments.")

        # Check for at least one filtering criterion
        if filter_value is None and start_date is None and end_date is None and min_amount is None and max_amount is None:
            raise ValueError("At least one filtering criterion must be provided.")

        # Call retrieve_rows function with provided arguments
        return models.storage.retrieve_rows(transaction_user_id, column_name, filter_value, start_date, end_date, min_amount, max_amount)
