from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction_model import Transactions
import traceback
from models.user_model import User

# Create a Blueprint instance
delete_act = Blueprint('delete_act', __name__)

@delete_act.route('/delete_account', methods=['DELETE'])
@jwt_required()  # Requires a valid JWT token
def delete_account():
    """Delete user account."""
    try:
        # Get email and password from request body
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Get user_id from JWT token
        user_id = get_jwt_identity()

        # Fetch transactions associated with the provided user_id
        user_transactions = Transactions.all_transactions(user_id)

        # Check if there are transactions associated with the user_id
        if user_transactions is not None:
            for transaction in user_transactions:
                print(transaction)
                transaction.remove_account()

        # Retrieve the user
        user = User.check_user(email, password)

        if user:
            print(user)
            user.remove_account()
            return jsonify({'message': 'account deleted successfully.'}), 200
        
        return jsonify({'message': 'User does not exist.'}), 404

    except Exception as e:
        # Log the exception
        print("Exception occurred in delete_account function:")
        traceback.print_exc()

        return jsonify({'error': 'Server error occurred.'}), 500
