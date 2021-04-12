let map;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 33.97417, lng: -117.32800 },
    zoom: 15,
  });
}