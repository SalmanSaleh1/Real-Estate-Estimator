function addClickListener(map) {
    map.innerMap.data.addListener('click', async function(event) {
        // Access property details from the clicked feature
        const idObject = event.feature.getProperty('OBJECTID');
        const ownerName = event.feature.getProperty('OWNERNAME') || "Not available";
        const parcelNo = event.feature.getProperty('PARCEL_NO') || "Parcel Number";
        const shapeArea = event.feature.getProperty('SHAPE.AREA') || "Not available";

        // Get the pop-up template from HTML and make a clone to edit
        const popupTemplate = document.getElementById('popup-template').cloneNode(true);
        popupTemplate.style.display = 'block'; // Make it visible

        // Populate static data into the pop-up
        popupTemplate.querySelector('.parcel-number').textContent = parcelNo;
        popupTemplate.querySelector('#popup-owner').textContent = ownerName;
        popupTemplate.querySelector('#popup-distance').textContent = shapeArea;

        // Fetch the estimated price from the ML API
        let estimatedPrice = "Not available";
        try {
            const response = await fetch(`/api/predict/${idObject}`);
            if (response.ok) {
                const data = await response.json();
                if (data.predicted_price) {
                    // Format estimated price with commas and two decimal places
                    const formattedPrice = new Intl.NumberFormat('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }).format(data.predicted_price);
                    
                    // Add currency symbol to the right
                    estimatedPrice = `${formattedPrice} SAR`;
                }
            }
        } catch (error) {
            console.error("Error fetching estimated price:", error);
        }

        // Update the estimated price in the pop-up
        popupTemplate.querySelector('#popup-price').textContent = estimatedPrice;

        // Set up 'More Details' button with direct event binding
        const moreDetailsBtn = popupTemplate.querySelector('.more-details-btn');
        moreDetailsBtn.addEventListener('click', function() {
            viewMoreDetails(idObject);
        });

        // Set the content and position of the pop-up (InfoWindow)
        infoWindow.setContent(popupTemplate); // Pass the entire element, not innerHTML
        infoWindow.setPosition(event.latLng);
        infoWindow.open(map.innerMap); // Open the pop-up on the map
    });
}

// Function to handle 'More Details' button click and redirect to the property details page
function viewMoreDetails(idObject) {
    // Redirect to the property details page using the id_object
    window.location.href = `/property/${idObject}`;
}
