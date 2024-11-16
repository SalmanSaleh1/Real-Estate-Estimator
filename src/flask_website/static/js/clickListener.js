function addClickListener(map) {
    map.innerMap.data.addListener('click', async function(event) {
        const idObject = event.feature.getProperty('OBJECTID');
        const district = event.feature.getProperty('DISTRICT') || "Not available";
        const parcelNo = event.feature.getProperty('PARCEL_NO') || "Parcel Number";
        const shapeArea = event.feature.getProperty('SHAPE.AREA') || "Not available";

        const popupTemplate = document.getElementById('popup-template').cloneNode(true);
        popupTemplate.style.display = 'block';

        // Set content for the popup
        popupTemplate.querySelector('.parcel-number').textContent = parcelNo;
        popupTemplate.querySelector('#popup-owner').textContent = district;
        popupTemplate.querySelector('#popup-distance').textContent = shapeArea;

        // Fetch price dynamically and update the styling based on the range
        let estimatedPrice = "Not available";
        try {
            const response = await fetch(`/api/predict/${idObject}`);
            if (response.ok) {
                const data = await response.json();
                if (data.predicted_price) {
                    const formattedPrice = new Intl.NumberFormat('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    }).format(data.predicted_price);
                    
                    estimatedPrice = `${formattedPrice} SAR`;
                    const priceElement = popupTemplate.querySelector('#popup-price');

                    if (data.predicted_price <= 100000) {
                        priceElement.style.color = "green";
                    } else if (data.predicted_price <= 300000) {
                        priceElement.style.color = "orange";
                    } else {
                        priceElement.style.color = "red";
                    }
                }
            }
        } catch (error) {
            console.error("Error fetching estimated price:", error);
        }

        const priceElement = popupTemplate.querySelector('#popup-price');
        priceElement.textContent = estimatedPrice;

        const moreDetailsBtn = popupTemplate.querySelector('.more-details-btn');
        moreDetailsBtn.addEventListener('click', function() {
            viewMoreDetails(idObject);
        });

        infoWindow.setContent(popupTemplate);
        infoWindow.setPosition(event.latLng);
        infoWindow.open(map.innerMap);
    });
}

function viewMoreDetails(idObject) {
    window.location.href = `/property/${idObject}`;
}
