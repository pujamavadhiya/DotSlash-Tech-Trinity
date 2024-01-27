document.addEventListener('DOMContentLoaded', function () {
    // Fetch and display points
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      var activeTab = tabs[0];
      chrome.tabs.sendMessage(activeTab.id, { action: 'getPoints' }, function (response) {
        displayPoints(response.points);
      });
    });
  
    // Function to display points
    function displayPoints(points) {
      var pointsList = document.getElementById('points-list');
      points.forEach(function (point) {
        var li = document.createElement('li');
        li.textContent = point;
        pointsList.appendChild(li);
      });
    }
  });
  