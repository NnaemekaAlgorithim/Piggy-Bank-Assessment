#!/usr/bin/python3
from flask import Blueprint, request, jsonify
from models.transaction_model import Transactions
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback

# Create a Blueprint instance
edit_transact = Blueprint('edit_transactions', __name__)

@edit_transact.route('/edit_transaction/<int:transaction_id>', methods=['PUT'])
@jwt_required()  # Requires a valid JWT token
def edit_transaction(transaction_id):
    """Edit an existing transaction for the logged-in user.

    Receives updated transaction data in JSON format and updates the corresponding
    transaction object in the database. Returns a success message upon successful
    update of the transaction.

    Requires the user to be logged in with a valid JWT token. The user ID associated
    with the JWT token is used to verify ownership of the transaction.

    Args:
        transaction_id (int): ID of the transaction to be edited.
        data (dict): JSON data containing updated transaction information.

    Returns:
        JSON: Message indicating successful transaction update or failure message.
    """
    try:
        data = request.get_json()

        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Retrieve the transaction from the database
        transaction = Transactions.get_a_transaction(transaction_id, transaction_user_id)

        if not transaction:
            return jsonify({'error': 'Transaction not found or you do not have permission to edit it.'}), 404

        # Update transaction details
        if 'amount' in data:
            transaction.amount = data['amount']
        if 'currency' in data:
            transaction.currency = data['currency']
        if 'category' in data:
            transaction.category = data['category']
        if 'transaction_description' in data:
            transaction.transaction_description = data['transaction_description']
        
        transaction.save()  # Assuming you have a save method in your Transaction model

        return jsonify({'message': 'Transaction updated successfully.'}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in edit_transaction function:")
        traceback.print_exc()

        return jsonify({'error': 'Server error occurred.'}), 500
