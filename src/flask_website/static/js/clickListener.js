function addClickListener(map) {
    map.innerMap.data.addListener('click', function(event) {
        // Access property details from the clicked feature
        const idObject = event.feature.getProperty('OBJECTID');
        const ownerName = event.feature.getProperty('OWNERNAME') || "Not available";
        const parcelNo = event.feature.getProperty('PARCEL_NO') || "Parcel Number";
        const shapeArea = event.feature.getProperty('SHAPE.AREA') || "Not available";
        const estimatedPrice = event.feature.getProperty('ESTIMATED_PRICE') || "Not available";

        // Get the pop-up template from HTML and make a clone to edit
        const popupTemplate = document.getElementById('popup-template').cloneNode(true);
        popupTemplate.style.display = 'block'; // Make it visible

        // Populate data into the pop-up
        popupTemplate.querySelector('.parcel-number').textContent = parcelNo;
        popupTemplate.querySelector('#popup-owner').textContent = ownerName;
        popupTemplate.querySelector('#popup-distance').textContent = shapeArea;
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
