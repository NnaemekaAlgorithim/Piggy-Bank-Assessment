from flask import Flask
from registration import reg
from login import log_in
from search import search_by
from create_new_transaction import transact
from edit_transaction import edit_transact
from view_transactions import transact_view
from delete_transaction import delete_transact
from delete_account import delete_act
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import secrets

# Create a Flask app
app = Flask(__name__)
CORS(app)

# Set the secret key for Flask sessions
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Set the secret key for JWT tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)


# Register the blueprint with the app
app.register_blueprint(reg)
app.register_blueprint(log_in)
app.register_blueprint(transact)
app.register_blueprint(edit_transact)
app.register_blueprint(transact_view)
app.register_blueprint(search_by)
app.register_blueprint(delete_transact)
app.register_blueprint(delete_act)

if __name__ == '__main__':
    app.run()