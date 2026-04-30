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
    const textareas = Array.from(form.querySelectorAll("textarea"));
    const selectInputs = Array.from(form.querySelectorAll("select"));
    const checkboxInputs = Array.from(form.querySelectorAll('input[type="checkbox"]'));
    const initialState = {
        numbers: numberInputs.map((input) => input.value),
        dates: dateInputs.map((input) => input.value),
        textareas: textareas.map((input) => input.value),
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
            const message = form.querySelector("#message-text").value.trim();
            const recipient = form.querySelector("#message-recipient").value;
            const intent = form.querySelector("#message-intent").value;
            const emotion = Number(form.querySelector("#message-emotion").value);
            const replyGap = Number(form.querySelector("#message-reply-gap").value);
            const reread = form.querySelector("#message-reread").checked;
            const screenshotRisk = form.querySelector("#message-screenshot").checked;

            if (!message) {
                throw new Error("Paste the message first.");
            }
            if (!Number.isFinite(emotion) || emotion < 1 || emotion > 10) {
                throw new Error("Use a score from 1 to 10 for emotional state.");
            }
            if (!Number.isFinite(replyGap) || replyGap < 0) {
                throw new Error("Use zero or more hours since the last reply.");
            }

            const recipientRiskMap = {
                partner: 5,
                ex: 8,
                friend: 4,
                boss: 9,
                colleague: 7,
                family: 5,
                "group-chat": 8,
            };
            const intentRiskMap = {
                clarify: 1,
                apologise: 2,
                flirt: 3,
                boundary: 3,
                win: 8,
                punish: 9,
                "pretend-fine": 7,
            };

            const lowercaseMessage = message.toLowerCase();
            const paragraphPenalty = message.split("\n").filter((line) => line.trim()).length >= 3 ? 2 : 0;
            const passiveAggressivePenalty = lowercaseMessage.includes("interesting that") || lowercaseMessage.includes("fine.") || lowercaseMessage.includes("whatever") ? 3 : 0;
            const courtroomPenalty = lowercaseMessage.includes("actually") || lowercaseMessage.includes("clearly") || lowercaseMessage.includes("obviously") ? 2 : 0;
            const screenshotPenalty = screenshotRisk ? 4 : 0;
            const rereadPenalty = reread ? 2 : 0;
            const replyGapPenalty = replyGap < 1 ? 2 : replyGap > 24 ? 1 : 0;

            const dramaRisk = Math.min(100, Math.max(0, Math.round((emotion * 7) + (intentRiskMap[intent] * 5) + passiveAggressivePenalty * 6 + courtroomPenalty * 5)));
            const screenshotScore = Math.min(100, Math.max(0, Math.round((recipientRiskMap[recipient] * 8) + screenshotPenalty * 6 + passiveAggressivePenalty * 5)));
            const sendability = Math.min(
                100,
                Math.max(
                    0,
                    Math.round(
                        95
                        - (emotion * 6)
                        - (recipientRiskMap[recipient] * 3)
                        - (intentRiskMap[intent] * 4)
                        - (paragraphPenalty * 5)
                        - (passiveAggressivePenalty * 5)
                        - (courtroomPenalty * 4)
                        - (screenshotPenalty * 3)
                        - (rereadPenalty * 3)
                        - (replyGapPenalty * 4)
                    )
                )
            );

            let headlineText = "Save it as a draft.";
            let badgeText = "Emotional grenade";
            let moodText = "Podge recommends waiting.";
            let summaryText = "This message reads more like pressure than communication. It will probably improve if you cut it back and come back later.";
            let verdictTone = "red";

            if (sendability >= 80) {
                headlineText = "Send it.";
                badgeText = "Good to go";
                moodText = "Podge sees no major structural problem.";
                summaryText = "Direct, proportionate, and unlikely to create extra drama. Send it before you add another paragraph.";
                verdictTone = "green";
            } else if (sendability >= 50) {
                headlineText = "Edit once, then decide.";
                badgeText = "Needs revision";
                moodText = "Podge recommends one calmer pass.";
                summaryText = "The core point may be valid, but the message is carrying enough extra heat that it could land badly as written.";
                verdictTone = "amber";
            } else if (sendability <= 20) {
                headlineText = "Do not send this.";
                badgeText = "Small legal proceeding";
                moodText = "Podge strongly recommends a pause.";
                summaryText = "This is not really a message yet. It reads more like a case file with feelings attached.";
            }

            return {
                headline: headlineText,
                detail: `Sendability is ${sendability}/100, drama risk is ${dramaRisk}/100, and screenshot risk is ${screenshotScore}/100.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This gauge looks at tone, emotional state, likely motive, recipient sensitivity, and how ugly the message would look if it escaped the chat window.",
                summary: summaryText,
                signals: [`${sendability}/100`, `${dramaRisk}/100`, `${screenshotScore}/100`],
                verdictTone,
            };
        },
        "main-character-risk": () => {
            const involvement = Number(form.querySelector("#main-involvement").value);
            const posting = form.querySelector("#main-posting").value;
            const asSomeone = form.querySelector("#main-as-someone").checked;
            const surprised = form.querySelector("#main-surprised").checked;
            const praise = form.querySelector("#main-praise").checked;
            const selfFocus = Number(form.querySelector("#main-self-focus").value);

            if (![involvement, selfFocus].every(Number.isFinite)) {
                throw new Error("Enter values for both scored fields.");
            }
            if ([involvement, selfFocus].some((value) => value < 1 || value > 10)) {
                throw new Error("Use scores from 1 to 10 for involvement and self-focus.");
            }

            const postingRisk = posting === "public" ? 9 : posting === "private" ? 4 : 1;
            const performance = (asSomeone ? 2 : 0) + (surprised ? 3 : 0) + (praise ? 3 : 0) + postingRisk;
            const score = Math.min(100, Math.max(0, Math.round(100 - (involvement * 6) + (selfFocus * 5) + (performance * 4))));

            let headlineText = "Step back a little.";
            let badgeText = "Elevated risk";
            let moodText = "Podge recommends stepping back.";
            let summaryText = "You may care about this, but the current version risks making the situation more about your performance than your relevance.";
            let verdictTone = "amber";

            if (score <= 35) {
                headlineText = "You are probably fine.";
                badgeText = "Low risk";
                moodText = "Podge sees no strong warning sign.";
                summaryText = "Your involvement appears direct enough that your contribution is less likely to feel intrusive.";
                verdictTone = "green";
            } else if (score >= 75) {
                headlineText = "This is becoming about you.";
                badgeText = "High risk";
                moodText = "Podge strongly recommends stepping back.";
                summaryText = "You may still care deeply. You just do not need to narrate this as if you are at the center of it.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Main character risk is ${score}/100, direct involvement is ${involvement}/10, and performance pressure is ${performance}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This calculator separates actual involvement from public performance, self-framing, and the subtle desire to be seen reacting well.",
                summary: summaryText,
                signals: [`${score}/100`, `${involvement}/10`, `${performance}/10`],
                verdictTone,
            };
        },
        "subscription-shame": () => {
            const monthlyCost = Number(form.querySelector("#subs-monthly").value);
            const annualCost = Number(form.querySelector("#subs-annual").value);
            const unusedCount = Number(form.querySelector("#subs-unused").value);
            const duplicateCount = Number(form.querySelector("#subs-duplicates").value);
            const renewToday = Number(form.querySelector("#subs-regret").value);
            const forgottenTrial = form.querySelector("#subs-forgotten").checked;

            if (![monthlyCost, annualCost, unusedCount, duplicateCount, renewToday].every(Number.isFinite)) {
                throw new Error("Enter values for all five fields.");
            }
            if (monthlyCost < 0 || annualCost < 0 || unusedCount < 0 || duplicateCount < 0 || renewToday < 0) {
                throw new Error("Use zero or more for all values.");
            }

            const monthlyLeakage = monthlyCost + (annualCost / 12);
            const annualLeakage = monthlyLeakage * 12;
            const forgetPenalty = forgottenTrial ? 12 : 0;
            const score = Math.min(100, Math.max(0, Math.round((monthlyLeakage * 1.1) + (unusedCount * 7) + (duplicateCount * 8) + forgetPenalty - (renewToday * 3))));

            let headlineText = "Direct-debit fog detected.";
            let badgeText = "High bloat";
            let moodText = "Podge recommends a review.";
            let summaryText = "Your stack may be doing useful things, but too much of it now looks automatic rather than intentional.";
            let verdictTone = "amber";

            if (score <= 30) {
                headlineText = "This stack looks fairly lean.";
                badgeText = "Controlled";
                moodText = "Podge sees manageable levels.";
                summaryText = "Most of your recurring payments still look deliberate rather than forgotten.";
                verdictTone = "green";
            } else if (score >= 70) {
                headlineText = "This stack is taking liberties.";
                badgeText = "Subscription shame";
                moodText = "Podge recommends an audit.";
                summaryText = "You are not just paying for services. You are also paying for momentum, forgetfulness, and a few things you may no longer want.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Monthly leakage is ${format(monthlyLeakage)}, annual leakage is ${format(annualLeakage)}, and the shame index comes out at ${score}/100.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This index combines the total spend with how much of the stack goes unused, duplicated, or simply forgotten.",
                summary: summaryText,
                signals: [`${score}/100`, `${format(monthlyLeakage)}`, `${unusedCount}`],
                verdictTone,
            };
        },
        "vaguepost-decoder": () => {
            const postText = form.querySelector("#vaguepost-text").value.trim();
            const platform = form.querySelector("#vaguepost-platform").value;
            const posterType = form.querySelector("#vaguepost-poster").value;
            const phraseCount = Number(form.querySelector("#vaguepost-phrases").value);
            const infoLevel = Number(form.querySelector("#vaguepost-info").value);
            const timing = form.querySelector("#vaguepost-timing").value;
            const dmMe = form.querySelector("#vaguepost-dm").checked;
            const notNaming = form.querySelector("#vaguepost-not-naming").checked;

            if (!postText) {
                throw new Error("Paste the vaguepost first.");
            }
            if (!Number.isFinite(phraseCount) || phraseCount < 0 || phraseCount > 12) {
                throw new Error("Use a phrase count between 0 and 12.");
            }
            if (!Number.isFinite(infoLevel) || infoLevel < 1 || infoLevel > 10) {
                throw new Error("Use an information score from 1 to 10.");
            }

            const platformRiskMap = {
                facebook: 6,
                x: 5,
                instagram: 7,
                linkedin: 8,
                tiktok: 6,
            };
            const posterRiskMap = {
                ex: 9,
                colleague: 6,
                "school-parent": 7,
                "linkedin-sage": 8,
                "gym-person": 5,
                "crypto-man": 8,
                "spiritual-chaos": 9,
                "barely-know": 6,
            };
            const timingRiskMap = {
                morning: 2,
                "work-hours": 4,
                evening: 5,
                "after-midnight": 8,
                "announcement-adjacent": 9,
            };

            const lowerText = postText.toLowerCase();
            const baitPhrases = [
                "some people",
                "you know who you are",
                "lesson learned",
                "protect your peace",
                "big things coming",
                "watch this space",
                "dm me",
                "i'm done explaining myself",
                "funny how people",
                "new chapter",
                "grateful for the real ones",
            ];
            const phraseHits = baitPhrases.reduce((count, phrase) => count + (lowerText.includes(phrase) ? 1 : 0), 0);
            const actualPhraseCount = Math.max(phraseCount, phraseHits);
            const infoContent = Math.max(1, Math.min(100, Math.round(infoLevel * 10)));
            const attentionFishing = Math.max(
                1,
                Math.min(
                    100,
                    Math.round(
                        20
                        + (actualPhraseCount * 8)
                        + (platformRiskMap[platform] * 3)
                        + (posterRiskMap[posterType] * 2)
                        + (timingRiskMap[timing] * 3)
                        + (dmMe ? 12 : 0)
                        + (notNaming ? 10 : 0)
                        + ((10 - infoLevel) * 4)
                    )
                )
            );
            const dramaProbability = Math.max(
                1,
                Math.min(100, Math.round((attentionFishing * 0.72) + (actualPhraseCount * 3) + (timingRiskMap[timing] * 2)))
            );

            let diagnosis = "Attention Fog";
            let headlineText = "Do not take the bait.";
            let badgeText = "Attention fog";
            let moodText = "Podge is refusing to ask what happened.";
            let summaryText = "This post contains almost no useful information and a dangerous amount of invitation.";
            let verdictTone = "amber";

            if (posterType === "linkedin-sage" && attentionFishing >= 70) {
                diagnosis = "LinkedIn Fog Machine";
            } else if (posterType === "ex" && dramaProbability >= 70) {
                diagnosis = "Ex-Bait With Candles";
            } else if (dmMe && attentionFishing >= 75) {
                diagnosis = "DM Me Hun Event";
            } else if (posterType === "spiritual-chaos" && actualPhraseCount >= 4) {
                diagnosis = "Spiritualised Attention Trap";
            } else if (posterType === "colleague" && notNaming) {
                diagnosis = "Workplace Subtweet";
            } else if (timing === "announcement-adjacent") {
                diagnosis = "Algorithmic Breadcrumbing";
            } else if (attentionFishing >= 65) {
                diagnosis = "Unresolved Group Chat Spillover";
            }

            if (attentionFishing <= 40 && infoContent >= 45) {
                headlineText = "Probably just vague, not weaponised.";
                badgeText = "Low bait";
                moodText = "Podge sees some ambiguity, not a full incident.";
                summaryText = "There is still some haze here, but it looks closer to ordinary oversharing than deliberate comment-harvesting.";
                verdictTone = "green";
            } else if (attentionFishing >= 80) {
                headlineText = diagnosis;
                badgeText = "High bait";
                moodText = "Podge recommends keeping your evening free of follow-up questions.";
                summaryText = "This was not written for everyone. It was written for a few specific people and performed for everyone else.";
                verdictTone = "red";
            } else {
                headlineText = diagnosis;
            }

            return {
                headline: headlineText,
                detail: `Attention fishing comes out at ${attentionFishing}%, drama probability is ${dramaProbability}%, and actual information content is ${infoContent}%.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This decoder looks at platform, archetype, stock bait phrases, timing, and how little the post actually says in exchange for how much it invites speculation.",
                summary: summaryText,
                signals: [`${attentionFishing}%`, `${dramaProbability}%`, `${infoContent}%`],
                verdictTone,
            };
        },
        "parent-phone-hypocrisy": () => {
            const parentScreenTime = Number(form.querySelector("#parent-screen-time").value);
            const parentUnlocks = Number(form.querySelector("#parent-unlocks").value);
            const parentBed = form.querySelector("#parent-bed").checked;
            const parentConvo = form.querySelector("#parent-convo").checked;
            const parentMinute = form.querySelector("#parent-minute").checked;
            const parentDoom = form.querySelector("#parent-doom").checked;
            const childAge = Number(form.querySelector("#child-age-hypocrisy").value);
            const childScreenTime = Number(form.querySelector("#child-screen-hypocrisy").value);
            const childImpact = Number(form.querySelector("#child-impact-hypocrisy").value);

            if (![parentScreenTime, parentUnlocks, childAge, childScreenTime, childImpact].every(Number.isFinite)) {
                throw new Error("Enter values for all scored fields.");
            }
            if (parentScreenTime < 0 || childScreenTime < 0 || parentUnlocks < 0) {
                throw new Error("Use zero or more for the screen and unlock values.");
            }
            if (childAge < 5 || childAge > 17) {
                throw new Error("Use a child age between 5 and 17.");
            }
            if (childImpact < 1 || childImpact > 10) {
                throw new Error("Use an impact score from 1 to 10.");
            }

            const parentSignals = (parentBed ? 2 : 0) + (parentConvo ? 3 : 0) + (parentMinute ? 3 : 0) + (parentDoom ? 2 : 0);
            const parentDrag = Math.min(10, Math.max(1, Math.round((parentScreenTime * 0.7) + (parentUnlocks / 20) + parentSignals)));
            const childPressure = Math.min(10, Math.max(1, Math.round((childScreenTime * 0.7) + childImpact + ((18 - childAge) / 4))));
            const moralAuthority = Math.max(1, Math.min(100, Math.round(100 - (parentDrag * 8) + (childPressure * 2))));

            let headlineText = "Patchy but trying.";
            let badgeText = "Compromised authority";
            let moodText = "Podge has noticed the mixed signals.";
            let summaryText = "The household rule may still be valid, but the adult example is making it harder to land cleanly.";
            let verdictTone = "amber";

            if (moralAuthority >= 70) {
                headlineText = "Clean enough to make the case.";
                badgeText = "Clean hands";
                moodText = "Podge sees a reasonably defensible example.";
                summaryText = "You are not perfect, but your own phone habits are controlled enough that the rule does not immediately collapse on contact.";
                verdictTone = "green";
            } else if (moralAuthority <= 35) {
                const doomscrollingMagistrate = parentDoom && parentBed && parentConvo;
                headlineText = doomscrollingMagistrate ? "Doomscrolling Magistrate." : "Full hypocrisy event.";
                badgeText = doomscrollingMagistrate ? "Low battery" : "Glass house parent";
                moodText = "Podge recommends less lecturing and more modelling.";
                summaryText = "You are trying to enforce phone discipline from inside the same swamp. The rule may be right. The example is not helping.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Moral authority battery is ${moralAuthority}%, parent screen drag is ${parentDrag}/10, and child pressure is ${childPressure}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This meter compares the child's phone pressure with the adult's own visible habits, because household discipline works differently when the parent is also clearly stuck to the rectangle.",
                summary: summaryText,
                signals: [`${moralAuthority}%`, `${parentDrag}/10`, `${childPressure}/10`],
                verdictTone,
            };
        },
        "fake-fan-detector": () => {
            const platform = form.querySelector("#fan-platform").value;
            const everywhere = Number(form.querySelector("#fan-everywhere").value);
            const comments = Number(form.querySelector("#fan-comments").value);
            const authenticity = form.querySelector("#fan-authentic").checked;
            const scripted = form.querySelector("#fan-scripted").checked;
            const explain = form.querySelector("#fan-explain").checked;

            if (![everywhere, comments].every(Number.isFinite)) {
                throw new Error("Enter values for both scored fields.");
            }
            if ([everywhere, comments].some((value) => value < 1 || value > 10)) {
                throw new Error("Use scores from 1 to 10 for both scored fields.");
            }

            const platformRiskMap = {
                tiktok: 8,
                instagram: 7,
                x: 6,
                youtube: 5,
                reddit: 4,
                linkedin: 8,
                news: 4,
            };
            const signalCount = (authenticity ? 2 : 0) + (scripted ? 3 : 0) + (explain ? 2 : 0);
            const campaignSignals = platformRiskMap[platform] + signalCount + Math.round((everywhere + comments) / 3);
            const organicChance = Math.max(0, Math.min(100, Math.round(100 - (campaignSignals * 6))));

            let headlineText = "Proceed with one eyebrow raised.";
            let badgeText = "Suspicious";
            let moodText = "Podge remains unconvinced.";
            let summaryText = "The attention may be real, but the enthusiasm around it does not yet look fully organic.";
            let verdictTone = "amber";

            if (organicChance >= 70) {
                headlineText = "This may be real enthusiasm.";
                badgeText = "Looks organic";
                moodText = "Podge sees fewer warning signs.";
                summaryText = "The pattern looks closer to ordinary excitement than a coordinated push.";
                verdictTone = "green";
            } else if (organicChance <= 30) {
                headlineText = "This hype looks farmed.";
                badgeText = "Low trust";
                moodText = "Podge is highly suspicious.";
                summaryText = "The pattern is coordinated enough that the hype may be doing more campaign work than discovery work.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Organic hype probability is ${organicChance}%, campaign signals are ${campaignSignals}/10, and comment similarity is ${comments}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This detector looks at how suddenly the hype appeared, how repetitive the language feels, and whether the enthusiasm sounds more orchestrated than spontaneous.",
                summary: summaryText,
                signals: [`${organicChance}%`, `${campaignSignals}/10`, `${comments}/10`],
                verdictTone,
            };
        },
        "phone-treaty": () => {
            const age = Number(form.querySelector("#treaty-age").value);
            const screenTime = Number(form.querySelector("#treaty-screen").value);
            const worry = form.querySelector("#treaty-worry").value;
            const enforcement = Number(form.querySelector("#treaty-enforcement").value);
            const apps = Number(form.querySelector("#treaty-apps").value);
            const friendsOnApps = form.querySelector("#treaty-friends").checked;
            const bedroomPhone = form.querySelector("#treaty-bedroom").checked;

            if (![age, screenTime, enforcement, apps].every(Number.isFinite)) {
                throw new Error("Enter values for all four scored fields.");
            }
            if (age < 5 || age > 17) {
                throw new Error("Use an age between 5 and 17.");
            }
            if (screenTime < 0 || enforcement < 1 || enforcement > 10 || apps < 0) {
                throw new Error("Check the screen time, enforcement, and app values.");
            }

            const worryRiskMap = {
                sleep: 8,
                bullying: 8,
                doomscrolling: 7,
                strangers: 9,
                distraction: 6,
                privacy: 7,
            };
            const agePressure = Math.max(0, 18 - age);
            const socialPressure = friendsOnApps ? 3 : 0;
            const bedroomPressure = bedroomPhone ? 4 : 0;
            const firmness = Math.min(
                100,
                Math.max(
                    0,
                    Math.round((agePressure * 4) + (screenTime * 4) + (apps * 3) + worryRiskMap[worry] + socialPressure + bedroomPressure + ((10 - enforcement) * 3))
                )
            );

            let headlineText = "Firm but negotiable.";
            let badgeText = "Treaty needed";
            let moodText = "Podge recommends structure.";
            let summaryText = "Your household probably needs clearer rules, but not necessarily an outright ban.";
            let verdictTone = "amber";

            if (firmness >= 75) {
                headlineText = "You need a firmer treaty.";
                badgeText = "High structure";
                moodText = "Podge recommends immediate rules.";
                summaryText = "The current setup looks loose enough that clearer boundaries will probably help more than case-by-case arguments.";
                verdictTone = "red";
            } else if (firmness <= 40) {
                headlineText = "Keep it simple and consistent.";
                badgeText = "Light structure";
                moodText = "Podge recommends a lighter agreement.";
                summaryText = "A simpler set of clear household rules may be enough without turning the phone into a permanent battleground.";
                verdictTone = "green";
            }

            return {
                headline: headlineText,
                detail: `Treaty firmness is ${firmness}/100, app pressure is ${apps}/10, and enforcement capacity is ${enforcement}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This generator weighs age, social pressure, screen habits, parental worries, and how enforceable the rules are likely to be in real life.",
                summary: summaryText,
                signals: [`${firmness}/100`, `${apps}/10`, `${enforcement}/10`],
                verdictTone,
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
        "future-embarrassment": () => {
            const postType = form.querySelector("#post-type").value;
            const emotion = Number(form.querySelector("#post-emotion").value);
            const audience = form.querySelector("#post-audience").value;
            const hasPrivateContext = form.querySelector("#post-private").checked;
            const futureComfort = form.querySelector("#post-future").checked;
            const intent = form.querySelector("#post-intent").value;

            if (!Number.isFinite(emotion) || emotion < 1 || emotion > 10) {
                throw new Error("Use a score from 1 to 10 for emotional state.");
            }

            const audienceRiskMap = {
                "close-friends": 3,
                mixed: 6,
                public: 8,
                work: 9,
            };
            const intentRiskMap = {
                connection: 1,
                information: 2,
                validation: 4,
                revenge: 8,
                boredom: 3,
            };
            const typeRiskMap = {
                opinion: 5,
                "life-update": 3,
                rant: 8,
                humblebrag: 6,
                work: 7,
                personal: 6,
            };

            const audienceRisk = audienceRiskMap[audience] || 5;
            const intentRisk = intentRiskMap[intent] || 3;
            const typeRisk = typeRiskMap[postType] || 5;
            const privateRisk = hasPrivateContext ? 3 : 0;
            const futureRisk = futureComfort ? 0 : 3;
            const score = Math.min(10, Math.max(1, Math.round((emotion + audienceRisk + intentRisk + typeRisk + privateRisk + futureRisk) / 3)));

            let headlineText = "Pause before posting.";
            let badgeText = "High caution";
            let moodText = "Podge recommends a pause.";
            let summaryText = "The current balance suggests reviewing the post again before putting it in front of other people.";
            let verdictTone = "amber";

            if (score <= 4) {
                headlineText = "Reasonably safe to post.";
                badgeText = "Low risk";
                moodText = "Podge sees no major warning sign.";
                summaryText = "This looks relatively calm and contained, so the risk of future embarrassment appears lower.";
                verdictTone = "green";
            } else if (score >= 8) {
                headlineText = "Keep this in drafts for now.";
                badgeText = "High risk";
                moodText = "Podge strongly recommends waiting.";
                summaryText = "This post carries enough emotional, audience, or privacy risk that waiting is likely the safer choice.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `Emotional heat is ${emotion}/10, audience risk is ${audienceRisk}/10, and the combined regret risk comes out at ${score}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This gauge looks at how emotional the moment is, how exposed the audience is, whether private context is involved, and whether the post still feels acceptable in the future.",
                summary: summaryText,
                signals: [`${score}/10`, `${emotion}/10`, `${audienceRisk}/10`],
                verdictTone,
            };
        },
        "sale-suspicion": () => {
            const originalPrice = Number(form.querySelector("#sale-original").value);
            const salePrice = Number(form.querySelector("#sale-price").value);
            const priorIntent = Number(form.querySelector("#sale-intent").value);
            const elsewhere = Number(form.querySelector("#sale-elsewhere").value);
            const clutter = Number(form.querySelector("#sale-clutter").value);
            const category = form.querySelector("#sale-category").value;

            if (![originalPrice, salePrice, priorIntent, elsewhere, clutter].every(Number.isFinite)) {
                throw new Error("Enter values for all five fields.");
            }
            if (originalPrice <= 0 || salePrice < 0) {
                throw new Error("Prices must be zero or more, and the original price must be above zero.");
            }
            if (salePrice > originalPrice) {
                throw new Error("Sale price should not be higher than the original price.");
            }
            if ([priorIntent, elsewhere, clutter].some((value) => value < 1 || value > 10)) {
                throw new Error("Use scores from 1 to 10 for the non-price questions.");
            }

            const discountPercent = ((originalPrice - salePrice) / originalPrice) * 100;
            const categoryAdjustmentMap = {
                tech: 1,
                clothes: -1,
                home: 0,
                diy: 1,
                garden: 0,
                impulse: -2,
            };
            const categoryAdjustment = categoryAdjustmentMap[category] || 0;
            const scoreRaw = (discountPercent / 10) + priorIntent + categoryAdjustment - elsewhere - (clutter / 2);
            const score = Math.min(10, Math.max(1, Math.round(scoreRaw)));

            let headlineText = "Useful, but check yourself.";
            let badgeText = "Mixed case";
            let moodText = "Podge is checking the label twice.";
            let summaryText = "The saving may be real, but the value of buying still needs a second look.";
            let verdictTone = "amber";

            if (score >= 8) {
                headlineText = "This looks like a real bargain.";
                badgeText = "Worthwhile";
                moodText = "Podge approves the arithmetic.";
                summaryText = "The discount looks substantial and the purchase itself appears justified, so this is more likely to be a genuine saving.";
                verdictTone = "green";
            } else if (score <= 4) {
                headlineText = "This sale is doing most of the work.";
                badgeText = "High suspicion";
                moodText = "Podge is not persuaded by the sticker.";
                summaryText = "The discount may be real, but the reasons for buying still look weak enough that this could be urgency rather than value.";
                verdictTone = "red";
            }

            return {
                headline: headlineText,
                detail: `The discount is ${format(discountPercent)}%, prior need is ${priorIntent}/10, and the overall usefulness score comes out at ${score}/10.`,
                badge: badgeText,
                mood: moodText,
                explainer: "This gauge separates the size of the discount from the usefulness of the purchase by weighing prior intent, outside price pressure, and clutter risk.",
                summary: summaryText,
                signals: [`${score}/10`, `${format(discountPercent)}%`, `${priorIntent}/10`],
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
        textareas.forEach((input, index) => {
            input.value = initialState.textareas[index];
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
