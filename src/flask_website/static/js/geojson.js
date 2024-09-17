// Function to load and display GeoJSON data on the map
async function loadGeoJSON() {
    try {
        // Fetch the GeoJSON file
        const response = await fetch('/static/geojson/TestPrint.geojson');
        const geojsonData = await response.json();

        // Get the map element
        const map = document.querySelector('gmp-map');

        // Check if the map is loaded
        if (!map || !map.innerMap) {
            console.error("Map is not loaded.");
            return;
        }

        // Add GeoJSON data to the map
        map.innerMap.data.addGeoJson(geojsonData);

        // Style the GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'yellow',
            strokeWeight: 2
        });
    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    }
}
