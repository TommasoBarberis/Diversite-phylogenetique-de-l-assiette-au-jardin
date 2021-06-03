/*
lang=[en]fr: in the follow code, this option allow to request the right server (between fr and en server);
searchbar=[true]false => if true it display the searchbar;
uifontsize=[11]int => when the searchbar is displayed it allows to modify font size of suggestions;
clickableMarkers=[true]false => if true, markers become clickable and they open a modal box with information.
*/

var DisplayInfo = function(lang, searchbar=false, uifontsize, clickableMarkers) {
	if (uifontsize!=null) {
		var s = document.styleSheets[1];
		adjustCSSRules(".ui-autocomplete.ui-widget", "font-size: "+uifontsize+"px", s);
	}
	searchDiv = document.getElementById("searchbar");
	if (searchbar) {
		// inject HTML needed for the searchbar
		searchDiv.innerHTML += `
		<!--RESIZE BUTTON-->
		<div class=" text-right"><i id="reducerightblock" class="glyphicon glyphicon-minus-sign" style="padding:5px; color:#b4c3e0; cursor: pointer;"></i>
		</div>	
		<!--IMAGE ON TOP-->
		<div id="logo" class="img.center">
			<img class="center" src = "img/LMicon1.png" width="50%">
		</div>
		<!--SIMPLE SEARCH DIV-->
		<div id="mainsearch" class="container-fluid" style="margin: 10px 10px 0px 10px; padding:0px; z-index:10;">
			<div class="btn-group" style="width:100%;">
				<span id="route" class="fa fa-level-up" title="Search routes between taxa or clades"></span>
				<input id="searchinput" type="search" class="form-control" style="width:100%; height:40px;" placeholder="Search species, clade, ...">
				
			</div>
		</div>
		`
		
		// fixes the width of suggestions
		jQuery.ui.autocomplete.prototype._resizeMenu = function () {
			var ul = this.menu.element;
			ul.outerWidth(this.element.outerWidth());
		};


		let SPfocus; // marker that will be add by the searchbar selection
		$(function() {
			var str;
			var URL_PREFIX = lang=="fr" ? "http://lifemap-fr.univ-lyon1.fr/solr/taxo/suggesthandler?suggest.q=" : "http://lifemap.univ-lyon1.fr/solr/taxo/suggesthandler?suggest.q=";
			var URL_PREFIX_FINAL = lang=="fr" ? "http://lifemap-fr.univ-lyon1.fr/solr/taxo/select?q=taxid:" : "http://lifemap.univ-lyon1.fr/solr/taxo/select?q=taxid:";
			var URL_SUFFIX = "&wt=json";

			$("#searchinput").autocomplete({
				source : function(request, response) {
					var URL = URL_PREFIX + $("#searchinput").val() + URL_SUFFIX;
					$.ajax({
						url : URL,
						success : function(data) {
							var step1=data.suggest.mySuggester[$("#searchinput").val()];
							try {var docs = JSON.stringify(step1.suggestions);} catch(e) {};
							var jsonData = JSON.parse(docs);
							jsonData.sort(function(a,b) {
								a1 = a.term.split("|")[0].replace(/<b>/g,"").replace(/<\/b>/g,"");
								b1 = b.term.split("|")[0].replace(/<b>/g,"").replace(/<\/b>/g,"");
								return(a1.length-b1.length);
							});
							response($.map(jsonData, function(value, key) {
								str = value.term;
								str=str.split("|");
								var issp = str[2];
								issp = issp.replace(/<b>/g,"");
								issp = issp.replace(/<\/b>/g,"");
								issp = issp.replace(" ","");
								issp = issp.replace(/[\x00-\x2f\x3a-\x40]/g,"");
								var taxid = str[3];
								taxid = taxid.replace(/<b>/g,"");
								taxid = taxid.replace(/<\/b>/g,"");
								taxid = taxid.replace(" ","");
								taxid = taxid.replace(/[\x00-\x2f\x3a-\x40]/g,"");
								var spname = str[0];
								spname=spname.replace(/<b>/g,"");
								spname=spname.replace(/<\/b>/g,"");
								var commonname = str[1];
								commonname=commonname.replace(/<b>/g,"");
								commonname=commonname.replace(/<\/b>/g,"");
								var renderval = spname + commonname;
								labOK = str[0].replaceAll("<b>", "").replaceAll("</b>", "") //+ str[1] + str[2]
								// if ((issp==="species")||(issp==="subspecies")) {
								// 	labOK = "<div style='padding: 20px;'><span class=\"scinameItalic\">" + str[0] + "</span><span class=\"commonname\">" + str[1] + "</span><br><span class=\"rank\" >" + str[2] + "</span></div>";			
								// }
								// else {
								// 	labOK = "<div style='padding: 20px;'><span class=\"sciname\">" + str[0] + "</span><span class=\"commonname\">" + str[1] + "</span><br><span class=\"rank\">" + str[2] + "</span></div>";
								// };
								return {
									label: labOK,
									value: renderval,
									taxidfinal: taxid,
									spname: spname,
									commonname: commonname,
									rank: issp	
								}
							}));
						},
						dataType : 'jsonp',
						jsonp : 'json.wrf'
					});
				},

				minLength : '1',
				autoFocus: true,
				html: true,
				scroll: true,
				highlightClass: "bold-text",
				focus: function() {
						// prevent value inserted on focus
						return false;
				},
				select: function(e, ui) {
					var taxidok = ui.item.taxidfinal;
					$("#searchinput").blur();						
					var URL = URL_PREFIX_FINAL + taxidok + URL_SUFFIX;

					$.ajax({
						url : URL,
						success : function(data) {
							var docs = JSON.stringify(data.response.docs);
							var jsonData = JSON.parse(docs);
							map.setView(jsonData[0].coordinates, jsonData[0].zoom[0]-8);
							latlong = new L.LatLng(jsonData[0].lat[0], jsonData[0].lon[0]);
							SPfocus = L.marker(latlong,{icon: pin1, opacity:1});
							markerList.push(SPfocus);
							if (clickableMarkers) {
								SPfocus.on("click", function (){
									let comname = "";
									try {comname = jsonData[0].common_name[0]} catch (e) {};
									markofun(jsonData[0].taxid[0], jsonData[0].sci_name[0], comname, jsonData[0].rank[0]);
								})
							}
							SPfocus.addTo(map);
						},
						dataType : 'jsonp',
						jsonp : 'json.wrf'
					});	    
				}
			})
		});
	}
}


