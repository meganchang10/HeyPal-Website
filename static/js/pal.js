function ViewModel() {
"use strict";

  var self = this;

  // Copies the locations values into a knockout observable array
  self.notMyPals = ko.observableArray(notMyPals);

  // Gets user input from searchfield
  self.query = ko.observable('');
  self.notMyPal = ko.computed(function () {
  return ko.utils.arrayFilter(self.notMyPals(), function (notMyPal) {
  var result = notMyPal.name.toLowerCase().indexOf(self.query().toLowerCase());

  // str.indexOf(searchValue)
  // If search value is an empty string, result = -1
  // If search value is not empty, result = 0
  if (result === -1) {
      notMyPal.setVisible(false);
      } else {
      notMyPal.setVisible(true);
      }
      return result >= 0;
      });
  });

}