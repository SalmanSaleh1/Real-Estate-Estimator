async function init() {
    try {
      // Wait for the custom elements to be defined
      await customElements.whenDefined('gmp-map');
      const map = document.querySelector('gmp-map');
      const marker = document.querySelector('gmp-advanced-marker');
      const placePicker = document.querySelector('gmpx-place-picker');
      const infowindow = new google.maps.InfoWindow();
  
      if (!map || !marker || !placePicker) {
        console.error("Failed to find map, marker, or place picker elements.");
        return;
      }
  
      // Set map options
      map.innerMap.setOptions({
        mapTypeControl: false
      });
  
      // Add event listener for place changes
      placePicker.addEventListener('gmpx-placechange', () => {
        const place = placePicker.value;
        if (!place || !place.location) {
          window.alert("No details available for input: '" + place.name + "'");
          infowindow.close();
          marker.position = null;
          return;
        }
  
        if (place.viewport) {
          map.innerMap.fitBounds(place.viewport);
        } else {
          map.center = place.location;
          map.zoom = 17;
        }
  
        marker.position = place.location;
        infowindow.setContent(
          `<div>
            <strong>${place.displayName}</strong><br>
            <span>${place.formattedAddress}</span><br>
            <span>Place ID: ${place.placeId}</span><br>
            <span>Coordinates: ${place.location.lat}, ${place.location.lng}</span>
          </div>`
        );
        infowindow.open(map.innerMap, marker);
      });
    } catch (error) {
      console.error("Error initializing map:", error);
    }
  }
  
  document.addEventListener('DOMContentLoaded', init);
  