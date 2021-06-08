/*
	Functions to get parameters from url and do what must be done
*/

/*
	this DisplayTaxids() function is the main one. It will display the taxids required.
	debug=[false]true => display the debug mode when true;
*/

//VARIABLES
var ServerAddress = "";
//Get url parameters
var queryString = window.location.search;
var urlParams = new URLSearchParams(queryString);

function onLoad() {	

	//language -> define address of basemap. english by default
	const lang = urlParams.get('lang')
	
	ServerAddress = lang=="en" ? "lifemap-fr.univ-lyon1.fr" : "lifemap.univ-lyon1.fr"
	setmaplayer('http://'+ServerAddress+'/retina_tiles/{z}/{x}/{y}.png');

	function setmaplayer(tolUrl) {
		if (map.hasLayer(tol)) map.removeLayer(tol)
		var tol = new L.TileLayer(tolUrl, {minZoom: 2, maxZoom: 42, detectRetina:false});
		map.addLayer(tol);
		map.setView([-5,0], 4);
	}

	//get taxid(s) (if any) 
	const tids = urlParams.get('tid')
	taxids = tids.split(",")

	//get zoom option. If true (the default) zoom to the taxids (if any)
	const zoom = urlParams.get('zoom') == "false" ? false : true;

	//get markers options. If true, (the default, markers are displayed
	const marks = urlParams.get('markers') == "false" ? false : true;

	//get tree option. If true (the default) the sub-tree with all taxa is displayed
	const tree = urlParams.get('tree') == "false" ? false : true;

	//get searchbar option. If true (the default), the searchbar is displayed
	const searchbar = urlParams.get('searchbar') == "false" ? false : true;

	//get font size for the jquery autocomplete widget, default is 11px
	let uifontsize = urlParams.get('uifontsize');
	try { uifontsize = parseInt(uifontsize, 10)} catch (e) {uifontsize = null}

	//get click on markers option. If true (the default) when the marker is clicked, information about taxon are displayed
	const clickableMarkers = urlParams.get('clickableMarkers') == "false" ? false : true;

	// get line color of tree (orange is the default)
	let colorLine = urlParams.get('colorLine');
	if (isColor(colorLine)) {
	} else if (isHexColor(colorLine)) {
		colorLine = "#" + colorLine
	} else {colorLine = 'orange'};

	// get line opacity of tree (default is 0.6)
	let opacityLine = urlParams.get('opacityLine');
	try {opacityLine = parseFloat(opacityLine)} catch (e) {opacityLine = 0.6}
	if (isNaN(opacityLine)) {opacityLine = 0.6};

	// get line weight of tree (default is 6)
	let weightLine = urlParams.get('weightLine');
	try {uifontsize = parseInt(uifontsize, 10)} catch (e) {weightLine = 6}
	if (typeof weightLine == "string") {weightLine = 6};

	//get debug option. If true (false is the default), it displays all options configuration
	const debug = urlParams.get('debug') == "true" ? true : false;

	if (tids) DisplayTaxids(pin1, taxids, zoom, marks, tree, clickableMarkers, colorLine, opacityLine, weightLine);
	DisplayInfo(lang, searchbar, uifontsize, clickableMarkers);

	// Please, add new params here for the debug mode
	let param = {"debug": debug, 
		"lang": lang,
		"tids": tids,
		"zoom": zoom,
		"marks": marks,
		"tree": tree,
		"searchbar": searchbar,
		"uifontsize": uifontsize,
		"clickableMarkers": clickableMarkers,
		"zoomButton": zoomButton,
		"colorLine": colorLine,
		"opacityLine": opacityLine,
		"weightLine": weightLine
	};

	debugDiv = document.getElementById("debug-mode");
	if (debug) {
		for (const [key, value] of Object.entries(param)) {
			debugDiv.innerHTML += 
			`
			${key + ": " + value} <br>
			`
		};	
	} else {debugDiv.parentNode.removeChild(debugDiv);}
}


function isColor(strColor) { // test if a string is a valid color
	var s = new Option().style;
	s.color = strColor;
	return s.color == strColor;
}

function isHexColor(hex) {
	return typeof hex === 'string'
		&& hex.length === 6
		&& !isNaN(Number('0x' + hex))
}