function adjustCSSRules(selector, props, sheets){
    // get stylesheet(s)
    if (!sheets) sheets = [...document.styleSheets];
    else if (sheets.sup){    // sheets is a string
        let absoluteURL = new URL(sheets, document.baseURI).href;
        sheets = [...document.styleSheets].filter(i => i.href == absoluteURL);
    }
    else sheets = [sheets];  // sheets is a stylesheet

    // CSS (& HTML) reduce spaces in selector to one.
    selector = selector.replace(/\s+/g, ' ');
    const findRule = s => [...s.cssRules].reverse().find(i => i.selectorText == selector)
    let rule = sheets.map(findRule).filter(i=>i).pop()

    const propsArr = props.sup
        ? props.split(/\s*;\s*/).map(i => i.split(/\s*:\s*/)) // from string
        : Object.entries(props);                              // from Object

    if (rule) for (let [prop, val] of propsArr){
        // rule.style[prop] = val; is against the spec, and does not support !important.
        rule.style.setProperty(prop, ...val.split(/ *!(?=important)/));
    }
    else {
        sheet = sheets.pop();
        if (!props.sup) props = propsArr.reduce((str, [k, v]) => `${str}; ${k}: ${v}`, '');
        sheet.insertRule(`${selector} { ${props} }`, sheet.cssRules.length);
    }
}


