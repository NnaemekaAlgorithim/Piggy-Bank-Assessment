from flask import Blueprint, request, jsonify
from models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Create a Blueprint instance for user-related routes
reg = Blueprint("Register_users", __name__)

@reg.route("/register", methods=["POST"])
def register():
    """Registers a new user with the provided details.

    Receives user data in JSON format and creates a new User object
    in the database. Returns a success message on successful registration.
    If the email already exists, prompts the user to login.

    Args:
        data (dict): JSON data containing user information,
        including first_name, last_name, gender, date_of_birth,
        phone_number, email, address, country_of_origin, and password.

    Returns:
        JSON: message indicating successful registration or failure message.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify(message='Missing JSON data'), 400

        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify(message=f'Missing value for {field}'), 400

        email = data["email"]

        # Check if email already exists
        existing_user = User.check_if_user_exist(email)
        if existing_user:
            return jsonify(message='Email already exists, please login'), 400

        first_name = data["first_name"]
        last_name = data["last_name"]
        user_password = data["password"]

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')

        # Create a new User object and populate its attributes
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.user_password = hashed_password

        # Save the user to the database
        user.save()

        # Return a success message
        return jsonify(message='Registration successful'), 201

    except Exception as e:
        return jsonify(message='Failed to register user'), 500