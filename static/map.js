
/* HeyPal activities */
var locations = [
  {id: 1, name: 'Bottomless Mimosas @ Brewhouse', position: {lat: 34.4120404, lng: -119.69582990000004}, venue_id: "4b4b96b8f964a5202ba126e3"},
  {id: 2, name: 'Beach Day @ Leadbetter Beach', position: {lat: 34.40234809999999, lng: -119.69934519999998}, venue_id: "4b12f540f964a5209d9123e3"},
  {id: 3, name: 'Wine Tasting @ Deep Sea Tasting Room', position: {lat: 34.4099896, lng: -119.68556949999999}, venue_id: "4e220b75fa761d671082ff1b"},
  {id: 4, name: 'Appetizers @ Milk and Honey', position: {lat: 34.42256559999999, lng: -119.70546179999997}, venue_id: "4b51496af964a520d64927e3"},
  {id: 5, name: "Dancing @ O'Malley's", position: {lat: 34.4172957, lng: -119.6964284}, venue_id: "4aad9191f964a520e36020e3"},
];


var map;

// Creates a map instance that renders on screen
function initMap() {
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