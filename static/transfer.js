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

    window.calculatedTransferPrice = parseFloat(price);

    const response = await fetch('/create-transfer-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, lastName, firstName, seats, price, transfer })
    });

    if (response.ok) {
      alert('Замовлення успішно створено!');
      const modal = bootstrap.Modal.getInstance(document.getElementById('transferModal'));
      modal.hide();
    } else {
      alert('Сталася помилка при створенні замовлення.');
    }
  });
});
