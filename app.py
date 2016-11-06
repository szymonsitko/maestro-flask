from flask import Flask, render_template, g, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from forms import RegisterForm, LoginForm, CreateAlbum, CreateSong
from werkzeug import secure_filename

import models
import os

staticfiles = '/home/simon/Documents/programming/python/flask/maestro/static'
app = Flask(__name__, static_url_path=staticfiles)
app.secret_key = '2sadxaaa4sakcSD'

# configuration for different files to upload: image files (media dir) and songs (media/songs)
app.config['UPLOAD_PICTURES_FOLDER'] = '/home/simon/Documents/programming/python/flask/maestro/static/media'
app.config['UPLOAD_SONGS_FOLDER'] = app.config['UPLOAD_PICTURES_FOLDER'] + '/songs/'

# lists with allowed extensions to upload (for function "allowed_files_extensions()")
song_extensions = ['mp3', 'wav', 'oog']
images_extensions = ['jpg', 'jpeg', 'gif', 'png']


@app.before_request
def before_request():
	# opens connection with database
	g.db = models.DATABASE
	g.db.connect()


@app.after_request
def after_request(response):
	# closes connections with database
	g.db.close()
	return response

# standard requirement for flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def user_loader(userid):
	# user_loader has to be configurated in order to help login manager to log user
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None


def allowed_files_extensions(filename, extensions):
	''' function-helper that validates input from file upload fields.
	Requires two parameters: secure filename (look: werzkeug docs) and list of
	extensions provided (above in this case) '''

	file = filename.split('.')
	if file[1] not in extensions:
		return False
	else:
		return True


@app.route('/create_album/', methods=['GET', 'POST'])
def create_album():

	''' Create album function allows user to add an album with photo (mandatory,
	since all albums have some covers). Data is validated by CreateAlbum form.

	BASE: if / else statements, exceptions are handled by rendering error_msg to 
	the template, so user can see what excatly went wrong withoud needing any further 
	help (reading, FAQ's etc.)

	'''

	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	
	else:
		add_album_form = CreateAlbum(request.form)
		if request.method == 'POST':
			if add_album_form.validate():
				f = request.files['file']
				file_name = secure_filename(f.filename)
				if allowed_files_extensions(file_name, images_extensions):
					f.save(os.path.join(app.config['UPLOAD_PICTURES_FOLDER'], file_name))
					models.Album.new_album(
						user=current_user.id, 
						artist=request.form['artist'], 
						album_title=request.form['album_title'],
						release_date=int(request.form['release_date']),
						genre=request.form['genre'],
						album_logo=file_name
						)
					return redirect(url_for('my_profile'))
				else:
					return render_template('create.html', 
						form=add_album_form,
						error_msg="File you are trying to upload is not supported.")
			else:
				return render_template('create.html', 
					form=add_album_form,
					error_msg="Cannot upload the file. Please check allowed extensions!")
	return render_template('create.html', form=add_album_form)


@app.route('/create_song/<int:album_id>', methods=['GET', 'POST'])
def create_song(album_id):

	''' function structure is very similar to the create_album function view. 
	Represents the same base, just parameters passed are different. Same BASE.
	'''

	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	else:
		add_song_form = CreateSong(request.form)
		if request.method == 'POST':
			if add_song_form.validate():
				f = request.files['file']
				file_name = secure_filename(f.filename)
				if allowed_files_extensions(file_name, song_extensions):
					f.save(os.path.join(app.config['UPLOAD_SONGS_FOLDER'], file_name))
					models.Song.new_song(
						album=album_id,
						song_title=request.form['song_title'],
						audio_file=file_name,
						)
					return redirect(url_for('details', media_id=album_id))
				else:
					return render_template('create.html', 
						form=add_song_form,
						error_msg="Unsupported media file uploaded.")
			else:
				return render_template('create.html', 
					form=add_song_form,
					error_msg="Form was not filled correctly. Try again please.")
		return render_template('create.html', form=add_song_form)


@app.route('/delete_album/<int:album_id>')
def delete_album(album_id):
	''' simple delete view, that comes with a int variable required to match query '''

	delete_album = models.Album.delete().where(models.Album.id == album_id)
	delete_album.execute()
	return redirect(url_for('my_profile'))

@app.route('/delete_song/<int:song_id>')
def delete_song(song_id):
	''' as above '''
	
	delete_song = models.Song.delete().where(models.Song.id == song_id)
	delete_song.execute()
	return redirect(url_for('my_profile'))