let markofun = function(taxid, spname, comname, rank) {
	// taxi = taxid;
	// spna = spname;
	// comna = comname;
	comname = comname + " ";
	spname = spname + " ";

	let modal = document.getElementById("myModal");
	modal.innerHTML += `
	<!-- Modal content -->
	<div class="modal-content">
	  <div class="modal-header">
		<span class="close">&times;</span>
		<div id="modaltitle" class="modal-title"></div>
	  </div>
		
	  	<div class="modalbody">
	 		<div id="modalbody-text"></div>
		</div>
		
	  <div class="modal-footer">
		<button type="button" id="close-button-footer" data-dismiss="modal">Close</button> 
	  </div>
	</div>
	`

	$('#modaltitle').empty();
	$('#modalbody-text').empty();	
	$('#modalbody-pict').empty();
	$('#modalbody-links').empty();	
	text = "<div style='font-style:center; color:grey;'>No article concerning this group on <i class='fa fa-wikipedia-w'></i>wikipedia.</div>";
	pict = "";
	if (spname!="Root") {
		getWikiDesc(spname).then(function(resu){
			if (resu!=null) {
				if (resu.thumbnail!==undefined) {
					//we add the image to the modal
					// <div><a href="https://en.wikipedia.org/wiki/' + spname + '" target="_blank"></a>
					pict = '<div id="modalbody-pict"><img id="wiki-image" src ='+resu.thumbnail.source+' width="100%"></div>'
					// </a></div>'
					$('#modalbody-text').append(pict);
					$('#modalbody-pict').css({
						width: '30%'
					});
				}
				else {
					pict = "<div style='padding:10px; font-size:xx-small; text-align:center; color:grey;'> No picture associated to this articlke on Wikipedia. Click <a href='https://en.wikipedia.org/wiki/" + spname + "' target='_blank'>here</a> if you want to upload one now.</div>";
					$('#modalbody-text').append(pict);
				}
				text = resu.extract;
				text += "<div style='padding-bottom:10px;text-align:left; font-size:xx-small; float:left'><a href='https://en.wikipedia.org/wiki/" + spname + "' target='_blank'>more on <i class='fa fa-wikipedia-w'></i>wikipedia</a><br></div>";
				$('#modalbody-text').append(text);	
			}
			else {
				$('#modalbody-text').append(text);
				$('#modalbody-text').append(pict);
			}
		})
	}
	else {
		$('#modalbody-links').append("<img src='img/galaxy.jpg' width='100%'>");
	}
	if ((rank==="species")||(rank===" species ")) {
		$('#modaltitle').append("<span class='scinameItalic2'>"+spname+"</span>");	
	}
	else {
		$('#modaltitle').append("<span class='sciname2'>"+spname+"</span>");	
	}
	$('#modaltitle').append("<span class='commonname2'>"+comname+"</span>");
	$('#modaltitle').append("<span class='rank2'>"+rank+"</span>");	
	// Get the <span> element that closes the modal
	let spanClose = document.getElementsByClassName("close")[0];
	
	// When the user clicks the marker, open the modal 
	modal.style.display = "block";

	// When the user clicks on <span> (x), close the modal
	spanClose.onclick = function() {
		modal.style.display = "none";
		modal.innerHTML = "";
	}

	let closeButton = document.getElementById("close-button-footer");
	closeButton.onclick = function() {
		modal.style.display = "none";
		modal.innerHTML = "";
	}
	
	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
		if (event.target == modal) {
			modal.style.display = "none";
			modal.innerHTML = "";
		}
	}
	// $('#myModal').modal('show');
	// $('#viewfullancestry').on("click", function() {
	// 	taxidFrom = taxi;
	// 	taxidTo = "1";
	// 	$("#myModal").modal("hide");
	// 	$("#mainsearch").hide();					
	// 	$('#searchinput2').val(spna + comna);
	// 	$('#searchinput3').val('Root');
	// 	$("#route-top").show();
	// 	mrcaroute();
	// })
};


function getWikiDesc (spname) {
	var res = '';
	return $.getJSON(wikiurl="https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts|pageimages&titles="+spname+"&redirects&exsentences=3&piprop=original|thumbnail|name&pithumbsize=400&callback=?").then(function(data){
		var page = data.query.pages;
		key = Object.keys(page)[0]
		if (key!="-1") {
			res = page[key];
			return res;
		}
		else {
			return null;
		}
	});
}