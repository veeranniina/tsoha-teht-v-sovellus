from os import getenv
from flask import Flask, session
import secrets

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

def generate_csrf_token():
    session["csrf_token"] = secrets.token_hex(16)

#ennen pyyntöä tarkastetaan, onko CSRF-tokeni tallennettu istuntoon
@app.before_request
def before_request():
    if "csrf_token" not in session:
        generate_csrf_token()

import routes