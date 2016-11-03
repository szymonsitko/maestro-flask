from flask import Flask, render_template, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from forms import RegisterForm, LoginForm, CreateAlbum

import models

app = Flask(__name__)
app.secret_key = '2sadxaaa4sakcSD'

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/create_album/', methods=['GET', 'POST'])
def create_album():

	''' Create album function allows user to add an album with photo (mandatory,
	since all albums have some covers). Data is validated by CreateAlbum form.

	BASE: if / else statements 

	'''

	# if not current_user.is_authenticated:
	# 	return redirect(url_for('login'))
	# else:





	return render_template('create_album.html')










@app.route('/login/')
def login():
	return render_template('login.html')

@app.route('/register/')
def register():
	return render_template('register.html')

@app.route('/logout/')
def logout():
	return ('Logged out')


if __name__ == "__main__":
	models.initialize()
	app.debug = True
	app.run(host='127.0.0.1', port=8000)