document.addEventListener('DOMContentLoaded', () => {
  const translations = {
    uk: {
      navRide: "Поїздка",
      navTariff: "Тарифи",
      rideTitle: "Планування маршруту",
      pickup: "📍 Місце посадки",
      chooseMarkerButton: "Обрати",
      dropoff: "📍 Місце висадки",
      tariffTitle: "📋 Тарифи",
      tariffs: [
        { name: "Тариф I", desc: "Ціна: 2.82 PLN/км", info: "Тариф у межах міста в будні дні." },
        { name: "Тариф II", desc: "Ціна: 3.15 PLN/км", info: "Нічний тариф та вихідні." },
        { name: "Тариф III", desc: "Ціна: 3.79 PLN/км", info: "Будні за межами міста." },
        { name: "Тариф IV", desc: "Ціна: 4.00 PLN/км", info: "Ніч або вихідні за межами міста." }
      ]
    },
    en: {
      navRide: "Ride",
      navTariff: "Tariffs",
      rideTitle: "Route Planning",
      pickup: "📍 Pickup Location",
      chooseMarkerButton: "Choose",
      dropoff: "📍 Drop-off Location",
      tariffTitle: "📋 Tariffs",
      tariffs: [
        { name: "Tariff I", desc: "Price: 2.82 PLN/km", info: "Weekday city rate." },
        { name: "Tariff II", desc: "Price: 3.15 PLN/km", info: "Night and holiday rate." },
        { name: "Tariff III", desc: "Price: 3.79 PLN/km", info: "Weekday suburban rate." },
        { name: "Tariff IV", desc: "Price: 4.00 PLN/km", info: "Night or weekend suburban rate." }
      ]
    },
    pl: {
      navRide: "Poizdka",
      navTariff: "Taryfy",
      rideTitle: "Planowanie trasy",
      pickup: "📍 Miejsce odbioru",
      chooseMarkerButton: "Vibrac",
      dropoff: "📍 Miejsce wysadzenia",
      tariffTitle: "📋 Taryfy",
      tariffs: [
        { name: "Taryfa I", desc: "Cena: 2.82 PLN/km", info: "Stawka dzienna w mieście." },
        { name: "Taryfa II", desc: "Cena: 3.15 PLN/km", info: "Noc i święta." },
        { name: "Taryfa III", desc: "Cena: 3.79 PLN/km", info: "Dzienna poza miastem." },
        { name: "Taryfa IV", desc: "Cena: 4.00 PLN/km", info: "Noc lub święta poza miastem." }
      ]
    }
  };

  document.getElementById('languageSwitcher').addEventListener('change', function () {
    const lang = this.value;
    const t = translations[lang];

    // Заміна заголовків
    document.querySelector('#ride h2').textContent = t.rideTitle;
    document.getElementById('label-start').textContent = t.pickup;
    document.getElementById('label-end').textContent = t.dropoff;
    document.querySelector('#tariffs h2').textContent = t.tariffTitle;

    document.querySelector('#chooseMarkerButton1').textContent = t.chooseMarkerButton;
    document.querySelector('#chooseMarkerButton2').textContent = t.chooseMarkerButton;

    document.querySelector('#navRide').textContent = t.navRide;
    document.querySelector('#navTariff').textContent = t.navTariff;

    // Заміна тарифів
    const cards = document.querySelectorAll('#tariffs .card');
    cards.forEach((card, index) => {
      card.querySelector('.card-title').textContent = t.tariffs[index].name;
      const paragraphs = card.querySelectorAll('.card-text');
      paragraphs[0].textContent = t.tariffs[index].desc;
      paragraphs[1].textContent = t.tariffs[index].info;
    });
  });
});
