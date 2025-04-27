let currentLang = localStorage.getItem('language') || 'en';

// Якщо є селектор вибору мови на цій сторінці — встановити значення
const languageSelect = document.getElementById('languageSelect');
if (languageSelect) {
    languageSelect.value = currentLang;

    // Додати слухач зміни мови тільки якщо селектор є
    languageSelect.addEventListener('change', function () {
        const selectedLang = this.value;
        localStorage.setItem('language', selectedLang);
        loadLanguage(selectedLang);
    });
}

// Функція для оновлення динамічного контенту з локалізацією
function updateDynamicLocalization() {
    const currentLang = localStorage.getItem('language') || 'en';
    loadLanguage(currentLang);
}

// Завантаження мови при завантаженні сторінки
loadLanguage(currentLang);

function loadLanguage(lang) {
    fetch(`/static/lang/${lang}.json`)
        .then(response => response.json())
        .then(translations => {
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (translations[key]) {
                    el.textContent = translations[key];
                }
            });
            document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
                const key = el.getAttribute('data-i18n-placeholder');
                if (translations[key]) {
                    el.setAttribute('placeholder', translations[key]);
                }
            });
        });
}
