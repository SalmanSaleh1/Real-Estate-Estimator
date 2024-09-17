// Function to initialize the Google Maps components
async function init() {
  try {
      // Wait for the custom elements to be defined
      await customElements.whenDefined('gmp-map');

      // Select the map, marker, and place picker elements
      const map = document.querySelector('gmp-map');
      const marker = document.querySelector('gmp-advanced-marker');
      const placePicker = document.querySelector('gmpx-place-picker');
      const infowindow = new google.maps.InfoWindow();

      // Check if required elements are found
      if (!map || !marker || !placePicker) {
          console.error("Failed to find map, marker, or place picker elements.");
          return;
      }

      // Set map options (e.g., disable map type control)
      map.innerMap.setOptions({
          mapTypeControl: false,
          mapId: 'YOUR_MAP_ID' // Add your Map ID here
      });

      // Set default location to Buraydah, Qassim
      const defaultLocation = { lat: 26.3267, lng: 43.9734 }; // Buraydah, Qassim coordinates
      map.center = defaultLocation;
      map.zoom = 13;
      marker.position = defaultLocation;

      // Add event listener for place changes
      placePicker.addEventListener('gmpx-placechange', () => {
          const place = placePicker.value;

          // Handle cases where no location is found
          if (!place || !place.location) {
              window.alert("No details available for input: '" + place.name + "'");
              infowindow.close();
              marker.position = null;
              return;
          }

          // Adjust map view based on the place details
          if (place.viewport) {
              map.innerMap.fitBounds(place.viewport);
          } else {
              map.center = place.location;
              map.zoom = 17;
          }

          // Update marker position and infowindow content
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

      // Load and display GeoJSON data
      loadGeoJSON();
  } catch (error) {
      console.error("Error initializing map:", error);
  }
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', init);
