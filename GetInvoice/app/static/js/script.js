document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("search-form");
    const clearBtn = document.getElementById("clear-btn");
    const textarea = document.getElementById("client_codes");
    const resultsPanel = document.getElementById("results-panel");

    if (clearBtn && textarea && form) {
        clearBtn.addEventListener("click", () => {
            textarea.value = "";
            textarea.focus();
        });
    }

    if (resultsPanel) {
        resultsPanel.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    if (form && textarea) {
        form.addEventListener("submit", () => {
            textarea.value = textarea.value.trim();
        });
    }
});
