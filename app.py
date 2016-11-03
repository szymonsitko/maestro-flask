from flask import Flask, render_template, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models

app = Flask(__name__)
app.secret_key = '2sadxaaa4sakcSD'

@app.before_request
def before_request():
	g.db = DATABASE

@app.after_request
def after_request():
	g.db.close()
	return response



if __name__ == "__main__":
	models.initialize()
	app.debug = True
	app.run(host='127.0.0.1', port=8000)