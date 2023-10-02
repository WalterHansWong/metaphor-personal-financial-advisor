from flask import Flask
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()

from app import routes
