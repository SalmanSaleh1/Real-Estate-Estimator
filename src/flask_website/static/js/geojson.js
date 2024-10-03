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
        map.innerMap.data.addListener('click', async function(event) {
            // Access properties directly from the feature
            const parcelNo = event.feature.getProperty('PARCEL_NO');
            const blockNo = event.feature.getProperty('BLOCK_NO');

            // Check if parcelNo and blockNo are valid
            if (parcelNo) {
                console.log(`Real Estate Details: Parcel Number: ${parcelNo}, Block Number: ${blockNo || "Not available"}`);

                // Prepare data for the API call
                const payload = {
                    parcel_no: parcelNo,
                    block_no: blockNo ? blockNo : "N/A"  // Fallback if blockNo is missing
                };

                // Call the API to send the parcel and block numbers
                try {
                    const apiResponse = await fetch('/api/test', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    });

                    const apiData = await apiResponse.json();
                    if (apiResponse.ok) {
                        console.log(`API Response: Updated Parcel No: ${apiData.parcel_no}, Updated Block No: ${apiData.block_no}`);
                    } else {
                        console.error(`API Error: ${apiData.error}`);
                    }
                } catch (error) {
                    console.error("Error calling the API:", error);
                }

            } else {
                console.warn("Parcel Number not available.");
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
