// Function to load GeoJSON data on the map and set up click events to log specific details to console
async function loadGeoJSON() {
    // Show a loading indicator
    showLoadingIndicator();

    try {
        // Fetch the GeoJSON file with caching (optional)
        const response = await fetch('/static/geojson/TestPrint.geojson');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
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

        // Add click listener for each feature (polygon) in the GeoJSON data
        map.innerMap.data.addListener('click', debounce(function(event) {
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
        }, 200)); // Debounce with 200ms delay

    } catch (error) {
        console.error("Error loading GeoJSON data or setting up click event:", error);
    } finally {
        // Hide the loading indicator
        hideLoadingIndicator();
    }
}

// Debounce function to limit the rate at which a function can fire
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

// Example functions for showing/hiding loading indicator
function showLoadingIndicator() {
    // Logic to show loading indicator
    console.log("Loading GeoJSON data...");
}

function hideLoadingIndicator() {
    // Logic to hide loading indicator
    console.log("Loading complete.");
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', loadGeoJSON);
