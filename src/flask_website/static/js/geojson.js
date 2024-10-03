let infoWindow;  // Declare the infoWindow variable globally to clickListener.js

// Function to load and style the GeoJSON data
async function loadGeoJSON() {
    const loadingIndicator = document.getElementById('loading-indicator');

    try {
        // Show loading indicator
        loadingIndicator.style.display = 'block';

        // Fetch the GeoJSON file
        const response = await fetch('/static/geojson/TestPrint.json');

        // Check if the response is OK
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const geojsonData = await response.json();

        // Get the map element
        const map = document.querySelector('gmp-map');

        // Check if the map is loaded
        if (!map || !map.innerMap) {
            console.error("Map is not loaded.");
            return;
        }

        // Add GeoJSON data to the map
        map.innerMap.data.addGeoJson(geojsonData);

        // Style the GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'black',
            strokeWeight: 1
        });

        console.log("GeoJSON data loaded and styled successfully.");

        // Initialize the InfoWindow object (must be done after the map is ready)
        infoWindow = new google.maps.InfoWindow();

        // Call the function to add the click listener after GeoJSON data is loaded
        addClickListener(map);

    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', loadGeoJSON);