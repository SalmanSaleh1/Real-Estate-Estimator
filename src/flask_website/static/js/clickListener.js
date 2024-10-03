// Function to handle feature click events and display real estate details
function addClickListener(map) {
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

                    // Create content for the InfoWindow (pop-up)
                    const infoContent = `
                        <div>
                            <h4>Real Estate Details</h4>
                            <p><strong>Parcel No (Raw):</strong> ${parcelNo}</p>
                            <p><strong>Block No (Raw):</strong> ${blockNo || "Not available"}</p>

                            <!-- Placeholder for API details after processing -->
                            <p><strong>Parcel No (API Processed):</strong> ${apiData.parcel_no}</p>
                            <p><strong>Block No (API Processed):</strong> ${apiData.block_no || "Not available"}</p>

                            <!-- More details button -->
                            <button id="more-details-btn" onclick="showMoreDetails()">More Details</button>
                        </div>
                    `;

                    // Set the content and position of the InfoWindow
                    infoWindow.setContent(infoContent);
                    infoWindow.setPosition(event.latLng);
                    infoWindow.open(map.innerMap);  // Open the pop-up on the map

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
}

// Function to handle 'More Details' button click
function showMoreDetails() {
    alert("More details functionality can be implemented here.");
}
