
var currentInfoWindow;


function ViewModel() {
"use strict";

  var self = this;
  self.markers = [];

  // Copies the locations values into a knockout observable array
  self.locations = ko.observableArray(locations);

  // Marker/icon style
  var defaultIcon = makeMarkerIcon('ff8800');
  var highlightedIcon = makeMarkerIcon('ff0000');

  // Creates a marker for each location in the locations array
  self.locations().forEach(function(location) {
    var position = {lat:location.lat, lng:location.lng};
    var marker = new google.maps.Marker({
      position: position,
      map: map,
      title: location.title,
      URL: location.shortUrl,
      icon: defaultIcon,
      animation: google.maps.Animation.DROP
    });

    location.marker = marker;
    marker.setVisible(true);

    // Pushes each marker into the markers array
    self.markers.push(marker);

    // Two event listeners - one for mouseover, one for mouseout,
    // to change the colors back and forth.
    marker.addListener('mouseover', function() {
      this.setIcon(highlightedIcon);
    });

    marker.addListener('mouseout', function() {
      this.setIcon(defaultIcon);
    });


    /* Foursquare client info */
    var CLIENT_ID = '?client_id=14Q2ET3UCW2QZMIGEZG1JAJQJDTJ5HUVHYM2CL2HGMGS0G3B';
    var CLIENT_SECRET = '&client_secret=QQ41HPQQ2ETSRUW30NVV3TWLKNF2CD1KHZNQK2V4RJPQKV4P';
    var version = '&v=20170531';

  /* Foursquare API ajax request */
    $.ajax({
        type: "GET",
        dataType: 'json',
        cache: false,
        url: 'https://api.foursquare.com/v2/venues/' + location.venue_id + CLIENT_ID + CLIENT_SECRET + version,
        async: true,
        success: function(data) {

          // Check that website is on file at FourSquare. If so, create an HTML a tag for the url
          // if not, do not add website option to info window
          var website = data.response.venue.url;
          var websiteHTMLtag;

          if (website !== undefined) {
            websiteHTMLtag = '<a href="' +
              website +
              '" target="_blank">Visit Website</a>';
          } else {
            websiteHTMLtag = "";
          }

          // Check that a website is on file at FourSquare. If so, create a photo tag for the url
          // if not, do not add website option to info window. For loop to get a few photos
          var photos = data.response.venue.photos.groups[0].items;
          var photoHTMLtag;

          if (photos !== undefined) {
            photoHTMLtag = '<div class="w3-content w3-display-container">';
            var i;
              for (i = 0; i < 5; i++) {
                var img_tag = '<img class="mySlides" src="' +
              photos[i].prefix + "300x300" + photos[i].suffix + '" style="width:100%">';
                  photoHTMLtag += img_tag;
              }
            photoHTMLtag += '</div>';
          } else {
            photoHTMLtag = "";
          }

          // Info window contents, call upon contentString function to create appropriate HTML tags
          var infoWindow = new google.maps.InfoWindow({
                maxWidth: 200,
                maxHeight: 400,
                content: contentString({
                  title: data.response.venue.name,
                  formattedAddress: data.response.venue.location.formattedAddress,
                  websiteHTMLtag: websiteHTMLtag,
                  photoHTMLtag: photoHTMLtag,
                  phone: data.response.venue.contact.formattedPhone
                })
          });

        location.infoWindow = infoWindow;

        location.marker.addListener('click', function () {
            if (currentInfoWindow !== undefined) {
                    currentInfoWindow.close();
            }
            currentInfoWindow = location.infoWindow;
            location.infoWindow.open(map, this);

            // Bounce markers when clicked with timer function to stop bounce after 1500 miliseconds
            location.marker.setAnimation(google.maps.Animation.BOUNCE);
            setTimeout(function () {
                    location.marker.setAnimation(null);
            }, 1500);
        });
    },

    // If there is an error in loading foursquare data, alert user
    error: function(data) {
          alert("Could not load data from foursquare.");
    }
    });
  });

  // Adds click functionality to location list items
  self.listViewClick = function(location) {
      if (location.fullName) {
          map.setZoom(15);
          var position = {lat:location.lat, lng:location.lng};
          map.panTo(position); // Focuses map view on selected marker when list item is clicked

          /* Offsets pan so that marker is not centered anymore, it is offset so that the
             info window can be more centered or when the screen is large enough, the
             to include both the list and the map, we can center the info window in the
             remaining map space */
          var mq = window.matchMedia('(max-width: 550px)');
          if(mq.matches) {
            // If width is smaller than 550px
            map.panBy(0,-225);
          } else {
            // If width is larger than 550px
            map.panBy(-400,-225);
          }

          location.marker.setAnimation(google.maps.Animation.BOUNCE);
           if (currentInfoWindow !== undefined) {
                         currentInfoWindow.close();
                      }
              currentInfoWindow = location.infoWindow;
              currentInfoWindow.open(map, location.marker); // Opens info window for clicked marker
      }
      setTimeout(function() {
          location.marker.setAnimation(null);
      }, 1500);
  };

  // Gets user input from searchfield
  self.query = ko.observable('');
  self.listItem = ko.computed(function () {
  return ko.utils.arrayFilter(self.locations(), function (listResult) {
  var result = listResult.fullName.toLowerCase().indexOf(self.query().toLowerCase());

  // str.indexOf(searchValue)
  // If search value is an empty string, result = -1
  // If search value is not empty, result = 0
  if (result === -1) {
      listResult.marker.setVisible(false);
      } else {
      listResult.marker.setVisible(true);
      }
      return result >= 0;
      });
  });

}


function contentString(location) {
  "use strict";
  return (
    '<div id="content">'+
      '<h2>' +
        location.title +
      '</h2>'+
      '<div id="bodyContent">'+
        '<p>' +
        location.formattedAddress[0] + '<br>' +
        location.formattedAddress[1] + '<br>' +
        '</p>' +
        '<p>' +
        location.websiteHTMLtag + '<br>' +
        location.phone + '</p>' +
      '</div>' +
      location.photoHTMLtag + '<br>' +
    '</div>');
}


// This function takes in a color, and then creates a new marker
// icon of that color. The icon will be 21 px wide by 34 high, have an origin
// of 0, 0 and be anchored at 10, 34).
function makeMarkerIcon(markerColor) {
  var markerImage = new google.maps.MarkerImage(
    'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
    '|40|_|%E2%80%A2',
    new google.maps.Size(21, 34),
    new google.maps.Point(0, 0),
    new google.maps.Point(10, 34),
    new google.maps.Size(21,34));
  return markerImage;
}




