from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, 
	Length)
from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, FileField, validators
from peewee import *
import models


def name_exists(form, field):
    if models.User.select().where(models.User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if models.User.select().where(models.User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

def release_date(form, field):
	if field == str:
		raise ValidationError('Year given is not number!')

class RegisterForm(Form):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message=('Username should contin one word, letters, numbers, underscore or hyphen only!')
			),
			name_exists,
			])
	
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists,
			])	

	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=5),	
		])

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class CreateAlbum(Form):
	artist = StringField('Artist',validators=[DataRequired()])
	album_title = StringField('Album title',validators=[DataRequired()])
	release_date = StringField('Release date', validators=[release_date])
	genre = StringField('Genre',validators=[DataRequired()])

class CreateSong(Form):
	song_title = StringField('Song title', validators=[DataRequired()])
	audio_file = StringField('File format', )

