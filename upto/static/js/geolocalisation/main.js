<script>
/*
function maPosition(position) {
  var infopos = "Position déterminée :\n";
  infopos += "Latitude : "+position.coords.latitude +"\n";
  infopos += "Longitude: "+position.coords.longitude+"\n";
  infopos += "Altitude : "+position.coords.altitude +"\n";
  document.getElementById("infoposition").innerHTML = infopos;

  var myLatLng = {lat: position.coords.latitude, lng: position.coords.longitude};

  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 8
  });

   var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Hello World!'
  });
}

if(navigator.geolocation)
{
    navigator.geolocation.getCurrentPosition(maPosition);

}
var map;
*/
var toto
if(navigator.geolocation)
{
    //navigator.geolocation.getCurrentPosition(initMap);
    navigator.geolocation.getCurrentPosition(getDistance);
}


function getDistance(position, DestinationLatitude, DestinationLongitude){
// 1 Get MyPosition

  var origin1 = {lat: p, lng: position.coords.longitude};
// test destosition.coords.latitude
  var destinationA = {lat: DestinationLatitude, lng: DestinationLongitude};
// 2 Calcul diff between origin and destination
  var geocoder = new google.maps.Geocoder;

  var service = new google.maps.DistanceMatrixService;
  service.getDistanceMatrix({
    origins: [origin1],
    destinations: [destinationA, destinationB], // here destinations array
    travelMode: google.maps.TravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC,
    avoidHighways: false,
    avoidTolls: false
  }, function(response, status) {
    if (status !== google.maps.DistanceMatrixStatus.OK) {
      alert('Error was: ' + status);
    } else {
      var originList = response.originAddresses;
      var destinationList = response.destinationAddresses;

      /*var showGeocodedAddressOnMap = function(asDestination) {
        var icon = asDestination ? destinationIcon : originIcon;
        return function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            map.fitBounds(bounds.extend(results[0].geometry.location));
            markersArray.push(new google.maps.Marker({
              map: map,
              position: results[0].geometry.location,
              icon: icon
            }));
          } else {
            alert('Geocode was not successful due to: ' + status);
          }
        };
      };*/

      for (var i = 0; i < originList.length; i++) {
        var results = response.rows[i].elements;
        for (var j = 0; j < results.length; j++) {
            results[j].distance.text
        }
      }
    }
  });
// 3 return float distance

}

function initMap(position, divNameMap) {
  var bounds = new google.maps.LatLngBounds;
  var markersArray = [];

  var origin1 = {lat: position.coords.latitude, lng: position.coords.longitude};
  var destinationA = '8 place Camoletti, 1204 Genève';
  var destinationB = 'Rue Chausse Coq 3, 1211 Genève';

  var destinationIcon = 'https://chart.googleapis.com/chart?' +
      'chst=d_map_pin_letter&chld=D|FF0000|000000';
  var originIcon = 'https://chart.googleapis.com/chart?' +
      'chst=d_map_pin_letter&chld=O|FFFF00|000000';
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 55.53, lng: 9.4},
    zoom: 10
  });
  var geocoder = new google.maps.Geocoder;

  var service = new google.maps.DistanceMatrixService;
  service.getDistanceMatrix({
    origins: [origin1],
    destinations: [destinationA, destinationB], // here destinations array
    travelMode: google.maps.TravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC,
    avoidHighways: false,
    avoidTolls: false
  }, function(response, status) {
    if (status !== google.maps.DistanceMatrixStatus.OK) {
      alert('Error was: ' + status);
    } else {
      var originList = response.originAddresses;
      var destinationList = response.destinationAddresses;
      var outputDiv = document.getElementById('output');
      outputDiv.innerHTML = '';
      deleteMarkers(markersArray);

      var showGeocodedAddressOnMap = function(asDestination) {
        var icon = asDestination ? destinationIcon : originIcon;
        return function(results, status) {
          if (status === google.maps.GeocoderStatus.OK) {
            map.fitBounds(bounds.extend(results[0].geometry.location));
            markersArray.push(new google.maps.Marker({
              map: map,
              position: results[0].geometry.location,
              icon: icon
            }));
          } else {
            alert('Geocode was not successful due to: ' + status);
          }
        };
      };

      for (var i = 0; i < originList.length; i++) {
        var results = response.rows[i].elements;
        geocoder.geocode({'address': originList[i]},
            showGeocodedAddressOnMap(false));
        for (var j = 0; j < results.length; j++) {
          geocoder.geocode({'address': destinationList[j]},
              showGeocodedAddressOnMap(true));
          outputDiv.innerHTML += originList[i] + ' to ' + destinationList[j] +
              ': ' + results[j].distance.text + ' in ' +
              results[j].duration.text + '<br>';
        }
      }
    }
  });
}

function deleteMarkers(markersArray) {
  for (var i = 0; i < markersArray.length; i++) {
    markersArray[i].setMap(null);
  }
  markersArray = [];
}

</script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDcRm_4W48Hu4OdwAHSaIfmWerF475RQA0&callback=initMap"
        async defer></script>


