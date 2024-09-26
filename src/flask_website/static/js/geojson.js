// Function to load GeoJSON data on the map and set up click events to log specific details to console
async function loadGeoJSON() {
    try {
        // Fetch the GeoJSON file
        const response = await fetch('/static/geojson/TestPrint.geojson');
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

        // Add click listener for each feature (polygon) in the GeoJSON data
        map.innerMap.data.addListener('click', function(event) {
            // Log the entire feature object for inspection
            console.log("Clicked Feature:", event.feature);
           
            // Access properties directly from the feature
            const parcelNo = event.feature.getProperty('PARCEL_NO');
            const blockNo = event.feature.getProperty('BLOCK_NO');

            // Check if properties exist to avoid errors
            if (parcelNo || blockNo) {
                // Log the specified details of the clicked feature (estate) to the console
                console.log("Real Estate Details:");
                console.log("Parcel Number:", parcelNo || "Unknown");
                console.log("Block Number:", blockNo || "Unknown");
            } else {
                // Handle case where properties are missing
                console.warn("No properties found for this feature.");
            }
        });

    } catch (error) {
        console.error("Error loading GeoJSON data or setting up click event:", error);
    }
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', loadGeoJSON);
