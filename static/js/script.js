var leaflet_config = {
	style: 997,
	key: "2ca42758fa584876a09900fc5b401400"
};

$(function() {
	// Make the map full screen
	$("#map").css({
		height: $(window).height(),
		width: $(window).width()
	});

	var map = L.map('map').setView([41.150556,-81.361111], 13);

	L.tileLayer('http://{s}.tile.cloudmade.com/' + leaflet_config.key + '/' + leaflet_config.style + '/256/{z}/{x}/{y}.png', {
		maxZoom: 18
	}).addTo(map);
});
