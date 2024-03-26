import traceback
from flask import Blueprint, request, jsonify, session
from models.user_model import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Create a Blueprint instance
log_in = Blueprint('Login_users', __name__)

# Track active sessions for users
active_sessions = {}

@log_in.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        user_password = data.get('user_password')

        # Validate inputs
        if not email or not user_password:
            return jsonify({'error': 'Email and password are required.'}), 400

        # Retrieve user from the database
        user = User.check_user(email, user_password)

        if user:
            # Invalidate existing session if user is already logged in
            if User.user_id in active_sessions:
                active_sessions.pop(user.user_id)
                # Perform any additional actions, such as notifying the user

            # Store user's identity in session
            session['user_id'] = user.user_id
            active_sessions[user.user_id] = request.remote_addr

            # Successful login
            access_token = create_access_token(identity=user.user_id)
            response = jsonify({'message': 'Login successful.', 'access_token': access_token})
            return response, 200
        else:
            # Invalid credentials
            return jsonify({'error': 'Invalid email or password.'}), 401

    except Exception as e:
        # Log the exception
        print("Exception occurred in login function:")
        traceback.print_exc()

        # Handle server failure
        return jsonify({'error': 'Server error during registration.'}), 500

@log_in.route('/logout', methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def logout():
    try:
        # Remove user's identity from session
        session.pop('user_id', None)

        # Invalidate active session
        user_id = get_jwt_identity()
        if user_id in active_sessions:
            active_sessions.pop(user_id)

        return jsonify({'message': 'Logout successful.'}), 200

    except Exception as e:
        # Log the exception
        print("Exception occurred in logout function:")
        traceback.print_exc()
        
        # Handle server failure
        return jsonify({'error': 'Server error during logout.'}), 500