@app.route('/', methods=['GET', 'POST'])
def my_profile():

	''' this is the main page, available to registered users only (since this is the owm media
	browser). This function lists own albums and songs added previously. As a main view, it is
	a point of redirection for functions: 

	- create_song, 
	- create_album, 
	- login
	- register*

	*all of those after success/validation.

	If user is not authorised then it is being send to login page.

	BASE: if / else 

	'''
	if not current_user.is_authenticated:
		return redirect(url_for('login'))
	else:
		user_albums = models.Album.select().where(models.Album.user_id == current_user.id)
		return render_template('my_profile.html', user_albums=user_albums, staticfiles=staticfiles)


	return render_template('my_profile.html')

@app.route('/details/<int:media_id>')
def details(media_id):

	''' details view takes media_id as a paramter paased from my_details view as a 
	int variable. This var. is needed to create database query to retrieve two objects:

	1. album query 
	2. songs query (related to relevant album)

	'''

	detailed_albums = models.Album.get(models.Album.id == media_id)

	try:
		album_songs = models.Song.get(models.Song.album_id == media_id)
		return render_template('details.html', 
			album_query=detailed_albums,
			album_songs=album_songs,
			staticfiles=staticfiles,
			media_id=media_id)
	except:
		return render_template('details.html', 
			album_query=detailed_albums,
			staticfiles=staticfiles,
			media_id=media_id,
			error_msg="You haven't uploaded any songs yet.")


@app.route('/favorite_song/<int:song_id>')
def favorite_song(song_id):

	''' add_favorite is a typical function seen in many social media sites. It
	does not return any particular view (just redirects) but just adds boolean = True 
	for album or song. Depending on condition (True or False) special icon will be displayed,

	Function takes variable with int value that is used for query. '''

	song = models.Song.get(models.Song.id == song_id)
	if song.is_favorite:
		return redirect(url_for('details', media_id=song.album_id))
	else:
		song.is_favorite = True
		song.save()
		return redirect(url_for('details', media_id=song.album_id))

@app.route('/favorite_album/<int:album_id>')
def favorite_album(album_id):

	''' as described above (see: favorite_song). In this case, function takes 
	argument but redirects user to my_profile view with no variable passed,
	so user can see all owned media '''

	album = models.Album.get(models.Album.id == album_id)
	if album.is_favorite:
		return redirect(url_for('my_profile'))
	else:
		album.is_favorite = True
		album.save()
		return redirect(url_for('my_profile'))

@app.route('/search/', methods=['GET', 'POST'])
def search():

	''' simple search view that returns detail view of item that user is searching for.
	If criteria fails, view redirects to main view with error message '''
	if request.method == 'POST':
		search_quote = request.form['query']
		try:
			album = models.Album.get(models.Album.album_title == search_quote)
			album_query = album.id
			return redirect(url_for('details', media_id=album_query))

		except:
			return render_template('my_profile.html', error_msg="Cannot find album or song with following criteria.")
	else:
		return render_template('my_profile.html', error_msg="Cannot find album or song with following criteria.")


def login_helper(email, password):

	''' in order to clean code and avoid confusion, login helper checks whether:
	1. user exists in the system already 
	2. if user exists, function checks whether salted password matches this given
	by user during loging time.

	returns user, and this holds user queryset object which is used to authorise user
	by login_user() function

	BASE: try / except { if / else }

	'''

	try:
		user = models.User.get(models.User.email == email)
		if check_password_hash(user.password, password):
			return user
		else:
			return False
	except:
		return False


@app.route('/login/', methods=['GET','POST'])
def login():

	''' simple login function that takes parameters from user input. Formm is being 
	validated, helper fires on third if statement, and if successful then user is get logged,
	otherwise user gets error 

	BASE: if / else statement

	'''

	login_form = LoginForm(request.form)
	if request.method == 'POST':
		if login_form.validate():
			email = request.form['email']
			password = request.form['password']
			user_login = login_helper(email, password)
			if user_login:
				login_user(user_login)
				return redirect(url_for('my_profile'))
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

	''' simple function thath checks whether user exists already in the db or not.
	If yes, user gets error, otherwise registration fires '''

	if user_name in models.User.select():
		return False
	else:
		return True 

@app.route('/register/', methods=['GET', 'POST'])
def register():

	''' simple register form, with register_validator() helper used to check if
	inserted data can be accepted by db or not 

	BASE: if / else 

	'''

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
	''' simplest function in this app, just simple uses tools provided by flask_login
	module to logout user '''

	logout_user()
	return redirect(url_for('create_album'))


if __name__ == "__main__":
	models.initialize()
	app.debug = True
	app.run(host='127.0.0.1', port=8000)