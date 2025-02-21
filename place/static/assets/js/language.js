document.addEventListener("DOMContentLoaded", function () {
    const languageSelector = document.getElementById("language-selector");

    // Charger la langue sauvegardée
    const savedLang = localStorage.getItem("selectedLanguage");
    if (savedLang) {
        languageSelector.value = savedLang;
        changeLanguage(savedLang);  // Fonction pour charger la langue
    }

    // Écouteur d'événement pour changer la langue
    languageSelector.addEventListener("change", function () {
        const selectedLanguage = this.value;
        localStorage.setItem("selectedLanguage", selectedLanguage);
        window.location.href = `?lang=${selectedLanguage}`;
    });
});

// Fonction pour charger la langue (si nécessaire)
function changeLanguage(lang) {
    console.log(`Langue actuelle: ${lang}`);
}
