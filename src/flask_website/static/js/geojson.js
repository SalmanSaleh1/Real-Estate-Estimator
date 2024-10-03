let infoWindow;  // Declare the infoWindow variable globally

// Function to load and style the GeoJSON data
async function loadGeoJSON(map) {
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
        addClickListener(map);  // Call the click listener with the map reference

    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }
}
