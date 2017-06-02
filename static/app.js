var currentInfoWindow;


function ViewModel() {
"use strict";

  var self = this;
  self.markers = [];

  // Copies the locations values into a knockout observable array
  self.locations = ko.observableArray(locations);

  // Marker/icon style
  var defaultIcon = makeMarkerIcon('ff9000');
  var highlightedIcon = makeMarkerIcon('42f4f4');

  // Creates a marker for each location in the locations array
  self.locations().forEach(function(location) {
    var marker = new google.maps.Marker({
      position: location.position,
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
              '" target="_blank">Visit Website</a>' + '<br>';
          } else {
            websiteHTMLtag = "";
          }

          // Check that a website is on file at FourSquare. If so, create a photo tag for the url
          // if not, do not add website option to info window
          var photos = data.response.venue.photos.groups[0].items[0];
          var photoHTMLtag;

          if (photos !== undefined) {
            photoHTMLtag = '<img src="' +
            photos.prefix + "100x100" + photos.suffix +
            '">' + '<br>';
          } else {
            photoHTMLtag = "";
          }

          // Info window contents, call upon contentString function to create appropriate HTML tags
          var infoWindow = new google.maps.InfoWindow({
                content: contentString({
                  title: data.response.venue.name,
                  formattedAddress: data.response.venue.location.formattedAddress,
                  websiteHTMLtag: websiteHTMLtag,
                  photoHTMLtag: photoHTMLtag
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
      if (location.name) {
          map.setZoom(15);
          map.panTo(location.position); // Focuses map view on selected marker when list item is clicked
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
  var result = listResult.name.toLowerCase().indexOf(self.query().toLowerCase());
  console.log(result);

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
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 id="firstHeading" class="firstHeading">' +
        location.title +
      '</h1>'+
      '<div id="bodyContent">'+
        '<p>' +
        location.formattedAddress[0] + '<br>' +
        location.formattedAddress[1] + '<br>' +
        location.formattedAddress[2] + '<br>' +
        '</p>' +
      '</div>' +
      location.photoHTMLtag +
      location.websiteHTMLtag +
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




