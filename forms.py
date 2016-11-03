from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, 
	Length)
from wtforms import Form, BooleanField, StringField, PasswordField, FileField, validators
from peewee import *

class RegisterForm(Form):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message=('Username should contin one word, letters, numbers, underscore or hyphen only!')
		),
			])
	
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			])	

	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=5),	
		])

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])

class CreateAlbum(Form):
	artist = StringField('Artist',validators=[DataRequired()])
	album_title = StringField('Album title',validators=[DataRequired()])
	genre = StringField('Genre',validators=[DataRequired()])
	album_logo = StringField('Logo', validators=[DataRequired()])

