let infoWindow;  // Declare the infoWindow variable globally

// Function to open an IndexedDB database
function openIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("GeoJSONData", 1);
        
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains("geojson")) {
                db.createObjectStore("geojson", { keyPath: "id" });
            }
        };

        request.onsuccess = (e) => {
            resolve(e.target.result);
        };

        request.onerror = (e) => {
            reject(e);
        };
    });
}

// Function to get GeoJSON from IndexedDB
async function getGeoJSONFromDB() {
    const db = await openIndexedDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction("geojson", "readonly");
        const store = transaction.objectStore("geojson");
        const request = store.get(1);  // Assuming we only store one item with id=1

        request.onsuccess = (e) => {
            resolve(e.target.result ? e.target.result.data : null);
        };

        request.onerror = (e) => {
            reject(e);
        };
    });
}

// Function to save GeoJSON to IndexedDB
async function saveGeoJSONToDB(geojsonData) {
    const db = await openIndexedDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction("geojson", "readwrite");
        const store = transaction.objectStore("geojson");
        const request = store.put({ id: 1, data: geojsonData });

        request.onsuccess = () => {
            resolve();
        };

        request.onerror = (e) => {
            reject(e);
        };
    });
}

// Function to load and style the GeoJSON data
async function loadGeoJSON(map) {
    const loadingIndicator = document.getElementById('loading-indicator');

    try {
        // Show loading indicator
        loadingIndicator.style.display = 'block';

        // Check if the GeoJSON data is cached in IndexedDB
        let geojsonData = await getGeoJSONFromDB();
        if (!geojsonData) {
            // If not cached, fetch the GeoJSON file
            const response = await fetch('/static/geojson/TestPrint1.json');

            // Check if the response is OK
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            geojsonData = await response.json();

            // Cache the GeoJSON data in IndexedDB
            await saveGeoJSONToDB(geojsonData);
        }

        // Add GeoJSON data to the map
        map.innerMap.data.addGeoJson(geojsonData);

        // Style the GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'black',
            strokeWeight: 1
        });

        console.log("GeoJSON data loaded and styled successfully.");

        // Initialize the InfoWindow object (must be done after the map is ready)
        infoWindow = new google.maps.InfoWindow();

        // Call the function to add the click listener after GeoJSON data is loaded
        addClickListener(map);  // Call the click listener with the map reference

    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    } finally {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }
}