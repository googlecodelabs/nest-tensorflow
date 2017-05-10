// Copyright 2017 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
$(function() {
    $('#fetch-image').bind('click', function(event) {
        event.preventDefault();

        // Disable the button
        var button = $(this);
        button.toggleClass('active');
        button.toggleClass('disabled');
        button.find('i.fa').toggle();

        // Placeholder image displayed during processing
        var resultsCard = $('.card#results');
        var resultsCardImage = resultsCard.find('img');
        resultsCardImage.attr('src', resultsCardImage.data('placeholder-url'));

        // Fetch the new image and results
        var apiURL = button.data('api-url');
        $.get(apiURL, function(data) {

            if (data.error) {
                // We have an error to display
                var alert =  $('<div/>', {
                    class: 'alert alert-danger',
                    role:  'alert',
                    html:  data.error
                });
                resultsCard.find('p').html(alert);
                return;
            }

            // We have good data

            // Sort the results DESC
            var sortable = [];
            for (var key in data.results) {
              sortable.push([key, data.results[key]]);
            }
            var sorted = sortable.sort(function(a, b) {
              return b[1] - a[1];
            });

            // Set the Image Src to the Nest Snapshot URL
            resultsCardImage.attr('src', data.image_url);

            // Build the classification list
            var list = $('<ul/>');
            sorted.forEach(function(r) {
              list.append($('<li/>', {
                  html: r[0] + ": " + (r[1]*100.0).toFixed(2) + "%"
              }));
            });
            resultsCard.find('p').html(list);
        }).always(function() {
          // Enable the button
          button.toggleClass('active');
          button.toggleClass('disabled');
          button.find('i.fa').toggle();
        });
    });
});
