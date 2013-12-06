var leaflet_config = {
	style: 997,
	key: "2ca42758fa584876a09900fc5b401400"
};

var get_tweets = function() {
	var tweets = new WebSocket("ws://" + window.location.host + "/tweets");

	tweets.onopen = function() {
		console.log("Connection open!");
	};

	tweets.onclose = function() {
		console.log("Connection closed!");
	};

	return tweets;
};

$(function() {
	// Make the map full screen
	$("#map").css({
		height: $(window).height(),
		width: $(window).width()
	});

	L.Icon.Default.imagePath = '/static/images'

	// Set inital view in Kent, Ohio
	var baseLayer = new L.TileLayer('http://{s}.tile.cloudmade.com/' + leaflet_config.key + '/' + leaflet_config.style + '/256/{z}/{x}/{y}.png', {
		maxZoom: 18
	});

	var markerLayer = new L.LayerGroup();

	var map = new L.Map('map', {
		center: [41.150556, -81.361111],
		zoom: 14,
		layers: [baseLayer, markerLayer]
	});

	var tweet_stream = get_tweets();

	tweet_stream.onmessage = function(event) {
		var t = jQuery.parseJSON(event.data);
		console.log(t);

		if (t.disconnect) {
			tweet_stream.close();
		}

		// Add a marker to the map
		var marker = new L
			.marker([t.latitude, t.longitude])
			.bindPopup(t.html)
			.addTo(markerLayer);
	};
});
