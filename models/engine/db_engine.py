#!/usr/bin/python3
"""Defines the DBStorage engine."""
from flask_bcrypt import check_password_hash
from os import getenv
from models.transaction_model import Transactions
from models.user_model import User
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from pymysql import connect, cursors


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+pymysql://{}:{}@{}/{}".
                                      format(getenv("MYSQL_USER"),
                                             getenv("MYSQL_PWD"),
                                             getenv("MYSQL_HOST"),
                                             getenv("MYSQL_DB")),
                                     )

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete_transaction(self, transaction_id, transaction_user_id):
        """Delete a transaction by its ID and user ID from the current database session."""
        try:
            # Query the transaction by its ID and user ID
            transaction_to_delete = self.__session.query(Transactions).filter(
                Transactions.transaction_id == transaction_id,
                Transactions.transaction_user_id == transaction_user_id
            ).first()

            # Check if the transaction exists
            if transaction_to_delete is None:
                return False  # Return False if transaction does not exist

            # Delete the transaction from the session
            self.__session.delete(transaction_to_delete)

            # Commit the changes to persist the deletion
            self.__session.commit()

            return True  # Return True to indicate successful deletion

        except Exception as e:
            # Log the exception or handle it accordingly
            print("An error occurred while deleting the transaction:", e)
            self.__session.rollback()  # Rollback changes in case of an error
            return False  # Return False to indicate deletion failure
        
    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    
    def get_user(self, email=None, user_password=None):
        """Retrieve a user from the database by email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The matching User object if found, None otherwise.
        """
        user = self.__session.query(User).filter(User.email == email).first()

        if user and check_password_hash(user.user_password, user_password):
            return user

        return None

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
    
    def existing_user(self, email=None):
        """Retrieve a user from the database by email.

        Args:
            email (str): The user's email.

        Returns:
            User: The matching User object if found, None otherwise.
        """
        user = self.__session.query(User).filter(User.email == email).first()

        if user:
            return user

        return None
    
    def existing_transaction(self, transaction_id=None, transaction_user_id=None):
        """Retrieve a transaction from the database by transaction_id and transaction_user_id.

        Args:
            transaction_id (int): The transaction's ID.
            transaction_user_id (str): The user ID associated with the transaction.

        Returns:
            Transactions: The matching Transactions object if found, None otherwise.
        """
        transaction = self.__session.query(Transactions).filter(
            Transactions.transaction_id == transaction_id,
            Transactions.transaction_user_id == transaction_user_id
        ).first()

        if transaction:
            return transaction

        return None
    
    def all_existing_transactions(self, transaction_user_id=None):
        """Retrieve transaction from the database by transaction_user_id.

        Args:
            transaction_user_id (str): The user ID associated with the transaction.

        Returns:
            Transactions: The matching Transactions object if found, None otherwise.
        """
        transaction = self.__session.query(Transactions).filter(
            Transactions.transaction_user_id == transaction_user_id
        ).all()

        if transaction:
            return transaction

        return None

    def all_distinct_types(self, transaction_user_id=None, column_name=None):
        """Retrieve all distinct values from the specified column for a given transaction_user_id.

        Args:
            transaction_user_id (str): The user ID associated with the transaction.
            column_name (str): The name of the column to retrieve distinct values from.

        Returns:
            list: List of distinct values from the specified column.
        """
        if not column_name:
            raise ValueError("Column name must be provided.")

        transaction = self.__session.query(getattr(Transactions, column_name)).filter(
            Transactions.transaction_user_id == transaction_user_id
        ).distinct().all()

        if transaction:
            return [item[0] for item in transaction]

        return None

    def retrieve_rows(self, transaction_user_id=None, column_name=None, filter_value=None, start_date=None, end_date=None, min_amount=None, max_amount=None):
        """Retrieve rows based on specified criteria.

        Args:
            transaction_user_id (str): The user ID associated with the transaction.
            column_name (str): The name of the column to filter by.
            filter_value (str): The value to filter the specified column by.
            start_date (str): The start date of the date range in the format 'YYYY-MM-DD'.
            end_date (str): The end date of the date range in the format 'YYYY-MM-DD'.
            min_amount (float): The minimum amount value for the amount range.
            max_amount (float): The maximum amount value for the amount range.

        Returns:
            list: List of rows matching the given criteria.
        """
        try:
            if not column_name or (not filter_value and not start_date and not end_date and min_amount is None and max_amount is None):
                raise ValueError("At least one filtering criterion must be provided.")

            query = self.__session.query(Transactions).filter(
                Transactions.transaction_user_id == transaction_user_id
            )

            if column_name and filter_value:
                query = query.filter(
                    getattr(Transactions, column_name) == filter_value
                )

            if start_date and end_date:
                query = query.filter(
                    Transactions.created_at.between(start_date, end_date)
                )

            if min_amount is not None:
                query = query.filter(
                    Transactions.amount >= min_amount
                )

            if max_amount is not None:
                query = query.filter(
                    Transactions.amount <= max_amount
                )

            rows = query.all()

            return rows

        except Exception as e:
            # Log the exception
            print("Exception occurred in retrieve_rows function:")
            print(e)
            return []
