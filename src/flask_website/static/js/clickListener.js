// Function to handle feature click events and display real estate details in a pop-up
function addClickListener(map) {
    map.innerMap.data.addListener('click', function(event) {
        // Access property details from the clicked feature
        const idObject = event.feature.getProperty('OBJECTID');
        const ownerName = event.feature.getProperty('OWNERNAME');
        const parcelNo = event.feature.getProperty('PARCEL_NO');
        const blockNo = event.feature.getProperty('BLOCK_NO');
        const shapeArea = event.feature.getProperty('SHAPE.AREA');
        const estimatedPrice = event.feature.getProperty('ESTIMATED_PRICE'); // Assuming this field exists

        if (idObject) {
            // Construct the pop-up content
            const popupContent = `
                <div style="
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #fff;
                    padding: 10px;
                    border-radius: 12px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
                    width: 100%;
                    max-width: 280px;
                    box-sizing: border-box;
                ">
                    <!-- Parcel Number -->
                    <div style="text-align: center; font-size: 14px; font-weight: bold; color: #000;">
                        ${parcelNo || "Parcel Number"}
                    </div>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 10px 0;">

                    <!-- Details Section -->
                    <div style="
                        display: flex; 
                        flex-direction: column; 
                        gap: 12px;
                    ">
                        <div style="
                            display: flex;
                            align-items: center;
                            font-size: 13px;
                            color: #333;
                        ">
                            <img src="https://img.icons8.com/ios-filled/50/000000/user.png" alt="Owner Icon" style="width: 20px; margin-right: 10px;">
                            <span><strong>Owner Name:</strong> ${ownerName || "<em>Not available</em>"}</span>
                        </div>

                        <div style="
                            display: flex;
                            align-items: center;
                            font-size: 13px;
                            color: #333;
                        ">
                            <img src="https://img.icons8.com/ios-filled/50/000000/ruler.png" alt="Distance Icon" style="width: 20px; margin-right: 10px;">
                            <span><strong>Distance:</strong> ${shapeArea || "<em>Not available</em>"} m²</span>
                        </div>

                        <div style="
                            display: flex;
                            align-items: center;
                            font-size: 13px;
                            color: #333;
                        ">
                            <img src="https://img.icons8.com/ios-filled/50/000000/price-tag.png" alt="Price Icon" style="width: 20px; margin-right: 10px;">
                            <span><strong>Estimated Price:</strong> ${estimatedPrice || "<em>Not available</em>"}</span>
                        </div>
                    </div>

                    <!-- More Details Button -->
                    <div style="text-align: right; margin-top: 10px;">
                        <button id="more-details-btn" onclick="viewMoreDetails(${idObject})" style="
                            background-color: transparent;
                            color: #333;
                            border: none;
                            text-decoration: underline;
                            font-size: 13px;
                            cursor: pointer;
                        ">more ></button>
                    </div>
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
    window.location.href = `/property/${idObject}`;
}