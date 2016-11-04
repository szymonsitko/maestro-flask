def allowed_song_extensions(filename):

	extensions = ['mp3', 'wav', 'oog']

	file = filename.split('.')
	print(file[1])
	if file[1] not in extensions:
		return False
	else:
		return True

print(allowed_song_extensions('koparka.html'))