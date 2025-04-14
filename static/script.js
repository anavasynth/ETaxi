let map = null;
let startCoords = null;
let endCoords = null;
let manualMode = null;
let routeLine = null;
let startMarker = null;
let endMarker = null;
let tempMarker = null;

function initMap() {
    if (!map) {
        map = L.map('map').setView([49.8397, 24.0297], 13); // Львів — центр
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        document.getElementById('mapContainer').style.display = 'block';
    }
}

function createMarkerAndSet(coords, type) {
    if (type === 'start') {
        if (startMarker) map.removeLayer(startMarker);
        startCoords = coords;
        startMarker = L.marker(coords).addTo(map).bindPopup("Старт").openPopup();
    } else if (type === 'end') {
        if (endMarker) map.removeLayer(endMarker);
        endCoords = coords;
        endMarker = L.marker(coords).addTo(map).bindPopup("Фініш").openPopup();
    }
}

function enableManual(type) {
    manualMode = type;
    initMap();
    map.on('click', function (e) {
        if (tempMarker) map.removeLayer(tempMarker);
        tempMarker = L.marker(e.latlng).addTo(map);
    });
}

function confirmSelection(type) {
    if (tempMarker) {
        const coords = [tempMarker.getLatLng().lat, tempMarker.getLatLng().lng];
        createMarkerAndSet(coords, type);
        map.off('click');
        map.removeLayer(tempMarker);
        tempMarker = null;

        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${coords[0]}&lon=${coords[1]}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById(type === 'start' ? 'startSearch' : 'endSearch').value = data.display_name;
            });
    }
}

function fetchSuggestions(query, callback) {
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
        .then(res => res.json())
        .then(data => callback(data));
}

function setupAutocomplete(inputId, suggestionsId, type) {
    const input = document.getElementById(inputId);
    const suggestionsDiv = document.getElementById(suggestionsId);

    input.addEventListener('input', function () {
        const query = input.value;
        if (query.length < 2) return;
        fetchSuggestions(query, data => {
            suggestionsDiv.innerHTML = '';
            data.forEach(place => {
                const div = document.createElement('div');
                div.innerText = place.display_name;
                div.onclick = () => {
                    input.value = place.display_name;
                    suggestionsDiv.innerHTML = '';
                    const coords = [parseFloat(place.lat), parseFloat(place.lon)];
                    createMarkerAndSet(coords, type);
                    if (!map) {
                        initMap();
                    }
                    map.setView(coords, 13);
                };
                suggestionsDiv.appendChild(div);
            });
        });
    });
}

setupAutocomplete('startSearch', 'startSuggestions', 'start');
setupAutocomplete('endSearch', 'endSuggestions', 'end');

function calculateDistance() {
    if (!startCoords || !endCoords) {
        alert("Будь ласка, оберіть обидві точки");
        return;
    }

    fetch('/distance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: startCoords, end: endCoords })
    })
    .then(res => res.json())
    .then(data => {
        if (data.distance_km !== undefined && data.geometry) {
            document.getElementById('result').innerText = `Відстань: ${data.distance_km} км`;

            if (!map) {
                initMap();
            }

            if (routeLine) map.removeLayer(routeLine);

            const geojson = {
                type: "Feature",
                geometry: data.geometry
            };

            routeLine = L.geoJSON(geojson, {
                style: {
                    color: 'blue',
                    weight: 5
                }
            }).addTo(map);

            map.fitBounds(routeLine.getBounds());
        } else {
            document.getElementById('result').innerText = `Помилка: ${data.error || 'Не вдалося побудувати маршрут'}`;
        }
    });
}


