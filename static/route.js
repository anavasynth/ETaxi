document.addEventListener('DOMContentLoaded', () => {
  async function getRoute(start, end) {
    try {
      const response = await fetch('/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coordinates: [start, end] })
      });
      const data = await response.json();

      if (!data || !data.features || !data.features[0]) {
        document.getElementById('distance').innerText = 'Маршрут не знайдено!';
        return;
      }

      if (window.routeLayer) window.map.removeLayer(window.routeLayer);
      window.routeLayer = L.geoJSON(data, {
        style: { color: 'green', weight: 5 }
      }).addTo(window.map);

      const distance = data.features[0].properties.summary.distance / 1000;
      const tariffInfo = await getTariff(start, end);
      const price = distance * tariffInfo.rate;
      window.calculatedPrice = price;

      document.getElementById('distance').innerHTML =
        `🚗 <b data-i18n="rd_route_len">Довжина маршруту:</b> ${distance.toFixed(2)} км<br>` +
        `💰 <b data-i18n="rd_tariff">Тариф:</b> ${tariffInfo.name} (${tariffInfo.rate.toFixed(2)} PLN/км)<br>` +
        `🧾 <b data-i18n="rd_price">Вартість:</b> ${price.toFixed(2)} PLN`;

      updateDynamicLocalization();
    } catch (error) {
      console.error('Error fetching route:', error);
      document.getElementById('distance').innerText = 'Помилка при розрахунку маршруту';
    }

  }

  window.getRoute = getRoute;

  async function getTariff(startCoords, endCoords) {
    try {
      const isStartInsideCity = await isWithinCity(startCoords[1], startCoords[0]);
      const isEndInsideCity = await isWithinCity(endCoords[1], endCoords[0]);

      const now = new Date();
      const hour = now.getHours();
      const day = now.getDay();
      const isNight = hour >= 22 || hour < 6;
      const isSunday = day === 0;

      if (isNight || isSunday) {
        return isStartInsideCity && isEndInsideCity ? { name: "Tariff II", rate: 3.15 } : { name: "Tariff IV", rate: 4.00 };
      } else {
        return isStartInsideCity && isEndInsideCity ? { name: "Tariff I", rate: 2.82 } : { name: "Tariff III", rate: 3.79 };
      }
    } catch (error) {
      console.error('Error in getTariff:', error);
      return { name: "Unknown", rate: 0 };
    }
  }

  window.getTariff = getTariff;

  async function isWithinCity(lat, lon) {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
      const data = await response.json();
      return data.address.city;
    } catch (error) {
      console.error('Error in isWithinCity:', error);
      return false;
    }
  }

  window.isWithinCity = isWithinCity;

  document.getElementById('confirmOrderBtn').addEventListener('click', async () => {
  const startInput = document.getElementById('start').value.trim();
  const endInput = document.getElementById('end').value.trim();
  const selectedClass = document.querySelector('.ride-class-option.selected');

  if (!startInput || !endInput) {
    showModalAlert('Будь ласка, введіть обидві адреси.')
    return;
  }

  if (!selectedClass) {
    showModalAlert('Оберіть клас авто.');
    return;
  }

  const startCoords = window.startCoords;
  const endCoords = window.endCoords;

  if (!startCoords || !endCoords) {
    showModalAlert('Будь ласка, оберіть точки на мапі.');
    return;
  }

  await getRoute(startCoords, endCoords);

  // Після успішного побудування маршруту показати модалку
  const confirmModal = new bootstrap.Modal(document.getElementById('confirmRouteModal'));
  confirmModal.show();
});

document.getElementById('confirmRouteBtn').addEventListener('click', async () => {
    const firstName = document.getElementById('confirmFirstName').value;
    const email = document.getElementById('confirmEmail').value;
    const phone = document.getElementById('confirmPhone').value;
    const selectedClass = document.querySelector('.ride-class-option.selected');

    const startAddress = window.startAddress || document.getElementById('start').value;
    const endAddress = window.endAddress || document.getElementById('end').value;
    const carClass = selectedClass.dataset.value;

    const paymentType = document.getElementById('paymentOption').value; // full / partial
    const rideTimeOption = document.getElementById('rideTimeOption').value; // now / later
    const scheduledTime = document.getElementById('scheduledTime').value; // якщо вибрали "later"

    let paymentAmount = window.calculatedPrice;

    // Якщо вибрано оплату 30%, змінити суму
    if (paymentType === 'partial') {
        paymentAmount = (paymentAmount * 0.3).toFixed(2);
    }

    try {
        const response = await fetch('/create-route-order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                firstName,
                email,
                phone,
                price: paymentAmount,
                carClass,
                startAddress,
                endAddress,
                paymentType,               // <-- додаємо
                rideTimeOption,             // (now або later)
                scheduledTime: rideTimeOption === 'later' ? scheduledTime : null
            })
        });

        const responseText = await response.text();
        console.log('Response:', responseText);

        if (response.ok) {
            const data = JSON.parse(responseText);

            if (data.status === 'success') {
                const orderId = data.id;

                const modal = bootstrap.Modal.getInstance(document.getElementById('confirmRouteModal'));
                modal.hide();

                // Перенаправлення на оплату
                const stripe = Stripe('pk_test_51RE7BEPFfDXYRYYJDO3ubsoT4BwW3V6GSVutYTRJ3b3pkcrK89wM7EYkPlJJSKsqw57R5rYVykXCUuUEfrK6uSCl000lUoBaAb');
                const checkoutResponse = await fetch("/create-checkout-session", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        price: paymentAmount,
                        order_id: orderId,
                        order_type: 'ride'
                    })
                });

                const checkoutData = await checkoutResponse.json();

                if (checkoutResponse.ok) {
                    stripe.redirectToCheckout({ sessionId: checkoutData.id }).then(function (result) {
                        if (result.error) {
                            alert('Помилка оплати: ' + result.error.message);
                        }
                    });
                } else {
                    alert('Помилка створення сесії оплати.');
                }
            } else {
                alert('Сталася помилка при створенні замовлення.');
            }
        } else {
            const errorData = JSON.parse(responseText);
            alert('Сталася помилка при створенні замовлення: ' + errorData.message);
        }
    } catch (error) {
        alert('Сталася помилка: ' + error.message);
    }
});

// Показати/сховати блок дати й часу в залежності від вибору
document.getElementById('rideTimeOption').addEventListener('change', function() {
  const scheduledBlock = document.getElementById('scheduledTimeBlock');
  if (this.value === 'later') {
    scheduledBlock.style.display = 'block';
  } else {
    scheduledBlock.style.display = 'none';
  }
});

function showModalAlert(message) {
  // Set the modal message
  document.getElementById('modalAlertMessage').innerText = message;

  // Show the modal
  const alertModal = new bootstrap.Modal(document.getElementById('genericModal'));
  alertModal.show();
}
});
