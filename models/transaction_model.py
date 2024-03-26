#!/usr/bin/python3
"""Defines the Transactions class."""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Float
from sqlalchemy import Text
from models.base_model import BaseModel
from models.base_model import Base
import models

class Transactions(BaseModel, Base):
    """Represents a transaction for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table transactions.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store users.
        transaction_user_id (sqlalchemy String): The user's id.
        transaction_id (sqlalchemy String): The transaction id.
        amount (sqlalchemy int): Transaction amount.
        currency (sqlalchemy int): The transaction amount.
        category (sqlalchemy String): The transaction category.
        transaction_description (sqlalchemy String): The transaction description.
    """
    __tablename__ = "transactions"
    transaction_user_id = Column(String(128), ForeignKey('user.user_id'))
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float)
    currency = Column(String(128))
    category = Column(String(128))
    transaction_description = Column(Text)

    def get_a_transaction(transaction_id, transaction_user_id):
        """retrives current instance from storage if it exists"""
        return  models.storage.existing_transaction(transaction_id, transaction_user_id)
