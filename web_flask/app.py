from flask import Flask
from registration import reg
from login import log_in
from create_new_transaction import transact
from flask_jwt_extended import JWTManager
import secrets

# Create a Flask app
app = Flask(__name__)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Set the secret key for JWT tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)


# Register the blueprint with the app
app.register_blueprint(reg)
app.register_blueprint(log_in)
app.register_blueprint(transact)

if __name__ == '__main__':
    app.run()