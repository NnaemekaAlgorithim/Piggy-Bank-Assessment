#!/usr/bin/python3
"""Defines the Transactions class."""
from uuid import uuid4
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Float
from sqlalchemy import Text
from models.base_model import BaseModel
from models.base_model import Base

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
    transaction_id = Column(String(60), primary_key=True, default=uuid4().hex)
    amount = Column(Float)
    currency = Column(String(128))
    category = Column(String(128))
    transaction_description = Column(Text)
