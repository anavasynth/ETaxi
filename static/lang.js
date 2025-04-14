 const translations = {
    uk: {
      title: "Планування маршруту",
      startLabel: "📍 Місце посадки",
      endLabel: "📍 Місце висадки",
      select: "Обрати",
      tariffs: "📋 Тарифи",
      routeLength: "🚗 <b>Довжина маршруту:</b>",
      tariff: "💰 <b>Тариф:</b>",
      cost: "🧾 <b>Вартість:</b>",
      notFound: "Маршрут не знайдено!",
      error: "Помилка...",
      footer: "&copy; 2025 Taxi Service. Всі права захищено.",
    },
    en: {
      title: "Route Planning",
      startLabel: "📍 Pickup Location",
      endLabel: "📍 Drop-off Location",
      select: "Select",
      tariffs: "📋 Tariffs",
      routeLength: "🚗 <b>Route Length:</b>",
      tariff: "💰 <b>Tariff:</b>",
      cost: "🧾 <b>Cost:</b>",
      notFound: "Route not found!",
      error: "Error...",
      footer: "&copy; 2025 Taxi Service. All rights reserved.",
    },
    pl: {
      title: "Planowanie Trasy",
      startLabel: "📍 Miejsce odbioru",
      endLabel: "📍 Miejsce docelowe",
      select: "Wybierz",
      tariffs: "📋 Taryfy",
      routeLength: "🚗 <b>Długość trasy:</b>",
      tariff: "💰 <b>Taryfa:</b>",
      cost: "🧾 <b>Koszt:</b>",
      notFound: "Trasa nie znaleziona!",
      error: "Błąd...",
      footer: "&copy; 2025 Taxi Service. Wszelkie prawa zastrzeżone.",
    }
  };

  function updateLanguage(lang) {
    const t = translations[lang];

    document.querySelector("h2").innerText = t.title;
    document.querySelector("label[for='start']")?.innerText = t.startLabel;
    document.querySelector("label[for='end']")?.innerText = t.endLabel;
    document.querySelectorAll("button.btn-success").forEach(btn => btn.innerText = t.select);
    document.querySelector("#tariffs h2").innerText = t.tariffs;
    document.querySelector("footer").innerHTML = t.footer;

    // Optional: update route box if visible
    const box = document.getElementById("distance");
    if (box.innerHTML.includes("Довжина") || box.innerHTML.includes("Route") || box.innerHTML.includes("Trasa")) {
      box.innerHTML = ""; // Or re-render route if needed
    }
  }

  document.getElementById("languageSwitcher").addEventListener("change", (e) => {
    updateLanguage(e.target.value);
  });

  // Init default language
  updateLanguage("uk");
