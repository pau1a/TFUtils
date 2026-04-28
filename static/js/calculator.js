document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector('[data-calculator="percentage-change"]');
    if (!form) {
        return;
    }

    const oldInput = form.querySelector("#old-value");
    const newInput = form.querySelector("#new-value");
    const error = form.querySelector("[data-form-error]");
    const resetButton = document.querySelector("[data-reset-calculator]");
    const headline = document.querySelector("[data-result-headline]");
    const detail = document.querySelector("[data-result-detail]");
    const badge = document.querySelector("[data-result-badge]");

    const updateResult = () => {
        const oldValue = Number(oldInput.value);
        const newValue = Number(newInput.value);

        if (!Number.isFinite(oldValue) || !Number.isFinite(newValue)) {
            error.textContent = "Enter a valid number.";
            return;
        }

        if (oldValue === 0) {
            error.textContent = "Podge needs a starting value that is not zero.";
            return;
        }

        error.textContent = "";
        const change = newValue - oldValue;
        const percentage = (change / oldValue) * 100;
        const rounded = percentage.toFixed(2).replace(/\.00$/, "");
        const direction = percentage > 0 ? "increase" : percentage < 0 ? "decrease" : "change";
        const badgeText = percentage > 0 ? "Increase" : percentage < 0 ? "Decrease" : "No change";

        headline.textContent = `${Math.abs(rounded)}% ${direction}`;
        detail.textContent = `The value changed by ${change.toFixed(2).replace(/\.00$/, "")}, which is ${Math.abs(rounded)}% ${percentage >= 0 ? "higher" : "lower"} than the starting value.`;
        badge.textContent = badgeText;
    };

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        updateResult();
    });

    form.addEventListener("input", updateResult);

    resetButton?.addEventListener("click", () => {
        oldInput.value = "80";
        newInput.value = "100";
        updateResult();
    });

    updateResult();
});
