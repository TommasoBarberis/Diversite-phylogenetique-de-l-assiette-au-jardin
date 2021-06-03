/*
	Functions for setting basemap options and define the appearance of markers.	
*/

var map = L.map('map', {zoomControl: false, attributionControl: false});

function setmaplayer(tolUrl) {
	if (map.hasLayer(tol)) map.removeLayer(tol)
	var tol = new L.TileLayer(tolUrl, {minZoom: 2, maxZoom: 42, detectRetina:false});
	map.addLayer(tol);
	map.setView([-5,0], 4);
}
var markers = new L.FeatureGroup();
let markerList = [];
//VISUAL ELEMENTS (LOGOS, IMAGES, etc...)
var pin1 = L.icon({
	iconUrl: 'img/pin1.png',
	iconSize:     [18, 25], // size of the icon
	iconAnchor:   [9, 30], // point of the icon which will correspond to marker's location
});
