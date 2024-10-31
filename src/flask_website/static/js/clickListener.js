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
                <div style="
        font-family: Arial, sans-serif;
        color: #333;
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        width: 100%;
        max-width: 280px;
        box-sizing: border-box;
    ">
        <h4 style="margin-bottom: 10px; color: #007BFF; text-align: center; font-size: 16px;">Real Estate Details</h4>
        
        <div style="
            display: flex; 
            flex-direction: column; 
            gap: 6px;
        ">
            <div style="
                background-color: #fff;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 13px;
                box-sizing: border-box;
            ">
                <strong>Owner Name:</strong>
                <p style="margin: 3px 0;">${ownerName || "<em>Not available</em>"}</p>
            </div>

            <div style="
                background-color: #fff;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 13px;
                box-sizing: border-box;
            ">
                <strong>Parcel No:</strong>
                <p style="margin: 3px 0;">${parcelNo || "<em>Not available</em>"}</p>
            </div>

            <div style="
                background-color: #fff;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 13px;
                box-sizing: border-box;
            ">
                <strong>Block No:</strong>
                <p style="margin: 3px 0;">${blockNo || "<em>Not available</em>"}</p>
            </div>

            <div style="
                background-color: #fff;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 13px;
                box-sizing: border-box;
            ">
                <strong>Shape Area:</strong>
                <p style="margin: 3px 0;">${shapeArea || "<em>Not available</em>"} m²</p>
            </div>
        </div>

        <div style="text-align: center; margin-top: 10px;">
            <button id="more-details-btn" onclick="viewMoreDetails(${idObject})" style="
                background-color: #007BFF;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 7px 10px;
                cursor: pointer;
                font-size: 13px;
                width: 100%;
                box-sizing: border-box;
            ">More Details</button>
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
