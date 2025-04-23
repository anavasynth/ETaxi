document.addEventListener('DOMContentLoaded', () => {
  function openTransferModal(button) {
    const card = button.closest('.card');
    const transfer = card.dataset.transfer;
    const price13 = card.dataset['price13'];
    const price46 = card.dataset['price46'];
    const price68 = card.dataset['price68'];

    const modal = new bootstrap.Modal(document.getElementById('transferModal'));
    document.getElementById('transferModalLabel').textContent = `Замовлення трансферу: ${transfer}`;

    const priceField = document.getElementById('price');
    const seatsField = document.getElementById('seats');

    seatsField.addEventListener('change', () => {
      let price = 0;
      if (seatsField.value === '1-3') {
        price = price13;
      } else if (seatsField.value === '4-6') {
        price = price46;
      } else if (seatsField.value === '6-8') {
        price = price68;
      }
      priceField.value = `${price} PLN`;
    });

    // Встановити початкове значення ціни
    seatsField.dispatchEvent(new Event('change'));

    modal.show();
  }

  window.openTransferModal = openTransferModal;

document.getElementById('payTransferBtn').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  const lastName = document.getElementById('lastName').value;
  const firstName = document.getElementById('firstName').value;
  const seats = document.getElementById('seats').value;
  const price = document.getElementById('price').value;
  const transfer = document.getElementById('transferModalLabel').textContent.split(': ')[1];

  try {
    const response = await fetch('/create-transfer-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, lastName, firstName, seats, price, transfer })
    });

    const responseText = await response.text();
    console.log('Transfer order response:', responseText);

    if (response.ok) {
      const data = JSON.parse(responseText);
      if (data.status === 'success') {
        const transferId = data.id;

        // Закриваємо модалку
        const modal = bootstrap.Modal.getInstance(document.getElementById('transferModal'));
        modal.hide();

        // Перенаправлення на Stripe
        const stripe = Stripe('pk_test_51RE7BEPFfDXYRYYJDO3ubsoT4BwW3V6GSVutYTRJ3b3pkcrK89wM7EYkPlJJSKsqw57R5rYVykXCUuUEfrK6uSCl000lUoBaAb');
        const checkoutResponse = await fetch('/create-checkout-session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            price: parseFloat(price),
            order_id: transferId,
            order_type: 'transfer'
          })
        });

        const checkoutData = await checkoutResponse.json();

        if (checkoutResponse.ok) {
          stripe.redirectToCheckout({ sessionId: checkoutData.id }).then((result) => {
            if (result.error) {
              alert('Помилка оплати: ' + result.error.message);
            }
          });
        } else {
          alert('Помилка створення сесії Stripe.');
        }
      } else {
        alert('Сталася помилка при створенні трансферу.');
      }
    } else {
      const errorData = JSON.parse(responseText);
      alert('Помилка при створенні трансферу: ' + errorData.message);
    }
  } catch (error) {
    alert('Помилка запиту: ' + error.message);
  }
});
});
