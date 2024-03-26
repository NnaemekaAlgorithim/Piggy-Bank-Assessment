from flask import Blueprint, request, jsonify
from models.transaction_model import Transactions
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback

# Create a Blueprint instance
transact = Blueprint('transactions', __name__)

@transact.route('/add_transaction', methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def add_transaction():
    """Adds a new transaction for the logged-in user.

    Receives transaction data in JSON format and creates a new transaction object
    in the database associated with the currently logged-in user. Returns a success
    message upon successful creation of the transaction.

    Requires the user to be logged in with a valid JWT token. The user ID associated
    with the JWT token is used to link the transaction to the corresponding user.

    Args:
        data (dict): JSON data containing transaction information, including amount and description.

    Returns:
        JSON: Message indicating successful transaction creation or failure message.
    """
    try:
        data = request.get_json()

        # Ensure request contains required data
        required_fields = ['amount', 'currency', 'category', 'transaction_description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing value for {field}'}), 400

        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Create a new transaction record using user_id
        transaction = Transactions()
        transaction.transaction_user_id = transaction_user_id
        transaction.amount = data['amount']
        transaction.currency = data['currency']
        transaction.category = data['category']
        transaction.transaction_description = data['transaction_description']
        transaction.save()  # Assuming you have a save method in your Transaction model

        return jsonify({'message': 'Transaction added successfully.'}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in logout function:")
        traceback.print_exc()

        return jsonify({'error': 'Server error occurred.'}), 500
