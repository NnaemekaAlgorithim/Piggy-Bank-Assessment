from flask import Blueprint, jsonify
from models.transaction_model import Transactions
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint instance
transact_view = Blueprint('transactions_view', __name__)

@transact_view.route('/get_transactions', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_transactions():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch transactions associated with the provided user_id
        transactions_view = Transactions.all_transactions(transaction_user_id)

        # Convert transactions to a list of dictionaries
        transactions_data = []
        for transaction in transactions_view:
            transactions_data.append({
                'transaction_id': transaction.transaction_id,
                'amount': transaction.amount,
                'currency': transaction.currency,
                'category': transaction.category,
                'transaction_description': transaction.transaction_description
            })

        return jsonify(transactions_data), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_transactions function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500

@transact_view.route('/get_distinct_currencies', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_distinct_currencies():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch distinct currencies associated with the provided user_id
        distinct_currencies = Transactions.get_types(transaction_user_id, 'currency')

        return jsonify({'distinct_currencies': distinct_currencies}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_distinct_currencies function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500

@transact_view.route('/get_distinct_categories', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_distinct_categories():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch distinct categories associated with the provided user_id
        distinct_categories = Transactions.get_types(transaction_user_id, 'category')

        return jsonify({'distinct_categories': distinct_categories}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_distinct_categories function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500
