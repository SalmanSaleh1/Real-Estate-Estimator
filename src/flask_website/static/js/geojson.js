// Function to load GeoJSON data on the map and set up click events to log specific details to console
async function loadGeoJSON() {
    const loadingIndicator = document.getElementById('loading-indicator');

    try {
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        console.log("Loading indicator shown.");

        // Fetch the GeoJSON file
        const response = await fetch('/static/geojson/TestPrint.geojson');
        console.log("Fetch response received.");

        // Check if the response is OK
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const geojsonData = await response.json();
        console.log("GeoJSON data loaded successfully:", geojsonData);

        // Get the map element
        const map = document.querySelector('gmp-map');
        console.log("Map element found:", map);

        // Check if the map is loaded
        if (!map || !map.innerMap) {
            console.error("Map is not loaded.");
            return;
        }

        // Add GeoJSON data to the map
        map.innerMap.data.addGeoJson(geojsonData);
        console.log("GeoJSON data added to the map.");

        // Style the GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'black',
            strokeWeight: 1
        });
        console.log("GeoJSON data styled successfully.");

        // Add click listener for each feature (polygon) in the GeoJSON data
        map.innerMap.data.addListener('click', function(event) {
            // Access properties directly from the feature
            const parcelNo = event.feature.getProperty('PARCEL_NO');
            const blockNo = event.feature.getProperty('BLOCK_NO');

            // Combine Parcel Number and Block Number in a single console log
            if (parcelNo || blockNo) {
                console.log(`Real Estate Details: Parcel Number: ${parcelNo || "Not available"}, Block Number: ${blockNo || "Not available"}`);
            } else {
                console.warn("No properties found for this feature.");
            }
        });

    } catch (error) {
        console.error("Error loading GeoJSON data or setting up click event:", error);
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
        console.log("Loading indicator hidden.");
    }
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', loadGeoJSON);
