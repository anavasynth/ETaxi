document.addEventListener('DOMContentLoaded', () => {
  const map = window.map;
  let currentInputType = window.currentInputType;

  function enableMapClick(type) {
    currentInputType = type;
    alert(`Натисніть на карту, щоб вибрати точку для ${type === 'start' ? 'посадки' : 'висадки'}.`);
  }

  window.enableMapClick = enableMapClick;

  map.on('click', (e) => {
    if (!currentInputType) return;
    const latlng = e.latlng;
    setMarker(currentInputType, latlng, currentInputType === 'start' ? 'Посадка (з карти)' : 'Висадка (з карти)');
    reverseGeocode(latlng.lat, latlng.lng, currentInputType);
    currentInputType = null;
  });

  function reverseGeocode(lat, lng, inputId) {
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const address = data.display_name || `${lat}, ${lng}`;
      document.getElementById(inputId).value = address;
    })
    .catch(error => {
      console.error("Reverse geocoding error:", error);
      document.getElementById(inputId).value = `${lat}, ${lng}`;
    });
}

  function setMarker(type, latlng, label) {
    if (type === 'start') {
      if (window.startMarker) map.removeLayer(window.startMarker);
      window.startCoords = [latlng.lng, latlng.lat];
      window.startMarker = L.marker(latlng).addTo(map).bindPopup(label).openPopup();
    } else {
      if (window.endMarker) map.removeLayer(window.endMarker);
      window.endCoords = [latlng.lng, latlng.lat];
      window.endMarker = L.marker(latlng).addTo(map).bindPopup(label).openPopup();
    }

    if (window.startCoords && window.endCoords) {
      getRoute(window.startCoords, window.endCoords);
    }
  }

  window.setMarker = setMarker;

  function searchLocation(input, type) {
    const query = input.value;
    const suggestionsBox = document.getElementById(`${type}-suggestions`);
    suggestionsBox.innerHTML = '';
    if (query.length < 3) return;

    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(results => {
        suggestionsBox.innerHTML = '';
        results.forEach(result => {
          const div = document.createElement('div');
          div.classList.add('autocomplete-suggestion');
          div.textContent = result.display_name;
          div.onclick = () => {
            input.value = result.display_name;
            const latlng = L.latLng(result.lat, result.lon);
            setMarker(type, latlng, type === 'start' ? 'Посадка (пошук)' : 'Висадка (пошук)');
            map.setView(latlng, 14);
            suggestionsBox.innerHTML = '';
          };
          suggestionsBox.appendChild(div);
        });
      });
  }

  window.searchLocation = searchLocation;
});
