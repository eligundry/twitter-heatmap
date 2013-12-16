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
	var baseLayer = new L.TileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
		styleId: 997,
		key: "2ca42758fa584876a09900fc5b401400",
		maxZoom: 18
	});

	var markerLayer = new L.LayerGroup();

	var heatmap = new L.TileLayer.WebGLHeatMap({
		autoresize: true,
		opacity: 1,
		size: 5000
	});

	var map = new L.Map('map', {
		center: [41.150556, -81.361111],
		zoom: 14,
		layers: [baseLayer, markerLayer, heatmap]
	});

	// Layer Grouping
	L.control
		.layers({}, {
			"Heatmap": heatmap,
			"Tweets": markerLayer
		})
		.addTo(map);

	var tweet_stream = get_tweets();

	tweet_stream.onmessage = function(event) {
		var t = jQuery.parseJSON(event.data);

		// Add a marker to the map
		var marker = new L
			.marker([t.latitude, t.longitude])
			.bindPopup(t.html)
			.addTo(markerLayer);

		// Update the heatmap
		heatmap
			.addDataPoint(t.latitude, t.longitude, 10)
			.update();
	};
});
