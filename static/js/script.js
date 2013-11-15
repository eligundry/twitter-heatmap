var leaflet_config = {
	style: 997,
	key: "2ca42758fa584876a09900fc5b401400"
};

var get_tweets = function() {
	var tweets = new WebSocket("ws://" + window.location.host + "/tweets");

	tweets.onopen = function() {
		console.log("Connection open!");
	}

	tweets.onmessage = function(msg) {
		console.log(msg);
	}

	tweets.onclose = function() {
		console.log("Connection closed!");
	}

	return tweets;
};

$(function() {
	// Make the map full screen
	$("#map").css({
		height: $(window).height(),
		width: $(window).width()
	});

	var map = L.map('map').setView([41.150556,-81.361111], 13);
	var markerLayer = new L.LayerGroup();

	L.tileLayer('http://{s}.tile.cloudmade.com/' + leaflet_config.key + '/' + leaflet_config.style + '/256/{z}/{x}/{y}.png', {
		maxZoom: 18
	}).addTo(map);

	var heatmap = new L.TileLayer.HeatCanvas({}, {});

	map.addLayer(heatmap);
});
