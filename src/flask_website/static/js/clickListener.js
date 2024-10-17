// Function to handle feature click events and display real estate details in a pop-up
function addClickListener(map) {
    map.innerMap.data.addListener('click', function(event) {
        // Access property details from the clicked feature
        const idObject = event.feature.getProperty('OBJECTID');
        const ownerName = event.feature.getProperty('OWNERNAME');
        const parcelNo = event.feature.getProperty('PARCEL_NO');
        const blockNo = event.feature.getProperty('BLOCK_NO');
        const shapeArea = event.feature.getProperty('SHAPE.AREA');

        if (idObject) {
            // Construct the pop-up content
            const popupContent = `
                <div>
                    <h4>Real Estate Details</h4>
                    <p><strong>Owner Name:</strong> ${ownerName || "Not available"}</p>
                    <p><strong>Parcel No:</strong> ${parcelNo || "Not available"}</p>
                    <p><strong>Block No:</strong> ${blockNo || "Not available"}</p>
                    <p><strong>Shape Area:</strong> ${shapeArea || "Not available"} m²</p>
                    <button id="more-details-btn" onclick="viewMoreDetails(${idObject})">More Details</button>
                </div>
            `;

            // Set the content and position of the pop-up (InfoWindow)
            infoWindow.setContent(popupContent);
            infoWindow.setPosition(event.latLng);
            infoWindow.open(map.innerMap); // Open the pop-up on the map
        } else {
            console.warn("id_object not available.");
        }
    });
}

// Utility function to format numbers to a specified decimal place
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined || isNaN(num)) {
        return "Not available";
    }
    return Number(num).toFixed(decimals);
}

// Function to handle 'More Details' button click and redirect to the property details page
function viewMoreDetails(idObject) {
    // Redirect to the property details page using the id_object
    window.location.href = `/property-details/${idObject}`;
}
