document.addEventListener('DOMContentLoaded', () => {
  // Ініціалізація карти
  const map = L.map('map').setView([50.0647, 19.9450], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

  window.map = map;
  window.startMarker = null;
  window.endMarker = null;
  window.routeLayer = null;
  window.startCoords = null;
  window.endCoords = null;
  window.currentInputType = null;
  window.calculatedPrice = 0;
  window.calculatedTransferPrice = 0;
});
