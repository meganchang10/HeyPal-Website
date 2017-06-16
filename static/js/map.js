/* HeyPal activities */
// locations = heypal activities
// name @ location

var map;

// Creates a map instance that renders on screen
function initMap(locations) {
"use strict";

  // Create a styles array to use with the map.
  var styles = [
    {
      featureType: 'water',
      stylers: [
        { color: '#3db7ff' }
      ]
    },{ // City Labels text outline
      featureType: 'administrative',
      elementType: 'labels.text.stroke',
      stylers: [
        { color: '#ffffff' },
        { weight: 3 }
      ]
    },{ // City Labels text
      featureType: 'administrative',
      elementType: 'labels.text.fill',
      stylers: [
        { color: '#2b3033' }
      ]
    },{
      featureType: 'road.highway',
      elementType: 'geometry.stroke',
      stylers: [
        { color: '#fff1d1' },
        { lightness: -40 }
      ]
    },{
      featureType: 'transit.station',
      stylers: [
        { weight: 9 },
        { hue: '#e85113' }
      ]
    },{
      featureType: 'road.highway',
      elementType: 'labels.icon',
      stylers: [
        { visibility: 'off' }
      ]
    },{
      featureType: 'water',
      elementType: 'labels.text.stroke',
      stylers: [
        { lightness: 100 }
      ]
    },{
      featureType: 'water',
      elementType: 'labels.text.fill',
      stylers: [
        { lightness: -100 }
      ]
    },{
      featureType: 'poi',
      elementType: 'geometry',
      stylers: [
        { visibility: 'on' },
        { color: '#f0e4d3' }
      ]
    },{
      featureType: 'road.highway',
      elementType: 'geometry.fill',
      stylers: [
        { color: '#fff1d1' },
        { lightness: 0 }
      ]
    }
  ];

  map = new google.maps.Map(document.getElementById("map"), {
    center: {lat: 34.415, lng: -119.72},
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    mapTypeControl: false,
    styles: styles
  });
}