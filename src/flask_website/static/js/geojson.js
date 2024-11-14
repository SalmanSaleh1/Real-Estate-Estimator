let infoWindow; // Declare the infoWindow variable globally

// Open IndexedDB
function openIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("GeoJSONData", 1);

        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains("geojson")) {
                db.createObjectStore("geojson", { keyPath: "id" });
            }
        };

        request.onsuccess = (e) => resolve(e.target.result);
        request.onerror = reject;
    });
}

// Get GeoJSON from IndexedDB
async function getGeoJSONFromDB() {
    try {
        const db = await openIndexedDB();
        const transaction = db.transaction("geojson", "readonly");
        const store = transaction.objectStore("geojson");
        return new Promise((resolve, reject) => {
            const request = store.get(1);
            request.onsuccess = (e) => resolve(e.target.result?.data || null);
            request.onerror = reject;
        });
    } catch (error) {
        console.error("Error accessing IndexedDB:", error);
        return null;
    }
}

// Save GeoJSON to IndexedDB
async function saveGeoJSONToDB(geojsonData) {
    try {
        const db = await openIndexedDB();
        const transaction = db.transaction("geojson", "readwrite");
        const store = transaction.objectStore("geojson");
        return new Promise((resolve, reject) => {
            const request = store.put({ id: 1, data: geojsonData });
            request.onsuccess = resolve;
            request.onerror = reject;
        });
    } catch (error) {
        console.error("Error saving data to IndexedDB:", error);
    }
}

// Load and Style GeoJSON Data
async function loadGeoJSON(map) {
    const loadingIndicator = document.getElementById('loading-indicator');

    let geojsonData;

    try {
        // Show loading indicator
        loadingIndicator.style.display = 'block';

        // Start both IndexedDB retrieval and fetch in parallel
        const dbPromise = getGeoJSONFromDB();
        const fetchPromise = fetch('/static/geojson/TestPrint_new.json');

        // Attempt to get cached data
        geojsonData = await dbPromise;

        // If no cached data, wait for the fetch response
        if (!geojsonData) {
            const response = await fetchPromise;

            // Validate response
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            geojsonData = await response.json();

            // Save to IndexedDB asynchronously
            saveGeoJSONToDB(geojsonData).catch(console.error);
        }

        // Add GeoJSON data to the map
        const geoJsonFeatures = map.innerMap.data.addGeoJson(geojsonData);

        // Style GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'black',
            strokeWeight: 1,
        });

        console.log(`Loaded and styled ${geoJsonFeatures.length} features successfully.`);

        // Initialize InfoWindow lazily
        if (!infoWindow) infoWindow = new google.maps.InfoWindow();

        // Add click listener if not already added
        if (!map.innerMap.__clickListenerAdded) {
            addClickListener(map);
            map.innerMap.__clickListenerAdded = true; // Flag to prevent duplicate listeners
        }
    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }
}