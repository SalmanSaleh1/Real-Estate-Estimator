// Function to initialize the map
function initMap() {
    var map = L.map('map').setView([23.8859, 45.0792], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var marker;

    function onMapClick(e) {
        if (marker) {
            map.removeLayer(marker);
        }

        marker = L.marker(e.latlng).addTo(map)
            .bindPopup("You clicked the map at " + e.latlng.toString())
            .openPopup();
    }

    map.on('click', onMapClick);

    // Add the Leaflet Control Geocoder to the map
    var searchControl = L.Control.geocoder({
        defaultMarkGeocode: false,
        geocodingQueryParams: {
            limit: 5
        }
    }).addTo(map);

    // Listen for the markgeocode event and add a marker
    searchControl.on('markgeocode', function (e) {
        if (marker) {
            map.removeLayer(marker);
        }

        if (e.geocode) {
            marker = L.marker(e.geocode.center).addTo(map)
                .bindPopup(e.geocode.name)
                .openPopup();
        } else {
            alert("No results found");
        }
    });
}

// Call the initMap function when the document is ready
document.addEventListener('DOMContentLoaded', function () {
    initMap();
});

// Reload the map every 10 seconds
setInterval(function () {
    initMap();
}, 10000);
