// Function to initialize the Google Maps components
async function init() {
  try {
      // Wait for the custom elements to be defined
      await customElements.whenDefined('gmp-map');
  
      // Select the map element only (removed the place picker element)
      const map = document.querySelector('gmp-map');
  
      // Check if the map element is found
      if (!map) {
          console.error("Failed to find map element.");
          return;
      }
  
      // Set map options (e.g., disable map type control, set Map ID)
      map.innerMap.setOptions({
          mapTypeControl: false,
          mapId: 'YOUR_MAP_ID' // Add your Map ID here
      });
  
      // Set default location to Buraydah, Qassim
      const defaultLocation = { lat: 26.3267, lng: 43.9734 }; // Buraydah, Qassim coordinates
      map.center = defaultLocation;
      map.zoom = 13;
  
  } catch (error) {
      console.error("Error initializing map:", error);
  }
}

// Initialize the map when the DOM content is loaded
document.addEventListener('DOMContentLoaded', init);
