from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction_model import Transactions
import traceback

# Create a Blueprint instance
delete_transact = Blueprint('delete_transaction', __name__)

@delete_transact.route('/delete_transaction/<int:transaction_id>', methods=['DELETE'])
@jwt_required()  # Requires a valid JWT token
def delete_transaction(transaction_id):
    """Delete a transaction for the logged-in user."""
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Retrieve the transaction by its ID
        transaction = Transactions.get_a_transaction(transaction_id, transaction_user_id)

        # Check if the transaction exists and belongs to the logged-in user
        if transaction is None or transaction.transaction_user_id != transaction_user_id:
            return jsonify({'error': 'Transaction not found or unauthorized.'}), 404

        # Delete the transaction from the database
        transaction.delete(transaction_id, transaction_user_id)

        return jsonify({'message': 'Transaction deleted successfully.'}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in delete_transaction function:")
        traceback.print_exc()


        return jsonify({'error': 'Server error occurred.'}), 500
