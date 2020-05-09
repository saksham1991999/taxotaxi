	//Map for Contact Us Page
	jQuery(document).ready(function($) {
	"use strict";
		// Display our google map when window is loaded
		google.maps.event.addDomListener(window, 'load', init);
		google.maps.event.addDomListener(window, 'load', init_map2);
	
		function init() {
			var mapOptions = {
				// Set zoom level for the map
				zoom: 11,

				// Set latitude and longitude to center the map 
				center: new google.maps.LatLng(40.6700, -73.9400), // New York

				//Set map style for your map
				styles:[{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#419d8c"},{"lightness":"-43"}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#419d8c"},{"lightness":"-70"}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#419d8c"},{"lightness":"-17"}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#419d8c"},{"lightness":"-66"},{"weight":1.2}]},{"featureType":"administrative","elementType":"labels.text","stylers":[{"lightness":"-63"}]},{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"lightness":"43"},{"color":"#419d8c"}]},{"featureType":"administrative","elementType":"labels.text.stroke","stylers":[{"color":"#419d8c"},{"lightness":"-69"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-51"}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-54"}]},{"featureType":"poi","elementType":"labels.text.fill","stylers":[{"color":"#419d8c"}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#419d8c"},{"lightness":"-23"}]},{"featureType":"road","elementType":"labels.text.stroke","stylers":[{"color":"#419d8c"},{"lightness":"-66"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#419d8c"},{"lightness":"-62"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#419d8c"},{"lightness":"-70"},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-60"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-54"}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-59"}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#419d8c"},{"lightness":"-61"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#419d8c"},{"lightness":"-45"}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"color":"#419d8c"},{"lightness":"-62"}]}]
			};

			// Get the HTML DOM element that will contain your map 
			var mapElement = document.getElementById('tj-map');
			if( mapElement!==null ){
				// Create the Google Map using our element and options defined above
				var map = new google.maps.Map(mapElement, mapOptions);

				// Add marker to your map
				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(40.6700, -73.9400),
					map: map,
					title: 'Find Us',
					icon: 'images/map-marker.png'
				});
				marker.setAnimation(google.maps.Animation.BOUNCE);
			}
			
		}
		
		
		function init_map2() {
		
			var mapOptions2 = {
				// Set zoom level for map
				zoom: 11,
				// Set latitude and longitude to center the map 
				center: new google.maps.LatLng(40.6700, -73.9400), // New York

				//Set map style for your map
				styles:[ { "featureType": "all", "elementType": "labels.text.fill", "stylers": [ { "color": "#ffffff" } ] }, { "featureType": "all", "elementType": "labels.text.stroke", "stylers": [ { "color": "#4b3829" } ] }, { "featureType": "administrative.neighborhood", "elementType": "all", "stylers": [ { "visibility": "on" } ] }, { "featureType": "administrative.neighborhood", "elementType": "geometry.stroke", "stylers": [ { "visibility": "on" } ] }, { "featureType": "administrative.neighborhood", "elementType": "labels.icon", "stylers": [ { "visibility": "on" } ] }, { "featureType": "landscape", "elementType": "all", "stylers": [ { "color": "#382f2d" }, { "visibility": "on" }, { "saturation": "0" }, { "lightness": "0" } ] }, { "featureType": "landscape", "elementType": "geometry", "stylers": [ { "color": "#382f2d" } ] }, { "featureType": "landscape.man_made", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#4a4140" } ] }, { "featureType": "landscape.man_made", "elementType": "geometry", "stylers": [ { "visibility": "on" }, { "color": "#4a4140" } ] }, { "featureType": "landscape.man_made", "elementType": "geometry.fill", "stylers": [ { "visibility": "on" }, { "color": "#4a4140" } ] }, { "featureType": "landscape.natural", "elementType": "all", "stylers": [ { "visibility": "simplified" }, { "color": "#4a4140" } ] }, { "featureType": "landscape.natural", "elementType": "geometry", "stylers": [ { "visibility": "on" } ] }, { "featureType": "landscape.natural.landcover", "elementType": "all", "stylers": [ { "visibility": "off" }, { "color": "#d3b9b9" } ] }, { "featureType": "landscape.natural.landcover", "elementType": "geometry", "stylers": [ { "visibility": "off" }, { "color": "#7c5656" } ] }, { "featureType": "landscape.natural.landcover", "elementType": "geometry.fill", "stylers": [ { "visibility": "off" }, { "color": "#8a3d3d" } ] }, { "featureType": "landscape.natural.terrain", "elementType": "all", "stylers": [ { "visibility": "off" }, { "color": "#a63c3c" } ] }, { "featureType": "poi", "elementType": "geometry.fill", "stylers": [ { "color": "#392718" } ] }, { "featureType": "poi", "elementType": "labels.text", "stylers": [ { "visibility": "off" } ] }, { "featureType": "poi", "elementType": "labels.icon", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road", "elementType": "geometry.fill", "stylers": [ { "color": "#4a3728" }, { "visibility": "off" } ] }, { "featureType": "road", "elementType": "geometry.stroke", "stylers": [ { "color": "#4a3728" } ] }, { "featureType": "road", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "all", "stylers": [ { "color": "#8e7974" }, { "visibility": "on" } ] }, { "featureType": "road.highway", "elementType": "geometry", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.highway", "elementType": "geometry.fill", "stylers": [ { "color": "#ff0000" }, { "visibility": "off" } ] }, { "featureType": "road.highway.controlled_access", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#584f4e" } ] }, { "featureType": "road.highway.controlled_access", "elementType": "geometry.fill", "stylers": [ { "color": "#ff0000" }, { "visibility": "off" } ] }, { "featureType": "road.highway.controlled_access", "elementType": "labels", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.arterial", "elementType": "all", "stylers": [ { "color": "#584f4e" }, { "visibility": "on" } ] }, { "featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [ { "visibility": "off" }, { "hue": "#ff0000" } ] }, { "featureType": "road.local", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "road.local", "elementType": "geometry.fill", "stylers": [ { "color": "#ff0000" }, { "visibility": "off" } ] }, { "featureType": "transit", "elementType": "all", "stylers": [ { "visibility": "off" } ] }, { "featureType": "water", "elementType": "all", "stylers": [ { "visibility": "on" }, { "color": "#cbdade" } ] }, { "featureType": "water", "elementType": "geometry", "stylers": [ { "color": "#392718" } ] }, { "featureType": "water", "elementType": "geometry.fill", "stylers": [ { "color": "#7d93a8" } ] } ]
			};

			// Get the HTML DOM element that will contain your map 
			var mapElement2 = document.getElementById('tj-map2');
			if( mapElement2!==null ){
				// Create the Google Map using our element and options defined above
				var map2 = new google.maps.Map(mapElement2, mapOptions2);

				// Add a marker
				var marker2 = new google.maps.Marker({
					position: new google.maps.LatLng(40.6700, -73.9400),
					map: map2,
					title: 'Find Us',
					icon: 'images/map-marker.png'
				});
				marker2.setAnimation(google.maps.Animation.BOUNCE);
			}
			
		}
	
	});