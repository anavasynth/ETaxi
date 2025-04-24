let currentLang = localStorage.getItem('language') || 'en';
document.getElementById('languageSelect').value = currentLang;

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
        });
}

// Завантаження мови при першому завантаженні сторінки
loadLanguage(currentLang);

// Зміна мови
document.getElementById('languageSelect').addEventListener('change', function () {
    const selectedLang = this.value;
    localStorage.setItem('language', selectedLang);
    loadLanguage(selectedLang);
});