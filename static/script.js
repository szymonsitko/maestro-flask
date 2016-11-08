
$(document).ready( function () {

	// LINKS TO THE API's
	var albumAPI = "/api/album/?ordering=-date_add"
	var songAPI = "/api/song/?ordering=-date_add"

	// TARGETING HTML ELEMENTS
	var $lastAlbum = $('#last-album-added');
	var $lastSong = $('#last-song-added');

	// GET THE LAST ALBUM ADDED
	$.getJSON(albumAPI, function (data) {

		// OBTAINING ALBUM API
		var album_date_add = data.objects[0].date_add
		var genre = data.objects[0].genre
		var album_title = data.objects[0].album_title
		var artist_name = data.objects[0].artist

		var lastAlbumInfo = "<p>" + "Album title" + "</p>"  + "<h4>" + album_title + "</h4>" +
		 "<p>" + "Artist: " + "</p>" + "<h4>" + artist_name + "</h4>" + "Genre" + "<p>" + genre + "</p>" +
		"<p>" + "Added: "+ "</p>" + "<p>" + album_date_add + "</p>"

		$lastAlbum.append(lastAlbumInfo)

	});

	$.getJSON(songAPI, function (data) {


		// OBTAINING SONG API
		var song_date_add = data.objects[0].date_add
		var song_title = data.objects[0].song_title

		var lastSongInfo = "<p>" + "Song title" + "</p>" + "<h4>" + song_title + "</h4>" + "<p>" + "Added at: " + "</p>"  + song_date_add
		console.log(lastSongInfo)
		$lastSong.append(lastSongInfo)

	});


});
