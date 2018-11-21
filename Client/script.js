var map = {};
var markers =[];

function initMap() {
		map = new google.maps.Map(document.getElementById("map"), {
	});
}

function test() {
	initMarkers();
	console.log(tweets[0].tweet[0].tweet_location[1]);
	console.log(tweets[1].tweet[0].tweet_location[1]);
}
 
function initMarkers(){
	bounds = new google.maps.LatLngBounds();
	for(var i = 0; i < tweets.length; i++) {
		loc = new google.maps.LatLng(tweets[i].tweet[0].tweet_location[1],tweets[i].tweet[0].tweet_location[0]);
		bounds.extend(loc);
		var marker = new google.maps.Marker({
			position: loc,
			map:map,
			title: tweets[i].tweet[0].tweet_text
		});
	}
	map.fitBounds(bounds);
	map.panToBounds(bounds);
}
