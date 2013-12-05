var leaflet_config = {
	style: 997,
	key: "2ca42758fa584876a09900fc5b401400"
};

var heatmap_config = {
	radius: 20,
	opacity: 0.5,
	gradient: {
		0.45: "rgb(0,0,255)",
		0.55: "rgb(0,255,255)",
		0.65: "rgb(0,255,0)",
		0.95: "yellow",
		1.0: "rgb(255,0,0)"
	}
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

	var heatmap = new L.TileLayer.HeatMap(heatmap_config);
	var heatmap_data = {
		max: 140,
		data: []
	};

	var map = new L.Map('map', {
		center: [41.150556, -81.361111],
		zoom: 14,
		layers: [baseLayer, markerLayer, heatmap]
	});

	var tweet_stream = get_tweets();

	tweet_stream.onmessage = function(event) {
		var t = jQuery.parseJSON(event.data);
		console.log(t);

		if (t.disconnect) {
			tweet_stream.close();
		}

		if ((t.geo != null) && (t.geo.length == 2)) {
			// Add a marker to the map
			var marker = new L
				.marker(t.geo)
				.bindPopup(t.html)
				.addTo(markerLayer);

			// Reload the Twitter oEmbed widget
			twttr.widgets.load();

			// Update heatmap data
			heatmap_data.data.push({
				lat: t.geo[0],
				lon: t.geo[1],
				value: t.weight
			});

			heatmap.setData(heatmap_data);
		}
	};
});
