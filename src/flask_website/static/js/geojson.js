let infoWindow; // Declare the infoWindow variable globally
let cachedGeoJSONData = null; // Global variable to store GeoJSON

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

async function loadGeoJSON(map) {
    const loadingIndicator = document.getElementById('loading-indicator');

    try {
        loadingIndicator.style.display = 'block';

        cachedGeoJSONData = await getGeoJSONFromDB();
        if (!cachedGeoJSONData) {
            const response = await fetch('/static/geojson/Formated_final.json');
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            cachedGeoJSONData = await response.json();

            saveGeoJSONToDB(cachedGeoJSONData).catch(console.error);
        }

        // Add all features to the map
        map.innerMap.data.addGeoJson(cachedGeoJSONData);

        // Style GeoJSON data
        map.innerMap.data.setStyle({
            fillColor: 'yellow',
            strokeColor: 'black',
            strokeWeight: 1,
        });

        console.log(`Loaded and styled ${cachedGeoJSONData.features.length} features.`);

        // Add the click listener for interacting with features
        addClickListener(map);
    } catch (error) {
        console.error("Error loading GeoJSON data:", error);
    } finally {
        loadingIndicator.style.display = 'none';
    }
}

function applyFilters(map, geojsonData) {
    const minPrice = parseFloat(document.getElementById("minPrice").value) || 0;
    const maxPrice = parseFloat(document.getElementById("maxPrice").value) || Infinity;
    const propertyType = document.getElementById("propertyType").value;
    const minShapeArea = parseFloat(document.getElementById("minShapeArea").value) || 0;
    const maxShapeArea = parseFloat(document.getElementById("maxShapeArea").value) || Infinity;

    console.log(`Filters: MinPrice=${minPrice}, MaxPrice=${maxPrice}, PropertyType=${propertyType}, MinShapeArea=${minShapeArea}, MaxShapeArea=${maxShapeArea}`);

    // Clear existing data on the map
    map.innerMap.data.forEach((feature) => {
        map.innerMap.data.remove(feature);
    });

    const filteredFeatures = geojsonData.features.filter((feature) => {
        const { ESTIMATED_PRICE, property_type } = feature.properties;
        const shapeArea = parseFloat(feature.properties["SHAPE.AREA"] || "0");

        console.log(`Feature: Price=${ESTIMATED_PRICE}, Type=${property_type}, Area=${shapeArea}`);

        return (
            (ESTIMATED_PRICE >= minPrice && ESTIMATED_PRICE <= maxPrice) &&
            (!propertyType || property_type === propertyType) &&
            (shapeArea >= minShapeArea && shapeArea <= maxShapeArea)
        );
    });

    map.innerMap.data.addGeoJson({ type: "FeatureCollection", features: filteredFeatures });

    map.innerMap.data.setStyle({
        fillColor: 'yellow',
        strokeColor: 'black',
        strokeWeight: 1,
    });

    console.log(`Applied filters. Showing ${filteredFeatures.length} properties.`);
}

function removeFilters(map, geojsonData) {
    console.log("Removing filters...");
    console.log("GeoJSON Data:", geojsonData);

    // Clear existing data on the map
    map.innerMap.data.forEach((feature) => {
        map.innerMap.data.remove(feature);
    });

    console.log("Cleared existing features.");

    // Add all features back to the map
    if (geojsonData && geojsonData.features) {
        map.innerMap.data.addGeoJson(geojsonData);
        console.log(`Re-added ${geojsonData.features.length} features to the map.`);
    } else {
        console.error("GeoJSON data is missing or invalid.");
    }

    // Re-apply styles
    map.innerMap.data.setStyle({
        fillColor: 'yellow',
        strokeColor: 'black',
        strokeWeight: 1,
    });
}


// Hook up filters to the map
document.getElementById("applyFilters").addEventListener("click", async () => {
    const map = document.querySelector("gmp-map");
    if (!cachedGeoJSONData) {
        cachedGeoJSONData = await getGeoJSONFromDB();
        if (!cachedGeoJSONData) return;
    }

    applyFilters(map, cachedGeoJSONData);
});

document.getElementById("removeFilters").addEventListener("click", async () => {
    const map = document.querySelector("gmp-map");
    if (!cachedGeoJSONData) {
        cachedGeoJSONData = await getGeoJSONFromDB();
        if (!cachedGeoJSONData) {
            console.error("Cached GeoJSON data is missing.");
            return;
        }
    }

    removeFilters(map, cachedGeoJSONData);

    // Optionally clear the filter input fields
    document.getElementById("minPrice").value = "";
    document.getElementById("maxPrice").value = "";
    document.getElementById("propertyType").value = "";
    document.getElementById("minShapeArea").value = "";
    document.getElementById("maxShapeArea").value = "";
});