from flask import Flask, render_template, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
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

@login_manager.user_loader
def user_loader(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

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





def login_helper(email, password):
	try:
		user = models.User.get(models.User.email == email)
		print(user.password)
		if check_password_hash(user.password, password):
			return user
		else:
			return False
	except:
		return False



@app.route('/login/', methods=['GET','POST'])
def login():
	login_form = LoginForm(request.form)
	if request.method == 'POST':
		if login_form.validate():
			email = request.form['email']
			password = request.form['password']
			user_login = login_helper(email, password)
			print(user_login)
			if user_login:
				login_user(user_login)
				return redirect(url_for('create_album'))
			else:
				return render_template('login.html',
					login_form=login_form,
					error_msg="Cannot authorise user. Try again!")
		else:
			return render_template('login.html', 
				login_form=login_form,
				error_msg="Incorrect data given, please try again!")
	else:
		return render_template('login.html', login_form=login_form)

def register_validator(user_name):
	if user_name in models.User.select():
		return False
	else:
		return True 

@app.route('/register/', methods=['GET', 'POST'])
def register():
	register_form = RegisterForm(request.form)
	if request.method == 'POST':
		if register_form.validate() and register_validator(request.form['username']):
			user = request.form['username']
			email = request.form['email']
			password = generate_password_hash(request.form['password'])
			models.User.new_user(
				username=user, 
				email=email, 
				password=password
				)
			user_login = models.User.get(models.User.username == user)
			login_user(user_login)
			return redirect(url_for('create_album'))
		else:
			return render_template('login.html', error_msg="Wrong details provided. Try again.")
	else:
		return render_template('login.html', register_form=register_form)

@app.route('/logout/')
def logout():
	return ('Logged out')


if __name__ == "__main__":
	models.initialize()
	app.debug = True
	app.run(host='127.0.0.1', port=8000)