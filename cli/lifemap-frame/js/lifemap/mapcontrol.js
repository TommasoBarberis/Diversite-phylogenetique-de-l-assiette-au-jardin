/*
	Functions for setting basemap options and define the appearance of markers.	
*/


/*
zoomButton=[true]false => display zoom buttons
*/


//get zoom button option. If true (the default), it displays zoom buttons
const zoomButton = urlParams.get('zoomButton') == "false" ? false : true;

var map = L.map('map', {zoomControl: zoomButton, attributionControl: true});

var markers = new L.FeatureGroup();
let markerList = [];
//VISUAL ELEMENTS (LOGOS, IMAGES, etc...)
var pin1 = L.icon({
	iconUrl: 'img/pin1.png',
	iconSize:     [18, 25], // size of the icon
	iconAnchor:   [9, 30], // point of the icon which will correspond to marker's location
})
