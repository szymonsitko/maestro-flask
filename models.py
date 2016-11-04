from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

import datetime

DATABASE = SqliteDatabase('maestro.db')

class BaseModel(Model):

    class Meta:
        database = DATABASE

class User(BaseModel, UserMixin):
	username = CharField(max_length=120, unique=True)
	email = CharField(max_length=120)
	password = CharField(max_length=200)
	joined_at = DateTimeField()
	id_admin = BooleanField(default=False)

	@classmethod
	def new_user(cls, username, email, password, joined_at=datetime.datetime.now(), is_admin=False):
		cls.create(
			username=username,
			email=email,
			password=password,
			joined_at=joined_at,
			is_admin=is_admin
				)

class Album(BaseModel):
	user = ForeignKeyField(User, related_name='albums')
	artist = CharField(max_length=250)
	album_title = CharField(max_length=500)
	genre = CharField(max_length=100)
	album_logo = CharField()
	release_date = IntegerField()
	is_favorite = BooleanField()

	@classmethod
	def new_album(cls, user, artist, album_title, genre, album_logo, release_date, is_favorite=False):
		cls.create(
			user=user,
			artist=artist,
			album_title=album_title,
			genre=genre,
			album_logo=album_logo,
			release_date=release_date,
			is_favorite=is_favorite
				)

class Song(BaseModel):
    album = ForeignKeyField(Album, related_name='songs')
    song_title = CharField(max_length=250)
    audio_file = CharField(default='')
    is_favorite = BooleanField()

    @classmethod
    def new_song(cls, album, song_title, audio_file, is_favorite=False):
    	cls.create(
    		album=album,
    		song_title=song_title,
    		audio_file=audio_file,
    		is_favorite=is_favorite
    		)

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Album, Song], safe=True)
	DATABASE.close()


