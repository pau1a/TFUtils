document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("[data-calculator]");
    if (!form) {
        return;
    }

    const calculatorType = form.dataset.calculator;
    const error = form.querySelector("[data-form-error]");
    const resetButton = document.querySelector("[data-reset-calculator]");
    const headline = document.querySelector("[data-result-headline]");
    const detail = document.querySelector("[data-result-detail]");
    const badge = document.querySelector("[data-result-badge]");
    const mood = document.querySelector("[data-podge-mood]");
    const explainer = document.querySelector("[data-result-explainer]");
    const summary = document.querySelector("[data-podge-summary]");
    const delta = document.querySelector("[data-result-delta]");
    const start = document.querySelector("[data-result-start]");
    const end = document.querySelector("[data-result-end]");
    const copyButton = document.querySelector("[data-copy-result]");
    const copyFeedback = document.querySelector("[data-copy-feedback]");
    const verdictCard = document.querySelector("[data-verdict-card]");
    const verdictTitle = document.querySelector("[data-verdict-title]");
    const verdictSummary = document.querySelector("[data-verdict-summary]");

    const numberInputs = Array.from(form.querySelectorAll('input[type="number"]'));
    const dateInputs = Array.from(form.querySelectorAll('input[type="date"]'));
    const selectInputs = Array.from(form.querySelectorAll("select"));
    const checkboxInputs = Array.from(form.querySelectorAll('input[type="checkbox"]'));
    const initialState = {
        numbers: numberInputs.map((input) => input.value),
        dates: dateInputs.map((input) => input.value),
        selects: selectInputs.map((input) => input.value),
        checks: checkboxInputs.map((input) => input.checked),
    };

    const format = (value) => value.toFixed(2).replace(/\.00$/, "");
    const isoDateToLong = (value) => {
        const date = new Date(`${value}T00:00:00`);
        return new Intl.DateTimeFormat("en-GB", {
            day: "numeric",
            month: "long",
            year: "numeric",
        }).format(date);
    };
    const setError = (message) => {
        error.textContent = message;
    };
    const clearError = () => {
        error.textContent = "";
    };
    const setResult = (result) => {
        headline.textContent = result.headline;
        detail.textContent = result.detail;
        badge.textContent = result.badge;
        mood.textContent = result.mood;
        explainer.textContent = result.explainer;
        summary.textContent = result.summary;
        delta.textContent = result.signals[0];
        start.textContent = result.signals[1];
        end.textContent = result.signals[2];
        if (verdictTitle) {
            verdictTitle.textContent = result.headline;
        }
        if (verdictSummary) {
            verdictSummary.textContent = result.summary;
        }
        if (verdictCard && result.verdictTone) {
            verdictCard.dataset.tone = result.verdictTone;
        }
    };
    const buildCopyText = () => `${headline.textContent}. ${detail.textContent}`;

    const calculators = {
        "percentage-change": () => {
            const oldValue = Number(form.querySelector("#old-value").value);
            const newValue = Number(form.querySelector("#new-value").value);

            if (!Number.isFinite(oldValue) || !Number.isFinite(newValue)) {
                throw new Error("Enter a valid number.");
            }
            if (oldValue === 0) {
                throw new Error("Podge needs a starting value that is not zero.");
            }

            const change = newValue - oldValue;
            const percentage = (change / oldValue) * 100;
            const rounded = format(percentage);
            const direction = percentage > 0 ? "increase" : percentage < 0 ? "decrease" : "change";
            const badgeText = percentage > 0 ? "Increase" : percentage < 0 ? "Decrease" : "No change";
            const comparison = percentage > 0 ? "higher" : percentage < 0 ? "lower" : "the same as";

            return {
                headline: `${Math.abs(rounded)}% ${direction}`,
                detail: `The value changed by ${format(change)}, which is ${Math.abs(rounded)}% ${comparison} the starting value.`,
                badge: badgeText,
                mood: percentage > 0 ? "Podge is pleased. That is a clean upward move." : percentage < 0 ? "Podge is focused. This one moved downward." : "Podge is calm. No movement detected.",
                explainer: percentage > 0
                    ? `This is an increase because the new value is above the starting value. The gap is ${format(change)}, and that gap equals ${Math.abs(rounded)}% of the original number.`
                    : percentage < 0
                        ? `This is a decrease because the new value is below the starting value. The gap is ${format(Math.abs(change))}, which works out to ${Math.abs(rounded)}% of the original number.`
                        : "There is no increase or decrease here because the starting and ending values are identical.",
                summary: percentage > 0
                    ? "That is a clear increase, so the new value is meaningfully higher than the starting one."
                    : percentage < 0
                        ? "That is a drop rather than a rise, so the new value has fallen relative to where it started."
                        : "No drama. The value stayed exactly where it started.",
                signals: [
                    `${change > 0 ? "+" : ""}${format(change)}`,
                    format(oldValue),
                    format(newValue),
                ],
            };
        },
        vat: () => {
            const amount = Number(form.querySelector("#vat-amount").value);
            const rate = Number(form.querySelector("#vat-rate").value);
            const mode = form.querySelector("#vat-mode").value;

            if (!Number.isFinite(amount) || !Number.isFinite(rate)) {
                throw new Error("Enter a valid number.");
            }
            if (amount < 0) {
                throw new Error("Podge needs a price that is zero or more.");
            }
            if (rate < 0) {
                throw new Error("VAT rate cannot be negative.");
            }

            const rateFraction = rate / 100;
            const net = mode === "add" ? amount : amount / (1 + rateFraction);
            const gross = mode === "add" ? amount * (1 + rateFraction) : amount;
            const vatAmount = gross - net;
            const actionLabel = mode === "add" ? "VAT added" : "VAT removed";

            return {
                headline: `${format(gross)} total ${mode === "add" ? "with VAT" : "including VAT"}`,
                detail: mode === "add"
                    ? `A net price of ${format(net)} at ${format(rate)}% VAT gives ${format(vatAmount)} of tax and a gross total of ${format(gross)}.`
                    : `A VAT-inclusive price of ${format(gross)} at ${format(rate)}% contains ${format(vatAmount)} of tax, leaving a net price of ${format(net)}.`,
                badge: actionLabel,
                mood: mode === "add" ? "Podge has stacked the tax on top." : "Podge has peeled the tax back out.",
                explainer: mode === "add"
                    ? "This starts with a net price and adds the VAT portion separately so the tax is visible instead of hidden in the total."
                    : "This works backwards from a VAT-inclusive total so you can see the underlying net price and the tax slice clearly.",
                summary: mode === "add"
                    ? "That is the full amount after VAT, with the tax separated out so the final price is easier to trust."
                    : "That breaks the VAT-inclusive price into the untaxed base amount and the tax portion.",
                signals: [format(vatAmount), format(net), format(gross)],
            };
        },
        "room-area": () => {
            const length = Number(form.querySelector("#room-length").value);
            const width = Number(form.querySelector("#room-width").value);
            const unit = form.querySelector("#room-unit").value;
            const areaUnit = unit === "m" ? "m²" : "ft²";
            const unitLabel = unit === "m" ? "m" : "ft";

            if (!Number.isFinite(length) || !Number.isFinite(width)) {
                throw new Error("Enter a valid number.");
            }
            if (length <= 0 || width <= 0) {
                throw new Error("Podge needs room dimensions greater than zero.");
            }

            const area = length * width;

            return {
                headline: `${format(area)} ${areaUnit}`,
                detail: `A room ${format(length)} ${unitLabel} long and ${format(width)} ${unitLabel} wide covers ${format(area)} ${areaUnit}.`,
                badge: "Area ready",
                mood: "Podge has mapped the floor space.",
                explainer: "This is the simplest area calculation: multiply the length by the width, making sure both measurements use the same unit.",
                summary: "That is the base floor area before you add extra allowance for cuts, waste, or awkward corners.",
                signals: [`${format(area)} ${areaUnit}`, `${format(length)} ${unitLabel}`, `${format(width)} ${unitLabel}`],
            };
        },
        "days-between-dates": () => {
            const startValue = form.querySelector("#start-date").value;
            const endValue = form.querySelector("#end-date").value;
            const includeBoth = form.querySelector("#include-both").checked;

            if (!startValue || !endValue) {
                throw new Error("Podge needs both dates filled in.");
            }

            const startDate = new Date(`${startValue}T00:00:00`);
            const endDate = new Date(`${endValue}T00:00:00`);
            const millisecondsPerDay = 1000 * 60 * 60 * 24;
            const baseDays = Math.round((endDate - startDate) / millisecondsPerDay);
            const days = includeBoth ? baseDays + (baseDays >= 0 ? 1 : -1) : baseDays;
            const absoluteDays = Math.abs(days);
            const direction = days >= 0 ? "after" : "before";

            return {
                headline: `${absoluteDays} day${absoluteDays === 1 ? "" : "s"} apart`,
                detail: includeBoth
                    ? `Counting both dates, ${isoDateToLong(endValue)} is ${absoluteDays} day${absoluteDays === 1 ? "" : "s"} ${direction} ${isoDateToLong(startValue)}.`
                    : `There are ${absoluteDays} day${absoluteDays === 1 ? "" : "s"} between ${isoDateToLong(startValue)} and ${isoDateToLong(endValue)}.`,
                badge: includeBoth ? "Inclusive count" : "Date gap",
                mood: "Podge has checked the calendar.",
                explainer: includeBoth
                    ? "This count includes the starting day itself, which is often useful for bookings, schedules, and countdowns."
                    : "This is the plain calendar-day gap between the two dates, without counting the starting day itself.",
                summary: includeBoth
                    ? "That is the inclusive date span, so both edge dates are counted as part of the total."
                    : "That is the straight calendar gap between the two dates.",
                signals: [String(absoluteDays), startValue, endValue],
            };
        },
        "send-that-message": () => {
            const urgency = Number(form.querySelector("#message-urgency").value);
            const clarity = Number(form.querySelector("#message-clarity").value);
            const charge = Number(form.querySelector("#message-charge").value);
            const hour = Number(form.querySelector("#message-hour").value);

            if (![urgency, clarity, charge, hour].every(Number.isFinite)) {
                throw new Error("Enter values for all four fields.");
            }
            if ([urgency, clarity, charge].some((value) => value < 1 || value > 10)) {
                throw new Error("Use scores from 1 to 10 for urgency, clarity, and emotional charge.");
            }
            if (hour < 0 || hour > 23) {
                throw new Error("Use an hour from 0 to 23.");
            }

            const latenessPenalty = hour >= 23 || hour < 6 ? 3 : hour >= 21 ? 2 : 0;
            const score = urgency + clarity - charge - latenessPenalty;

            let headlineText = "Draft it. Sleep on it.";
            let badgeText = "Hold fire";
            let moodText = "Podge recommends waiting.";
            let detailText = `The urgency is ${urgency}/10, clarity is ${clarity}/10, emotional charge is ${charge}/10, and the time penalty is ${latenessPenalty}.`;
            let explainerText = "This gauge makes urgency, clarity, emotional heat, and lateness visible at the same time so you can see whether the impulse is carrying more weight than the actual reason to send.";
            let summaryText = "The current balance suggests waiting, rewriting, or reviewing it in a calmer moment.";

            if (score >= 8) {
                headlineText = "Send it, but keep it tidy.";
                badgeText = "Probably fine";
                moodText = "Podge has lowered the warning flag.";
                summaryText = "The balance here looks clear enough that sending the message is probably reasonable.";
            } else if (score >= 4) {
                headlineText = "Maybe send it. Read it once more first.";
                badgeText = "Proceed carefully";
                moodText = "Podge recommends one calm edit.";
                summaryText = "This is not a disaster, but it probably improves with one more pass and slightly less adrenaline.";
            } else if (score <= 0) {
                headlineText = "Absolutely not tonight.";
                badgeText = "Severe wobble";
                moodText = "Podge strongly recommends waiting.";
                summaryText = "The current mix looks impulsive, late, and emotionally charged enough that waiting is the safer move.";
            }

            return {
                headline: headlineText,
                detail: detailText,
                badge: badgeText,
                mood: moodText,
                explainer: explainerText,
                summary: summaryText,
                signals: [`${score}/10`, `${urgency}/10`, `${charge}/10`],
                verdictTone: score >= 8 ? "green" : score >= 4 ? "amber" : "red",
            };
        },
        "fancy-version": () => {
            const use = Number(form.querySelector("#fancy-use").value);
            const failure = Number(form.querySelector("#fancy-failure").value);
            const longevity = Number(form.querySelector("#fancy-longevity").value);
            const joy = Number(form.querySelector("#fancy-joy").value);
            const pain = Number(form.querySelector("#fancy-pain").value);

            if (![use, failure, longevity, joy, pain].every(Number.isFinite)) {
                throw new Error("Enter values for all five fields.");
            }
            if ([use, failure, longevity, joy, pain].some((value) => value < 1 || value > 10)) {
                throw new Error("Use scores from 1 to 10 for every factor.");
            }

            const score = Math.round(((use + failure + longevity + joy) / 4) - pain + 5);
            let headlineText = "Maybe spring for it.";
            let badgeText = "Case building";
            let moodText = "Podge is comparing finishes with narrowed eyes.";
            let summaryText = "This is either a wise upgrade or a very articulate excuse. The engine exists to tell the difference.";
            let verdictTone = "amber";

            if (score >= 8) {
                headlineText = "Buy the better one.";
                badgeText = "Upgrade justified";
                moodText = "Podge has stopped raising objections.";
                summaryText = "This looks like a genuine value upgrade rather than decorative self-deception.";
                verdictTone = "green";
            } else if (score <= 4) {
                headlineText = "The cheap one is probably fine.";
                badgeText = "Vibes detected";
                moodText = "Podge is not yet convinced.";
                summaryText = "The nicer version may be appealing, but the practical case for paying more still looks weak.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Use frequency is ${use}/10, failure pain is ${failure}/10, longevity is ${longevity}/10, joy is ${joy}/10, and price pain is ${pain}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This engine weighs how often you use the thing, how bad failure would be, how long the nicer version lasts, how much delight it adds, and how much the price hurts.",
                summary: summaryText,
                signals: [`${score}/10`, `${use}/10`, `${pain}/10`],
                verdictTone,
            };
        },
    };

    const updateResult = () => {
        const calculator = calculators[calculatorType];
        if (!calculator) {
            return;
        }
        clearError();
        setResult(calculator());
    };

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        try {
            updateResult();
        } catch (errorObject) {
            setError(errorObject.message || "Something went wrong.");
        }
    });

    form.addEventListener("input", () => {
        try {
            updateResult();
        } catch (errorObject) {
            setError(errorObject.message || "Something went wrong.");
        }
    });

    form.addEventListener("change", () => {
        try {
            updateResult();
        } catch (errorObject) {
            setError(errorObject.message || "Something went wrong.");
        }
    });

    resetButton?.addEventListener("click", () => {
        numberInputs.forEach((input, index) => {
            input.value = initialState.numbers[index];
        });
        dateInputs.forEach((input, index) => {
            input.value = initialState.dates[index];
        });
        selectInputs.forEach((input, index) => {
            input.value = initialState.selects[index];
        });
        checkboxInputs.forEach((input, index) => {
            input.checked = initialState.checks[index];
        });
        copyFeedback.textContent = "";
        try {
            updateResult();
        } catch (errorObject) {
            setError(errorObject.message || "Something went wrong.");
        }
    });

    copyButton?.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(buildCopyText());
            copyFeedback.textContent = "Result summary copied.";
        } catch (errorObject) {
            copyFeedback.textContent = "Copy failed. Select the text manually if needed.";
        }
    });

    try {
        updateResult();
    } catch (errorObject) {
        setError(errorObject.message || "Something went wrong.");
    }
});
