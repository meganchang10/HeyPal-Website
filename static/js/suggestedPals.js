function ViewModel() {
"use strict";

  var self = this;

  // Copies the locations values into a knockout observable array
  self.pals = ko.observableArray(pals);

  // Gets user input from searchfield
  self.query = ko.observable('');
  self.listItem = ko.computed(function () {
  return ko.utils.arrayFilter(self.pals(), function (listResult) {
  var result = listResult.name.toLowerCase().indexOf(self.query().toLowerCase());

  // str.indexOf(searchValue)
  // If search value is an empty string, result = -1
  // If search value is not empty, result = 0
  if (result === -1) {
      listResult.setVisible(false);
      } else {
      listResult.setVisible(true);
      }
      return result >= 0;
      });
  });

}