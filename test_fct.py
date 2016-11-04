def allowed_song_extensions(filename):

	extensions = ['mp3', 'wav', 'oog']

	file = filename.split('.')
	print(file[1])
	if file[1] not in extensions:
		return False
	else:
		return True

def length_field(form, field):

	length = field.split(':')
	print(length[0], length[1])
	if (length[0] and length[1]) is not True:
		return ValidationError


print(length_field('3:20'))