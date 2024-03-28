from flask import Blueprint, jsonify, request
from models.transaction_model import Transactions
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create a Blueprint instance
search_by = Blueprint('transactions_search', __name__)

@search_by.route('/get_rows_by_currency', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_rows_by_currency():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch rows by currency type associated with the provided user_id
        currency_type = request.args.get('currency_type')
        rows = Transactions.search(transaction_user_id, 'currency', currency_type)

        # Convert rows to a list of dictionaries
        rows_data = []
        for row in rows:
            rows_data.append({
                'transaction_id': row.transaction_id,
                'amount': row.amount,
                'currency': row.currency,
                'category': row.category,
                'transaction_description': row.transaction_description
            })

        return jsonify(rows_data), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_rows_by_currency function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500

@search_by.route('/get_rows_by_category', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_rows_by_category():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch rows by category type associated with the provided user_id
        category_type = request.args.get('category_type')
        rows = Transactions.search(transaction_user_id, 'category', category_type)

        # Convert rows to a list of dictionaries
        rows_data = []
        for row in rows:
            rows_data.append({
                'transaction_id': row.transaction_id,
                'amount': row.amount,
                'currency': row.currency,
                'category': row.category,
                'transaction_description': row.transaction_description
            })

        return jsonify(rows_data), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_rows_by_category function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500

@search_by.route('/get_rows_by_amount_range', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_rows_by_amount_range():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch rows by amount range associated with the provided user_id
        min_amount = request.args.get('min_amount')
        max_amount = request.args.get('max_amount')
        rows = Transactions.search(transaction_user_id, 'amount', min_amount=min_amount, max_amount=max_amount)

        # Convert rows to a list of dictionaries
        rows_data = []
        for row in rows:
            rows_data.append({
                'transaction_id': row.transaction_id,
                'amount': row.amount,
                'currency': row.currency,
                'category': row.category,
                'transaction_description': row.transaction_description
            })

        return jsonify(rows_data), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_rows_by_amount_range function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500
    
@search_by.route('/get_rows_by_date_range', methods=['GET'])
@jwt_required()  # Requires a valid JWT token
def get_rows_by_date_range():
    try:
        # Get user_id from JWT token
        transaction_user_id = get_jwt_identity()

        # Fetch rows by date range associated with the provided user_id
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        rows = Transactions.search(transaction_user_id, 'created_at', start_date=start_date, end_date=end_date)

        # Convert rows to a list of dictionaries
        rows_data = []
        for row in rows:
            rows_data.append({
                'transaction_id': row.transaction_id,
                'amount': row.amount,
                'currency': row.currency,
                'category': row.category,
                'transaction_description': row.transaction_description
            })

        return jsonify(rows_data), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in get_rows_by_date_range function:")
        print(e)
        return jsonify({'error': 'Server error occurred.'}), 500
