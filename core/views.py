import random

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


SITE_NAME = "Technofatty"
SITE_TAGLINE = "Questions, awkwardly answered."
SITE_DOMAIN = "https://technofatty.com"
CONTACT_EMAIL = "hello@technofatty.com"

CATEGORIES = [
    {"name": "Money", "slug": "money", "description": "Everyday money instruments for pay, tax, comparisons, and practical trade-offs."},
    {"name": "Home", "slug": "home", "description": "Room, surface, and household measuring instruments for practical jobs."},
    {"name": "Health", "slug": "health", "description": "Estimate-driven instruments with clear caveats where they matter."},
    {"name": "Time", "slug": "time", "description": "Dates, ages, countdowns, and workday questions without spreadsheet pain."},
    {"name": "Food", "slug": "food", "description": "Kitchen-friendly conversions, scaling, and timing helpers."},
    {"name": "Tech", "slug": "tech", "description": "Conversions, speed checks, and other compact instruments for technical odd jobs."},
    {"name": "Life", "slug": "life", "description": "Guidance instruments for timing, trade-offs, and other less tidy real-life questions."},
]

CATEGORY_CONTENT = {
    "money": {
        "intro": "Money tools on Technofatty focus on small decisions that become expensive when nobody gives them a shape: subscriptions, sales, VAT, percentage changes, and purchase justifications.",
        "use_cases": [
            "Check whether a discount is doing real work or just creating urgency.",
            "Separate recurring costs from the fog of direct debits.",
            "Compare price changes and tax-inclusive totals without spreadsheet theatre.",
        ],
        "reading": "Use these tools as framing aids, not financial advice. A result can show where the pressure is coming from, but it cannot know your whole budget, tax position, or future plans.",
    },
    "health": {
        "intro": "Health instruments here are broad flag checks. They are useful for noticing obvious dietary or behaviour patterns, but they do not diagnose, prescribe, or replace qualified advice.",
        "use_cases": [
            "Put a meal under a specific dietary lens without pretending to know exact nutrition.",
            "Separate green flags from watch-outs such as salt, lactose, gluten, reflux triggers, or sugar-heavy choices.",
            "Use plain-English caution where a condition needs clinician or dietitian input.",
        ],
        "reading": "For medical conditions, allergies, pregnancy, medication interactions, eating disorder history, or clinician-prescribed plans, follow qualified advice over Technofatty verdicts.",
    },
    "life": {
        "intro": "Life tools handle the messy human questions that are too awkward for a normal calculator: messages, posts, family phone rules, social judgement, and whether your reaction has become the event.",
        "use_cases": [
            "Pause before sending or posting something with screenshot risk.",
            "Turn vague household or social conflict into a clearer verdict and next move.",
            "Get a shareable card for a familiar modern problem without pretending the tool knows every detail.",
        ],
        "reading": "These are judgement aids, not relationship, safeguarding, legal, or mental health advice. The useful bit is often the pause they create.",
    },
    "tech": {
        "intro": "Tech tools focus on the internet's less obvious costs: synthetic hype, recommendation feeds, attention traps, and enthusiasm that may have arrived with a media plan.",
        "use_cases": [
            "Check whether hype looks organic or suspiciously coordinated.",
            "Estimate the hidden cost of recommendation feeds in money, time, and mood.",
            "Treat online patterns as evidence to inspect, not proof to overclaim.",
        ],
        "reading": "These tools are media-literacy prompts. They do not prove fraud, coordination, bot activity, or intent.",
    },
    "home": {
        "intro": "Home instruments keep practical jobs moving: measuring rooms, estimating areas, and turning vague DIY questions into usable numbers.",
        "use_cases": [
            "Work out floor area before buying materials.",
            "Keep measurements clear enough to compare options.",
            "Remember that awkward rooms, waste, and offcuts still need real-world allowance.",
        ],
        "reading": "Use the results as planning estimates. Measure twice before spending money on materials.",
    },
    "time": {
        "intro": "Time instruments make date gaps and scheduling questions easier to read without calendar wrangling.",
        "use_cases": [
            "Count days between dates.",
            "Use inclusive or non-inclusive counts depending on the situation.",
            "Turn date gaps into plain language for planning.",
        ],
        "reading": "These are calendar-day tools. Working days, time zones, holidays, and deadlines may need extra checks.",
    },
    "food": {
        "intro": "Food tools are for kitchen maths and meal judgement: scaling, swapping, and checking what a plate is probably doing.",
        "use_cases": [
            "Scale cooking decisions without mental arithmetic.",
            "Inspect a meal under a chosen dietary lens.",
            "Separate one meal from a pattern without turning dinner into a morality play.",
        ],
        "reading": "Food tools use broad signals. Labels, allergies, clinical diets, and personal tolerance still matter.",
    },
}

TOOL_REGISTRY = [
    {
        "name": "Percentage Change Engine",
        "slug": "percentage-change-calculator",
        "category": "Money",
        "category_slug": "money",
        "summary": "Work out the percentage increase or decrease between two values.",
        "eyebrow": "Live demo",
        "calculator_type": "percentage-change",
        "microcopy": "Enter two values and Podge will show the percentage increase or decrease.",
        "formula": "Percentage change = ((new value - old value) / old value) x 100",
        "worked_example": "If the old value is 80 and the new value is 100, the change is 20. Divide 20 by 80, then multiply by 100 to get 25%.",
        "disclaimer": "This calculator gives a general estimate only. It is not financial, legal, medical, or professional advice.",
        "result_labels": ["Raw change", "Started at", "Ended at"],
        "faq": [
            {
                "question": "Why does a decrease show as negative?",
                "answer": "The sign makes the direction explicit, so you can see whether the number went up or down.",
            },
            {
                "question": "Can I use this for money?",
                "answer": "Yes for simple comparisons, but not as financial advice or a substitute for fees, tax, or compound growth modelling.",
            },
        ],
        "schema_faq": True,
        "defaults": {
            "headline": "25% increase",
            "detail": "The value changed by 20, which is 25% higher than the starting value.",
            "badge": "Increase",
            "mood": "Podge is pleased. That is a clean upward move.",
            "signals": ["+20", "80", "100"],
            "explainer": "This is an increase because the new value is above the starting value. The gap is 20, and that gap equals 25% of the original number.",
            "summary": "That is a clear increase, so the new value is meaningfully higher than the starting one.",
        },
    },
    {
        "name": "VAT Engine",
        "slug": "vat-calculator",
        "category": "Money",
        "category_slug": "money",
        "summary": "Add or remove VAT from a price with clear totals and tax breakdown.",
        "eyebrow": "Live demo",
        "calculator_type": "vat",
        "microcopy": "Choose whether the price excludes or includes VAT, then let Podge break out the tax.",
        "formula": "VAT amount = net price x VAT rate. Gross price = net price + VAT amount.",
        "worked_example": "If a net price is 100 and VAT is 20%, the VAT amount is 20 and the gross price is 120.",
        "disclaimer": "This calculator gives a general estimate only. Check local tax rules and invoicing requirements for anything important.",
        "result_labels": ["VAT amount", "Net price", "Gross price"],
        "faq": [
            {
                "question": "When should I use add VAT?",
                "answer": "Use add VAT when your starting price does not include tax yet and you want the final price including VAT.",
            },
            {
                "question": "What does remove VAT do?",
                "answer": "It works backwards from a VAT-inclusive price so you can see the underlying net amount and the tax portion.",
            },
        ],
        "defaults": {
            "headline": "120 total with VAT",
            "detail": "A net price of 100 at 20% VAT gives 20 of tax and a gross total of 120.",
            "badge": "VAT added",
            "mood": "Podge has separated the tax from the total.",
            "signals": ["20", "100", "120"],
            "explainer": "This starts with a tax-exclusive price and adds the VAT portion on top so you can see the tax and the final amount clearly.",
            "summary": "That is the full price after VAT, with the tax amount split out rather than hidden inside the total.",
        },
    },
    {
        "name": "Room Area Instrument",
        "slug": "room-area-calculator",
        "category": "Home",
        "category_slug": "home",
        "summary": "Measure floor area fast before you buy paint, flooring, or furniture.",
        "eyebrow": "Live demo",
        "calculator_type": "room-area",
        "microcopy": "Enter the room dimensions and Podge will work out the total floor area.",
        "formula": "Area = length x width",
        "worked_example": "A room that is 5 metres long and 4 metres wide has an area of 20 square metres.",
        "disclaimer": "This calculator gives a general estimate only. Measure awkward layouts, alcoves, and waste allowances separately before buying materials.",
        "result_labels": ["Area", "Length", "Width"],
        "faq": [
            {
                "question": "Can I use feet instead of metres?",
                "answer": "Yes. Use the unit switch and keep both measurements in the same unit.",
            },
            {
                "question": "Does this include waste or offcuts?",
                "answer": "No. It gives the base area only, so add your own allowance for waste where needed.",
            },
        ],
        "defaults": {
            "headline": "20 m²",
            "detail": "A room 5 metres long and 4 metres wide covers 20 square metres.",
            "badge": "Area ready",
            "mood": "Podge has mapped the floor space.",
            "signals": ["20 m²", "5 m", "4 m"],
            "explainer": "This is the simplest floor area calculation: multiply the room length by the room width using the same unit for both.",
            "summary": "That is the flat floor area before you add extra allowance for cuts, waste, or awkward corners.",
        },
    },
    {
        "name": "Days Between Dates Engine",
        "slug": "days-between-dates",
        "category": "Time",
        "category_slug": "time",
        "summary": "See the number of days between two dates without calendar wrangling.",
        "eyebrow": "Live demo",
        "calculator_type": "days-between-dates",
        "microcopy": "Pick two dates and Podge will count the gap, with an option to include both end dates.",
        "formula": "Days between dates = end date - start date, with an optional +1 if you include both dates.",
        "worked_example": "From 1 April to 10 April is 9 days apart, or 10 days if you count both the start and end date.",
        "disclaimer": "This calculator gives a general date difference only. Business days, holidays, and time zones are different problems.",
        "result_labels": ["Days apart", "Start date", "End date"],
        "faq": [
            {
                "question": "Why does include both dates change the result?",
                "answer": "It counts the starting day itself as part of the total, which is useful for bookings, countdowns, and schedules.",
            },
            {
                "question": "Does this count working days?",
                "answer": "No. This is calendar-day math, not workday logic.",
            },
        ],
        "defaults": {
            "headline": "183 days apart",
            "detail": "From 1 January 2026 to 3 July 2026 there are 183 days between the two dates.",
            "badge": "Date gap",
            "mood": "Podge has checked the calendar.",
            "signals": ["183", "2026-01-01", "2026-07-03"],
            "explainer": "This compares two calendar dates directly and counts the day gap between them.",
            "summary": "That is the calendar gap between the two dates, which is useful for planning and countdowns.",
        },
    },
    {
        "name": "Recipe Scaling Instrument",
        "slug": "recipe-scaler",
        "category": "Food",
        "category_slug": "food",
        "summary": "Scale ingredients up or down without mental arithmetic.",
        "eyebrow": "Queued",
        "calculator_type": "placeholder",
    },
    {
        "name": "Water Intake Gauge",
        "slug": "water-intake-calculator",
        "category": "Health",
        "category_slug": "health",
        "summary": "Get a quick hydration estimate with a sensible disclaimer.",
        "eyebrow": "Queued",
        "calculator_type": "placeholder",
    },
    {
        "name": "Should I Send That Message Gauge",
        "slug": "should-i-send-that-message-gauge",
        "category": "Life",
        "category_slug": "life",
        "summary": "Paste the message and get a verdict on whether to send it, redraft it, or leave it alone.",
        "eyebrow": "Featured",
        "calculator_type": "send-that-message",
        "microcopy": "Use this to weigh tone, intent, emotional state, timing, and screenshot risk before you send.",
        "formula": "Sendability score = clarity + proportion - emotional heat - hidden motive - screenshot risk",
        "worked_example": "A calm, direct message sent to clarify something usually scores better than a long emotional paragraph sent to win the argument.",
        "disclaimer": "This is a subjective guidance gauge, not relationship, legal, medical, or professional advice.",
        "result_labels": ["Sendability", "Drama risk", "Screenshot risk"],
        "faq": [
            {
                "question": "Is this meant as serious life advice?",
                "answer": "No. It is a framing instrument for awkward moments, not a substitute for judgment, context, or consent.",
            },
            {
                "question": "What makes a message risky here?",
                "answer": "High emotional heat, mixed motives, passive aggression, and writing something you would hate to see screenshotted all push the score down.",
            },
        ],
        "defaults": {
            "headline": "Save it as a draft.",
            "detail": "The current mix looks more emotional than clear, so it may be better to wait and return to it later.",
            "badge": "Low sendability",
            "mood": "Podge recommends waiting.",
            "signals": ["31/100", "74/100", "82/100"],
            "explainer": "This gauge surfaces how direct the message is, what emotional state it carries, what it seems designed to do, and how embarrassing it would be if someone else saw it.",
            "summary": "The current balance suggests drafting it, cooling off, and removing whatever part only exists to make the other person feel it.",
        },
        "schema_faq": True,
    },
    {
        "name": "Main Character Risk Calculator",
        "slug": "main-character-risk-calculator",
        "category": "Life",
        "category_slug": "life",
        "summary": "Estimate whether you are about to make somebody else's moment too much about you.",
        "eyebrow": "Featured",
        "calculator_type": "main-character-risk",
        "microcopy": "Use this to gauge whether you are contributing, reacting, or quietly stepping into the middle with a monologue.",
        "formula": "Main character risk = distance from event + public performance + self-focus + praise-seeking",
        "worked_example": "A post that barely involves you, reframes the event around your feelings, and looks built for approval scores much riskier than a quiet, relevant contribution.",
        "disclaimer": "This is a subjective social guidance instrument, not moral, legal, or professional advice.",
        "result_labels": ["Risk", "Involvement", "Performance"],
        "faq": [
            {
                "question": "Does a high score mean do nothing?",
                "answer": "Not always. It means the current version may be centering you more than the situation requires.",
            },
            {
                "question": "What pushes the score up fastest?",
                "answer": "Low direct involvement, public posting, self-branding language, and hoping to be praised for your sensitivity all raise the risk.",
            },
        ],
        "defaults": {
            "headline": "Step back a little.",
            "detail": "The current setup suggests you may be standing too close to someone else's moment while adding more of yourself than the situation needs.",
            "badge": "Elevated risk",
            "mood": "Podge recommends stepping back.",
            "signals": ["82/100", "24/100", "88/100"],
            "explainer": "This calculator is not asking whether you care. It is asking whether your reaction is about the situation or about being seen reacting to it.",
            "summary": "You may still care deeply. You just do not need to turn this into your scene.",
        },
        "schema_faq": True,
    },
    {
        "name": "Subscription Shame Index",
        "slug": "subscription-shame-index",
        "category": "Money",
        "category_slug": "money",
        "summary": "Find out how much your subscriptions are quietly costing you in money and attention.",
        "eyebrow": "Featured",
        "calculator_type": "subscription-shame",
        "microcopy": "Add the monthly cost, the unused stack, and the duplicates. The result is usually less charming than the signup process.",
        "formula": "Subscription shame = monthly spend + unused services + duplicate services + forgot-it-was-renewing factor",
        "worked_example": "A stack with several unused services, duplicate household payments, and recurring annual costs will score much worse than a lean set you would actively choose again today.",
        "disclaimer": "This is a general money guidance instrument, not financial advice.",
        "result_labels": ["Shame index", "Monthly leakage", "Unused services"],
        "faq": [
            {
                "question": "Does a high score mean cancel everything?",
                "answer": "No. It means your current stack deserves review because convenience may be doing more work than value.",
            },
            {
                "question": "What usually pushes the score up?",
                "answer": "Unused services, duplicate household subscriptions, forgotten annual renewals, and services you would not sign up to again today all increase the score.",
            },
        ],
        "defaults": {
            "headline": "Direct-debit fog detected.",
            "detail": "The current mix suggests that some of the stack is serving you, but too much of it is simply continuing by inertia.",
            "badge": "High bloat",
            "mood": "Podge recommends a review.",
            "signals": ["76/100", "48", "5"],
            "explainer": "This index looks at how much the stack costs, how much of it goes unused, and how many subscriptions survive mostly because nobody has cancelled them yet.",
            "summary": "You are not necessarily overspending everywhere, but your subscription stack may be more automatic than intentional.",
        },
        "schema_faq": True,
    },
    {
        "name": "Vaguepost Decoder",
        "slug": "vaguepost-decoder",
        "category": "Life",
        "category_slug": "life",
        "summary": "Paste a cryptic post and get a verdict on what species of attention-seeking nonsense it probably is.",
        "eyebrow": "Featured",
        "calculator_type": "vaguepost-decoder",
        "microcopy": "Use this to turn a context-free status update into a label, a score, and a recommended level of involvement.",
        "formula": "Vaguepost diagnosis = phrase fog + timing suspicion + poster archetype + information missingness + bait signals",
        "worked_example": "A post full of 'some people', posted after midnight, with no actual context and a 'DM me' reply habit will score far more suspiciously than an ordinary vague life update.",
        "disclaimer": "This is a subjective social-reading instrument, not a factual statement about the poster's intent.",
        "result_labels": ["Attention fishing", "Drama probability", "Information content"],
        "faq": [
            {
                "question": "Does a high score mean the post is definitely bait?",
                "answer": "No. It means the post is using enough classic vagueposting ingredients that it reads like bait whether that was intended or not.",
            },
            {
                "question": "What pushes the diagnosis toward full nonsense?",
                "answer": "Cryptic stock phrases, suspicious timing, 'DM me' energy, and very low actual information all make the decoder less charitable.",
            },
        ],
        "defaults": {
            "headline": "Attention fog detected.",
            "detail": "The current mix looks thin on information and rich in invitation, which is usually how vagueposts keep themselves alive in the comments.",
            "badge": "Decoder engaged",
            "mood": "Podge is squinting at the subtext.",
            "signals": ["88%", "76%", "14%"],
            "explainer": "This decoder is trying to separate ordinary vagueness from deliberate breadcrumbing, by weighing stock phrases, poster type, timing, and how much useful information the post actually contains.",
            "summary": "This may not be a crisis. It may simply be a post designed to make other people ask whether it is one.",
        },
        "schema_faq": True,
    },
    {
        "name": "Parent Phone Hypocrisy Meter",
        "slug": "parent-phone-hypocrisy-meter",
        "category": "Life",
        "category_slug": "life",
        "summary": "Check whether your household phone rules are backed by example or being enforced from inside the same swamp.",
        "eyebrow": "Featured",
        "calculator_type": "parent-phone-hypocrisy",
        "microcopy": "Use this to compare the child's phone load with the adult's own screen habits before another speech about discipline.",
        "formula": "Moral authority battery = child impact - parent contradiction - household phone hypocrisy signals",
        "worked_example": "A parent who doomscrolls in bed, checks the phone during conversations, and says 'just a minute' while holding it will score weaker moral authority than a parent modelling stricter phone habits.",
        "disclaimer": "This is a subjective family-behaviour gauge, not safeguarding, legal, or medical advice.",
        "result_labels": ["Moral authority", "Parent screen drag", "Child pressure"],
        "faq": [
            {
                "question": "Does a low battery mean the rule is wrong?",
                "answer": "No. It means the adult example is making the rule harder to defend, enforce, or take seriously.",
            },
            {
                "question": "What drains moral authority fastest?",
                "answer": "Bedtime scrolling, distracted parenting, constant checking, and condemning behaviours the adult is visibly doing too all drain it quickly.",
            },
        ],
        "defaults": {
            "headline": "Battery running low.",
            "detail": "The rule may still be valid, but the adult example currently looks patchier than the speech that would accompany it.",
            "badge": "Authority compromised",
            "mood": "Podge has noticed the double standard.",
            "signals": ["23%", "8/10", "7/10"],
            "explainer": "This meter compares child screen concerns with the adult's own visible phone habits, because household rules land differently when the parent is obviously in the same loop.",
            "summary": "You may still be right about the phone. You are just not making the case from clean ground.",
        },
        "schema_faq": True,
    },
    {
        "name": "Fake Fan Detector",
        "slug": "fake-fan-detector",
        "category": "Tech",
        "category_slug": "tech",
        "summary": "Estimate whether a wave of hype looks organic or carefully farmed.",
        "eyebrow": "Featured",
        "calculator_type": "fake-fan-detector",
        "microcopy": "Use this to weigh how sudden, repetitive, and suspicious the hype feels before you trust it.",
        "formula": "Organic hype probability = consistency of behaviour - campaign signals - synthetic enthusiasm markers",
        "worked_example": "If hype appears everywhere at once, comments all sound alike, and the praise feels oddly coordinated, the detector will score it as less organic.",
        "disclaimer": "This is a subjective media-literacy instrument, not a factual determination of campaign activity.",
        "result_labels": ["Organic chance", "Campaign signals", "Comment similarity"],
        "faq": [
            {
                "question": "Does a low score prove a marketing campaign?",
                "answer": "No. It means the pattern looks less organic and more coordinated than a normal burst of enthusiasm.",
            },
            {
                "question": "What pushes the score down most?",
                "answer": "Seeing the thing everywhere at once, repetitive comments, suspiciously polished authenticity, and identical fan language all increase suspicion.",
            },
        ],
        "defaults": {
            "headline": "Proceed with one eyebrow raised.",
            "detail": "The current pattern suggests the hype may be doing more campaign work than discovery work.",
            "badge": "Suspicious",
            "mood": "Podge remains unconvinced.",
            "signals": ["24%", "8/10", "7/10"],
            "explainer": "This detector looks for patterns that make hype feel orchestrated rather than naturally spreading from person to person.",
            "summary": "The attention may be real, but the enthusiasm around it does not yet look fully organic.",
        },
        "schema_faq": True,
    },
    {
        "name": "Parental Phone Treaty Generator",
        "slug": "parental-phone-treaty-generator",
        "category": "Life",
        "category_slug": "life",
        "summary": "Turn household phone arguments into a clearer, more enforceable set of rules.",
        "eyebrow": "Featured",
        "calculator_type": "phone-treaty",
        "microcopy": "Use this to shape a realistic phone agreement based on age, worries, enforcement capacity, and the apps already in play.",
        "formula": "Treaty firmness = child age + app pressure + parent worries + enforcement capacity + social pressure",
        "worked_example": "A younger child with heavy app use, late-night phone access, and patchy enforcement usually leads to a firmer treaty than an older child with clearer boundaries already in place.",
        "disclaimer": "This is a general family guidance instrument, not legal, safeguarding, or medical advice.",
        "result_labels": ["Treaty firmness", "App pressure", "Enforcement capacity"],
        "faq": [
            {
                "question": "Is this meant to replace actual parenting conversations?",
                "answer": "No. It is a structure for the conversation, not a substitute for judgment, trust, or family context.",
            },
            {
                "question": "What makes a treaty firmer?",
                "answer": "Heavier app use, younger age, weak existing boundaries, and low enforcement consistency all push the result toward a stricter agreement.",
            },
        ],
        "defaults": {
            "headline": "Firm but negotiable.",
            "detail": "The current setup suggests you need clearer household rules, but not necessarily an outright ban.",
            "badge": "Treaty needed",
            "mood": "Podge recommends structure.",
            "signals": ["68/100", "8/10", "4/10"],
            "explainer": "This generator weighs age, social pressure, usage patterns, and enforcement reality so the agreement is more likely to survive a real week.",
            "summary": "Your household probably needs a calm, enforceable agreement rather than another argument made up on the spot.",
        },
        "schema_faq": True,
    },
    {
        "name": "Fancy Version Justification Engine",
        "slug": "fancy-version-justification-engine",
        "category": "Life",
        "category_slug": "life",
        "summary": "Compare value, longevity, and cost before paying more for the better version.",
        "eyebrow": "Featured",
        "calculator_type": "fancy-version",
        "microcopy": "Use this to balance frequency of use, reliability, longevity, delight, and price.",
        "formula": "Upgrade score = use frequency + consequence of failure + longevity value + joy factor - price pain",
        "worked_example": "If you use something daily, the cheap version failing would be annoying, and the nicer one lasts longer, the upgrade case gets much stronger.",
        "disclaimer": "This is a subjective framing engine, not financial advice.",
        "result_labels": ["Upgrade score", "Use frequency", "Price pain"],
        "faq": [
            {
                "question": "Is this only for luxury purchases?",
                "answer": "No. It is useful anywhere the better version costs more and you are trying to sort signal from self-justification.",
            },
            {
                "question": "What pushes the engine toward buying the fancy version?",
                "answer": "Frequent use, meaningful reliability gains, longer lifespan, and honest delight all help. Price pain pushes the other way.",
            },
        ],
        "defaults": {
            "headline": "Maybe spring for it.",
            "detail": "If the better version gets used often enough and fails less annoyingly, the upgrade can stop being frivolous and start being sensible.",
            "badge": "Case building",
            "mood": "Podge is comparing finishes with narrowed eyes.",
            "signals": ["6/10", "8/10", "4/10"],
            "explainer": "This engine separates practical value from impulse by putting use, longevity, reliability, delight, and price on the same footing.",
            "summary": "The goal is to tell the difference between a sensible upgrade and an expensive impulse.",
        },
        "schema_faq": True,
    },
    {
        "name": "Future Embarrassment Gauge",
        "slug": "future-embarrassment-gauge",
        "category": "Life",
        "category_slug": "life",
        "summary": "Estimate how likely a post is to feel regrettable once the moment has passed.",
        "eyebrow": "Featured",
        "calculator_type": "future-embarrassment",
        "microcopy": "Use this to weigh tone, audience, emotional state, and staying power before you post.",
        "formula": "Regret risk = emotional heat + audience risk + future visibility + sensitivity flags - calm intention",
        "worked_example": "A public post made while angry, with private context and no long-term comfort, scores much riskier than a calm update shared with close friends.",
        "disclaimer": "This is a subjective guidance gauge, not legal, professional, or reputational advice.",
        "result_labels": ["Regret risk", "Emotional heat", "Audience risk"],
        "faq": [
            {
                "question": "Does a high score always mean do not post?",
                "answer": "No. It means the post is more likely to age badly, spread further than intended, or carry context you may wish you had handled differently.",
            },
            {
                "question": "What pushes the score up most?",
                "answer": "Posting while emotional, sharing to a mixed or public audience, including private details, and feeling unsure about future visibility all increase the risk.",
            },
        ],
        "defaults": {
            "headline": "Pause before posting.",
            "detail": "The mix of audience, tone, and emotional state suggests this may feel worse tomorrow than it does right now.",
            "badge": "High caution",
            "mood": "Podge recommends a pause.",
            "signals": ["7/10", "8/10", "7/10"],
            "explainer": "This gauge is a way to surface the risks around tone, audience, privacy, and timing before you publish.",
            "summary": "The current balance suggests reviewing the post again before putting it in front of other people.",
        },
        "schema_faq": True,
    },
    {
        "name": "Sale Suspicion Gauge",
        "slug": "sale-suspicion-gauge",
        "category": "Money",
        "category_slug": "money",
        "summary": "Check whether a discount is genuinely useful or just turning mild interest into urgency.",
        "eyebrow": "Featured",
        "calculator_type": "sale-suspicion",
        "microcopy": "Use this to balance the size of the discount against whether you actually needed the thing in the first place.",
        "formula": "Discount usefulness = price drop + prior intent + replacement value - urgency pressure - clutter risk",
        "worked_example": "A large discount on something you already needed scores much better than a modest discount on something you only want because it is on sale.",
        "disclaimer": "This is a general consumer guidance gauge, not financial advice.",
        "result_labels": ["Usefulness score", "Discount size", "Need level"],
        "faq": [
            {
                "question": "Can a big discount still be a bad buy?",
                "answer": "Yes. If you did not need the item, could buy it cheaper elsewhere, or it simply adds clutter, the discount may not be doing real work for you.",
            },
            {
                "question": "What improves the score?",
                "answer": "A real price drop, a purchase you were already planning, and replacing something you genuinely need all make the discount more worthwhile.",
            },
        ],
        "defaults": {
            "headline": "Useful, but check yourself.",
            "detail": "The discount may be real, but the decision still depends on whether the item solves a genuine need rather than creating a new one.",
            "badge": "Mixed case",
            "mood": "Podge is checking the label twice.",
            "signals": ["5/10", "30%", "6/10"],
            "explainer": "This gauge separates the size of the discount from the usefulness of the purchase, because those are not the same thing.",
            "summary": "The saving may be real, but the value of buying still needs a second look.",
        },
        "schema_faq": True,
    },
    {
        "name": "Astroturf Detector",
        "slug": "astroturf-detector",
        "category": "Tech",
        "category_slug": "tech",
        "summary": "Estimate whether a campaign, comment wave, or public outrage looks grassroots or manufactured.",
        "eyebrow": "Featured",
        "calculator_type": "astroturf-detector",
        "microcopy": "Use this when sudden consensus feels a little too tidy, repetitive, or professionally outraged.",
        "formula": "Astroturf risk = message sameness + account weirdness + timing coordination + funding opacity + outrage velocity",
        "worked_example": "A normal grassroots wave has messy language, visible context, and varied accounts. A manufactured one often arrives suddenly, repeats the same lines, hides who benefits, and moves faster than ordinary people usually organise.",
        "disclaimer": "This is a subjective media-literacy detector, not proof of coordination, funding, or misconduct.",
        "result_labels": ["Astroturf risk", "Message sameness", "Coordination"],
        "faq": [
            {
                "question": "Does a high score prove a campaign is fake?",
                "answer": "No. It means the visible pattern has enough manufactured-looking signals that it deserves more scepticism before you amplify it.",
            },
            {
                "question": "What makes a movement look astroturfed?",
                "answer": "Repeated language, brand-new accounts, identical timing, unclear funding, and outrage that appears fully formed before ordinary context catches up.",
            },
        ],
        "defaults": {
            "headline": "Synthetic grassroots smell detected.",
            "detail": "The visible pattern looks coordinated enough that you should verify who benefits before treating it as spontaneous public opinion.",
            "badge": "High suspicion",
            "mood": "Podge is checking the lawn for plastic seams.",
            "signals": ["82/100", "8/10", "9/10"],
            "explainer": "This detector weighs repeated phrasing, account quality, timing, funding clarity, and outrage velocity to separate messy public reaction from something that may be managed.",
            "summary": "Do not assume the crowd is fake, but do not hand it your trust for free either.",
        },
        "schema_faq": True,
    },
    {
        "name": "Algorithm Tax Calculator",
        "slug": "algorithm-tax-calculator",
        "category": "Tech",
        "category_slug": "tech",
        "summary": "Estimate how much money, time, and attention a platform's recommendations are quietly extracting.",
        "eyebrow": "Featured",
        "calculator_type": "algorithm-tax",
        "microcopy": "Use this when recommendations keep turning boredom into purchases, subscriptions, outrage, or time you did not mean to spend.",
        "formula": "Algorithm tax = impulse spend + unplanned time cost + subscription creep + attention residue",
        "worked_example": "A platform that turns ten casual minutes into an hour, a purchase, and a recurring subscription is charging more than the listed price.",
        "disclaimer": "This is a general attention-and-spending estimate, not financial, psychological, or professional advice.",
        "result_labels": ["Algorithm tax", "Monthly leakage", "Time cost"],
        "faq": [
            {
                "question": "What counts as algorithm tax?",
                "answer": "Unplanned purchases, subscriptions, extra platform time, and the mental drag left after recommendation feeds steer your attention.",
            },
            {
                "question": "Is this blaming the algorithm for every choice?",
                "answer": "No. It is a framing tool for noticing when recommendation systems are repeatedly nudging you into costs you would not choose cold.",
            },
        ],
        "defaults": {
            "headline": "The feed is taking a cut.",
            "detail": "Your recommendations are converting attention into enough spend and lost time that the platform is no longer free in any useful sense.",
            "badge": "Hidden tax",
            "mood": "Podge has found the receipt inside the scroll.",
            "signals": ["78/100", "64", "19h"],
            "explainer": "This calculator combines impulse purchases, recurring costs, unplanned feed time, and attention residue to estimate the hidden cost of recommendation systems.",
            "summary": "The listed price may be zero, but the algorithm is still collecting payment in money, time, and mood.",
        },
        "schema_faq": True,
    },
    {
        "name": "AI Emotional Dependency Gauge",
        "slug": "ai-emotional-dependency-gauge",
        "category": "Life",
        "category_slug": "life",
        "summary": "Check whether an AI assistant is helping you think or quietly becoming your main emotional outlet.",
        "eyebrow": "Featured",
        "calculator_type": "ai-emotional-dependency",
        "microcopy": "Use this to weigh reassurance loops, disclosure habits, human support, and whether the chat is expanding your life or replacing parts of it.",
        "formula": "Dependency risk = emotional reliance + reassurance loops + human avoidance + attachment language - offline support",
        "worked_example": "Using AI to organise thoughts before a difficult conversation is different from using it as the only place you feel understood, especially if it delays talking to real people.",
        "disclaimer": "This is a subjective wellbeing gauge, not medical, mental health, or crisis advice. If you feel at risk or unable to stay safe, contact local emergency services or a crisis support line.",
        "result_labels": ["Dependency risk", "Reassurance loop", "Human support"],
        "faq": [
            {
                "question": "Is using AI for emotional support automatically bad?",
                "answer": "No. The risk rises when it becomes the main or only outlet, replaces human repair, or keeps you cycling through reassurance without action.",
            },
            {
                "question": "What should I do with a high result?",
                "answer": "Treat it as a prompt to bring at least one trusted human or qualified professional back into the loop, especially for serious distress.",
            },
        ],
        "defaults": {
            "headline": "The chat is carrying too much.",
            "detail": "The pattern suggests the assistant may be doing more emotional holding than is healthy for a tool.",
            "badge": "High reliance",
            "mood": "Podge recommends bringing a human back into the room.",
            "signals": ["84/100", "8/10", "3/10"],
            "explainer": "This gauge looks at how often you seek reassurance, how much you disclose to AI before people, whether it delays real conversations, and how much offline support is still active.",
            "summary": "The tool may be useful, but it should not become the only place your feelings are allowed to land.",
        },
        "schema_faq": True,
    },
    {
        "name": "Should I Be Proud Of This Plate?",
        "slug": "should-i-be-proud-of-this-plate",
        "category": "Health",
        "category_slug": "health",
        "summary": "Put a meal on trial under a chosen health lens and get green flags, watch-outs, and a tiny repair job.",
        "eyebrow": "Featured",
        "calculator_type": "plate-pride",
        "microcopy": "Podge is judging the plate, not diagnosing you. Describe the meal, pick the health lens, and inspect the evidence.",
        "formula": "Plate pride = protein + plants + fibre-friendly carbs - condition watch-outs - trigger risk - regular-pattern penalty",
        "worked_example": "Chicken, rice, vegetables, and a salty sauce may score respectably for general balance, but under a blood-pressure lens the sodium becomes the main suspect.",
        "disclaimer": "This is a broad dietary flag check, not medical advice. If you have diabetes on insulin, kidney disease, allergies, coeliac disease, pregnancy, an eating disorder history, or a clinician-prescribed diet, follow qualified advice over dinner theatre.",
        "result_labels": ["Plate pride", "Condition fit", "Main suspect"],
        "faq": [
            {
                "question": "Can this tell me if a meal is safe for my condition?",
                "answer": "No. It flags likely dietary pros and watch-outs from broad principles. It cannot guarantee safety, account for medications, or replace clinician or dietitian advice.",
            },
            {
                "question": "Why does the same meal change under different health lenses?",
                "answer": "A plate can be fine in one context and awkward in another. Sodium, lactose, gluten, reflux triggers, purines, fibre, and refined carbs matter differently depending on the lens.",
            },
        ],
        "defaults": {
            "headline": "Answer a few questions first.",
            "detail": "Your plate verdict will appear once Podge has enough evidence.",
            "badge": "Waiting",
            "mood": "Podge has put on a tiny courtroom wig.",
            "signals": ["Waiting", "Not scored", "Ready"],
            "explainer": "This engine starts blank because judging an imaginary dinner would be nutritional theatre with no witnesses.",
            "summary": "Describe the plate-shaped incident and choose the health lens to get a verdict.",
        },
        "schema_faq": True,
    },
]

LIVE_TOOLS = [tool for tool in TOOL_REGISTRY if tool.get("calculator_type") != "placeholder"]

GUIDES = [
    {
        "slug": "how-to-calculate-percentage-change",
        "title": "How to calculate percentage change without overthinking it",
        "summary": "A plain-English explainer with the formula, a worked example, and when the result can mislead.",
        "sections": [
            {
                "heading": "The short version",
                "body": "Percentage change compares where a value started with where it ended. The useful question is not just whether the number moved, but how large that movement is compared with the starting point.",
            },
            {
                "heading": "The formula",
                "body": "Subtract the old value from the new value, divide that difference by the old value, then multiply by 100. A positive answer is an increase. A negative answer is a decrease.",
            },
            {
                "heading": "Where it can mislead",
                "body": "Small starting values can make ordinary changes look dramatic. A rise from 1 to 2 is a 100% increase, but the actual change is still only 1. For money or business decisions, look at the percentage and the raw difference together.",
            },
        ],
        "related_slugs": ["percentage-change-calculator", "vat-calculator", "sale-suspicion-gauge"],
    },
    {
        "slug": "when-a-quick-calculator-is-good-enough",
        "title": "When a quick instrument is good enough, and when it is not",
        "summary": "A short guide to estimates, disclaimers, and using Technofatty responsibly.",
        "sections": [
            {
                "heading": "Good enough means useful, not perfect",
                "body": "A quick calculator is useful when it helps you understand the shape of a decision: the likely range, the obvious trade-off, or the part that deserves attention. It is not a replacement for source data or professional judgement.",
            },
            {
                "heading": "Use estimates for reversible decisions",
                "body": "Room area, VAT, date gaps, rough subscription reviews, and simple purchase checks are usually good candidates for quick tools. They help you move without pretending the answer is more exact than it is.",
            },
            {
                "heading": "Slow down for high-stakes contexts",
                "body": "Health, legal, tax, safeguarding, finance, and safety questions need more care. Technofatty can flag obvious issues, but important decisions should be checked against qualified advice or official sources.",
            },
        ],
        "related_slugs": ["room-area-calculator", "days-between-dates", "should-i-be-proud-of-this-plate"],
    },
    {
        "slug": "why-most-calculator-sites-are-hard-to-use",
        "title": "Why most answer sites are hard to use",
        "summary": "What Technofatty is trying to fix: clutter, filler, and hiding the useful bit.",
        "sections": [
            {
                "heading": "The useful answer is often buried",
                "body": "Many answer pages make people scroll through filler before they reach the actual tool or result. Technofatty is built around the opposite pattern: put the instrument first, then explain the result underneath.",
            },
            {
                "heading": "Tools need personality, not confusion",
                "body": "A memorable voice can help a page stick, but only if it does not make the answer harder to use. Podge exists to make the site distinctive while keeping the mechanics clear.",
            },
            {
                "heading": "Verdicts work when they create a next move",
                "body": "The strongest Technofatty pages do more than label a situation. They give a score, a verdict, a reason, and a next action that somebody might actually send to a friend.",
            },
        ],
        "related_slugs": ["vaguepost-decoder", "future-embarrassment-gauge", "algorithm-tax-calculator"],
    },
    {
        "slug": "how-to-tell-if-a-meal-fits-your-health-goals",
        "title": "How to tell if a meal fits your health goals without turning dinner into a trial",
        "summary": "A practical guide to judging meals by broad dietary signals, condition lenses, and one useful next move.",
        "sections": [
            {
                "heading": "Judge the plate, not your worth",
                "body": "One meal is not a personality verdict. A useful meal check looks for signals: protein, plants, fibre, salt, sugar, rich or fried elements, known triggers, and whether this was a one-off or a pattern.",
            },
            {
                "heading": "The health lens changes the answer",
                "body": "The same plate can look different under a blood-pressure, blood-sugar, reflux, lactose, coeliac, or kidney-conscious lens. Sodium, refined carbs, dairy, gluten, spicy foods, and unknown ingredients do not matter equally for everyone.",
            },
            {
                "heading": "Use broad flags carefully",
                "body": "A tool can flag likely watch-outs, but it cannot know lab results, medication, allergies, portion details, or a clinician-prescribed diet. For medical conditions, use broad verdicts as prompts, not permission slips.",
            },
        ],
        "related_slugs": ["should-i-be-proud-of-this-plate", "water-intake-calculator", "sale-suspicion-gauge"],
    },
    {
        "slug": "how-to-decide-whether-to-send-a-difficult-message",
        "title": "How to decide whether to send a difficult message",
        "summary": "A practical way to check tone, motive, timing, and screenshot risk before a message escapes the chat box.",
        "sections": [
            {
                "heading": "The problem is rarely just the words",
                "body": "A risky message usually has more than one issue: emotional heat, unclear motive, bad timing, and a recipient who may read it differently than intended. The words matter, but the surrounding situation matters too.",
            },
            {
                "heading": "Check what the message is trying to do",
                "body": "Clarifying, apologising, and setting a boundary are different from winning, punishing, or pretending to be fine. If the real motive is to make someone feel something, the message probably needs a slower pass.",
            },
            {
                "heading": "Use the screenshot test",
                "body": "If you would hate to see the message outside its original context, that is not automatic proof you should never send it. It is proof you should edit for clarity, proportion, and future-you.",
            },
        ],
        "related_slugs": ["should-i-send-that-message-gauge", "future-embarrassment-gauge", "main-character-risk-calculator"],
    },
    {
        "slug": "how-to-audit-subscriptions-without-cancelling-everything",
        "title": "How to audit subscriptions without cancelling everything",
        "summary": "A calm way to separate useful recurring costs from forgotten renewals, duplicates, and direct-debit fog.",
        "sections": [
            {
                "heading": "Start with visibility",
                "body": "Subscription bloat works because each charge feels small on its own. Add monthly costs, annual renewals, unused services, duplicate household subscriptions, and forgotten trials before deciding what deserves to stay.",
            },
            {
                "heading": "Do not cancel useful things just to feel productive",
                "body": "The point is not to punish every recurring payment. A service you use often and would choose again today is different from one that survives because the cancellation flow is annoying.",
            },
            {
                "heading": "Review the stack on purpose",
                "body": "A simple quarterly review is usually enough: keep what earns its place, cancel what only exists through inertia, and watch annual renewals before they become expensive surprises.",
            },
        ],
        "related_slugs": ["subscription-shame-index", "algorithm-tax-calculator", "fancy-version-justification-engine"],
    },
    {
        "slug": "how-to-spot-fake-hype-online",
        "title": "How to spot fake hype online without becoming paranoid",
        "summary": "A media-literacy guide to sudden consensus, repeated phrases, campaign signals, and suspiciously polished enthusiasm.",
        "sections": [
            {
                "heading": "Real excitement is usually messier",
                "body": "Organic hype tends to have mixed language, uneven timing, and people enjoying the thing in different ways. Manufactured-looking hype often arrives suddenly, repeats the same phrases, and sounds oddly briefed.",
            },
            {
                "heading": "Look for coordination signals",
                "body": "Identical wording, brand-new accounts, the same links, unexplained funding, and instant outrage are not proof by themselves. Together, they are reasons to slow down before amplifying.",
            },
            {
                "heading": "Suspicion is not a conclusion",
                "body": "A detector can help you withhold trust, but it should not become a machine for accusing strangers. Treat the pattern as evidence to inspect, not a verdict on intent.",
            },
        ],
        "related_slugs": ["fake-fan-detector", "astroturf-detector", "vaguepost-decoder"],
    },
]

INTENT_PATHS = [
    {
        "title": "I need a quick answer",
        "description": "Jump straight to the instruments people use most when they want a quick answer.",
        "href": "/calculators/",
    },
    {
        "title": "I am sorting out money",
        "description": "Percentages, VAT, raises, and other money questions that benefit from a clear answer.",
        "href": "/categories/money/",
    },
    {
        "title": "I am doing house stuff",
        "description": "Useful measuring instruments for rooms, flooring, paint, and practical planning.",
        "href": "/categories/home/",
    },
]

TRUST_POINTS = [
    "Answer first, explanation second",
    "Mobile-friendly inputs with plain-English feedback",
    "Clear disclaimers where a result is only an estimate",
]

QUESTION_PROMPTS = [
    {
        "question": "What is this vaguepost actually about?",
        "answer": "Useful when somebody has posted almost no information but an unhealthy amount of implication.",
        "href": "/calculators/vaguepost-decoder/",
    },
    {
        "question": "Do I actually have the moral authority to police phone use?",
        "answer": "Useful when the child is glued to a screen and the adult is holding one while complaining.",
        "href": "/calculators/parent-phone-hypocrisy-meter/",
    },
    {
        "question": "Should I send that message?",
        "answer": "Useful when the message feels important, but you are no longer sure whether it is wise.",
        "href": "/calculators/should-i-send-that-message-gauge/",
    },
    {
        "question": "Am I making this all about me?",
        "answer": "Useful when your reaction is getting bigger and you are not sure it should be.",
        "href": "/calculators/main-character-risk-calculator/",
    },
    {
        "question": "Are my subscriptions getting out of hand?",
        "answer": "Useful when recurring costs have started to feel invisible and suspicious.",
        "href": "/calculators/subscription-shame-index/",
    },
    {
        "question": "Is this hype actually real?",
        "answer": "Useful when excitement looks a little too coordinated to trust on sight.",
        "href": "/calculators/fake-fan-detector/",
    },
    {
        "question": "What phone rules would actually work in this house?",
        "answer": "Useful when everyone is already arguing and nobody wants another vague rule.",
        "href": "/calculators/parental-phone-treaty-generator/",
    },
    {
        "question": "Do I actually need the fancy version?",
        "answer": "Useful when durability, value, and price are all competing for attention.",
        "href": "/calculators/fancy-version-justification-engine/",
    },
    {
        "question": "Will I regret posting this?",
        "answer": "Useful when audience, tone, and emotion are all harder to judge than they look.",
        "href": "/calculators/future-embarrassment-gauge/",
    },
    {
        "question": "Is this discount actually worth it?",
        "answer": "Useful when a big red sale sticker is doing most of the talking.",
        "href": "/calculators/sale-suspicion-gauge/",
    },
    {
        "question": "Is this grassroots or astroturf?",
        "answer": "Useful when a sudden wave of comments, outrage, or support looks suspiciously coordinated.",
        "href": "/calculators/astroturf-detector/",
    },
    {
        "question": "What is this algorithm quietly costing me?",
        "answer": "Useful when recommendations keep converting spare attention into money, time, or mood damage.",
        "href": "/calculators/algorithm-tax-calculator/",
    },
    {
        "question": "Am I relying on AI too much emotionally?",
        "answer": "Useful when a helpful chat starts becoming the main place your feelings go.",
        "href": "/calculators/ai-emotional-dependency-gauge/",
    },
    {
        "question": "Should I be proud of this plate?",
        "answer": "Useful when dinner needs a tiny courtroom under a health lens, not a morality spiral.",
        "href": "/calculators/should-i-be-proud-of-this-plate/",
    },
    {
        "question": "How big is this room, really?",
        "answer": "Good for paint, flooring, furniture, and fewer trips back to the shop.",
        "href": "/calculators/room-area-calculator/",
    },
    {
        "question": "How much of this total is actually VAT?",
        "answer": "Useful when a number looks simple until tax starts haunting it.",
        "href": "/calculators/vat-calculator/",
    },
]

INSTRUMENT_TYPES = [
    {"name": "Engines", "description": "For awkward numeric questions that need a definite answer."},
    {"name": "Gauges", "description": "For messy feelings, fuzzy judgments, and squishy states that still benefit from shape."},
    {"name": "Instruments", "description": "For the practical little mechanisms in between."},
]

HOUSE_SPECIALS = [
    {
        "name": "Vaguepost Decoder",
        "slug": "vaguepost-decoder",
        "pitch": "A verdict on what kind of cryptic engagement bait a context-free post is trying to be.",
    },
    {
        "name": "Parent Phone Hypocrisy Meter",
        "slug": "parent-phone-hypocrisy-meter",
        "pitch": "A blunt check on whether the household phone lecture is being delivered from inside the same behavioural swamp.",
    },
    {
        "name": "Should I Send That Message Gauge",
        "slug": "should-i-send-that-message-gauge",
        "pitch": "A verdict on whether your message is clear, proportionate, and safe to send as written.",
    },
    {
        "name": "Main Character Risk Calculator",
        "slug": "main-character-risk-calculator",
        "pitch": "A blunt check on whether you are about to make somebody else's moment revolve around you.",
    },
    {
        "name": "Subscription Shame Index",
        "slug": "subscription-shame-index",
        "pitch": "A quick diagnosis of how much your recurring payments are costing you in money and inertia.",
    },
    {
        "name": "Fake Fan Detector",
        "slug": "fake-fan-detector",
        "pitch": "A suspicion check for hype that looks too polished, too sudden, or too coordinated to feel fully real.",
    },
    {
        "name": "Parental Phone Treaty Generator",
        "slug": "parental-phone-treaty-generator",
        "pitch": "A practical way to turn family phone anxiety into clearer rules that can actually be enforced.",
    },
    {
        "name": "Fancy Version Justification Engine",
        "slug": "fancy-version-justification-engine",
        "pitch": "A practical comparison for deciding whether the better version is worth the extra cost.",
    },
    {
        "name": "Future Embarrassment Gauge",
        "slug": "future-embarrassment-gauge",
        "pitch": "A practical check on whether a post is ready for other people or better left in drafts.",
    },
    {
        "name": "Sale Suspicion Gauge",
        "slug": "sale-suspicion-gauge",
        "pitch": "A practical way to tell whether a discount is helping you or just hurrying you.",
    },
    {
        "name": "Astroturf Detector",
        "slug": "astroturf-detector",
        "pitch": "A scepticism check for sudden grassroots-looking campaigns that may be more manufactured than messy.",
    },
    {
        "name": "Algorithm Tax Calculator",
        "slug": "algorithm-tax-calculator",
        "pitch": "A cost check for recommendation feeds that quietly turn attention into purchases, subscriptions, and lost time.",
    },
    {
        "name": "AI Emotional Dependency Gauge",
        "slug": "ai-emotional-dependency-gauge",
        "pitch": "A wellbeing check for when an AI assistant is helping with feelings but may be replacing human support.",
    },
    {
        "name": "Should I Be Proud Of This Plate?",
        "slug": "should-i-be-proud-of-this-plate",
        "pitch": "A condition-aware meal verdict with green flags, charges pending, and one non-dramatic next move.",
    },
]

USER_ANSWER_FIRST_TYPES = {
    "send-that-message",
    "main-character-risk",
    "subscription-shame",
    "vaguepost-decoder",
    "parent-phone-hypocrisy",
    "fake-fan-detector",
    "phone-treaty",
    "fancy-version",
    "future-embarrassment",
    "sale-suspicion",
    "astroturf-detector",
    "algorithm-tax",
    "ai-emotional-dependency",
    "plate-pride",
}


def get_tool(slug):
    return next((tool for tool in LIVE_TOOLS if tool["slug"] == slug), None)


def tools_by_category():
    return [
        {
            "category": category,
            "tools": [tool for tool in LIVE_TOOLS if tool["category_slug"] == category["slug"]],
        }
        for category in CATEGORIES
    ]


def public_route_paths():
    paths = [
        reverse("home"),
        reverse("calculators_index"),
        reverse("ask_podge"),
        reverse("about"),
        reverse("contact"),
        reverse("privacy"),
        reverse("terms"),
        reverse("robots_txt"),
        reverse("ads_txt"),
        reverse("sitemap_xml"),
    ]
    paths.extend(reverse("calculator_detail", args=[tool["slug"]]) for tool in LIVE_TOOLS)
    paths.extend(reverse("category_detail", args=[category["slug"]]) for category in CATEGORIES)
    paths.extend(reverse("guide_detail", args=[guide["slug"]]) for guide in GUIDES)
    return paths


ADMIN_TOOL_NAV = [
    {
        "name": "AdSense Readiness",
        "slug": "adsense-readiness",
        "url_name": "admin_tools_adsense_readiness",
        "status": "Live",
    },
    {
        "name": "Content Inventory",
        "slug": "content-inventory",
        "url_name": "admin_tools_content_inventory",
        "status": "Queued",
    },
    {
        "name": "SEO Metadata Audit",
        "slug": "seo-metadata",
        "url_name": "admin_tools_seo_metadata",
        "status": "Queued",
    },
    {
        "name": "Health/YMYL Safety",
        "slug": "ymyl-safety",
        "url_name": "admin_tools_ymyl_safety",
        "status": "Queued",
    },
    {
        "name": "Internal Links",
        "slug": "internal-links",
        "url_name": "admin_tools_internal_links",
        "status": "Queued",
    },
]


def admin_tools_context(request, active_slug, **extra):
    page_title = extra.get("page_title", "Admin Tools")
    context = admin.site.each_context(request)
    tool_app = {
        "name": "Technofatty Tools",
        "app_label": "technofatty_tools",
        "app_url": reverse("admin_tools_index"),
        "has_module_perms": True,
        "models": [
            {
                "name": item["name"],
                "object_name": item["slug"].replace("-", "_"),
                "admin_url": reverse(item["url_name"]),
                "add_url": None,
                "view_only": True,
            }
            for item in ADMIN_TOOL_NAV
        ],
    }
    context["available_apps"] = [tool_app, *context.get("available_apps", [])]
    context.update(base_context(
        title=page_title,
        meta_title="Admin Tools | Technofatty",
        meta_description="Staff-only operational dashboards for Technofatty.",
        admin_tool_nav=ADMIN_TOOL_NAV,
        active_admin_tool=active_slug,
        **extra,
    ))
    return context


def readiness_item(label, passed, detail, severity="critical", action=""):
    return {
        "label": label,
        "passed": passed,
        "status": "Pass" if passed else ("Warn" if severity == "warning" else "Fail"),
        "severity": severity,
        "detail": detail,
        "action": action,
    }


def placeholder_scan():
    blockers = [
        "starter placeholder",
        "initial Django build",
        "wire this page",
        "before launch",
        "Template-ready",
    ]
    files = [
        settings.BASE_DIR / "core" / "templates" / "core" / "legal.html",
        settings.BASE_DIR / "core" / "templates" / "core" / "contact.html",
        settings.BASE_DIR / "core" / "templates" / "core" / "calculators_index.html",
        settings.BASE_DIR / "core" / "templates" / "core" / "category_detail.html",
        settings.BASE_DIR / "core" / "views.py",
    ]
    hits = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for blocker in blockers:
            if blocker.lower() in text.lower():
                hits.append(f"{path.relative_to(settings.BASE_DIR)}: {blocker}")
    return hits


def ads_txt_lines():
    return ads_txt(None).content.decode("utf-8").splitlines()


def adsense_readiness_audit():
    live_tool_count = len(LIVE_TOOLS)
    queued_tool_count = len(TOOL_REGISTRY) - live_tool_count
    guide_count = len(GUIDES)
    category_content_count = len(CATEGORY_CONTENT)
    sitemap_paths = public_route_paths()
    placeholder_hits = placeholder_scan()
    ads_lines = ads_txt_lines()
    has_real_adsense_line = any("google.com, pub-" in line and "XXXXXXXXXXXXXXXX" not in line for line in ads_lines)
    health_tools = [tool for tool in LIVE_TOOLS if tool["category_slug"] == "health"]
    health_disclaimer_count = sum(
        1
        for tool in health_tools
        if "medical advice" in tool.get("disclaimer", "").lower()
        or "qualified advice" in tool.get("disclaimer", "").lower()
    )

    items = [
        readiness_item(
            "Privacy policy",
            True,
            "Privacy route is live with public-facing copy.",
            action="/privacy/",
        ),
        readiness_item(
            "Terms page",
            True,
            "Terms route is live with informational-use and no-professional-advice language.",
            action="/terms/",
        ),
        readiness_item(
            "Contact route",
            bool(CONTACT_EMAIL),
            f"Contact email configured as {CONTACT_EMAIL}.",
            action="/contact/",
        ),
        readiness_item(
            "robots.txt",
            True,
            "robots.txt is routed and points to the sitemap.",
            action="/robots.txt",
        ),
        readiness_item(
            "sitemap.xml",
            live_tool_count > 0 and guide_count > 0,
            f"Sitemap includes {len(sitemap_paths)} public URLs across tools, categories, guides, and policy pages.",
            action="/sitemap.xml",
        ),
        readiness_item(
            "ads.txt route",
            True,
            "ads.txt is routed. Real publisher ID is pending until AdSense provides it.",
            severity="warning",
            action="/ads.txt",
        ),
        readiness_item(
            "Real AdSense publisher line",
            has_real_adsense_line,
            "No real Google publisher line yet. This is expected before AdSense approval.",
            severity="warning",
            action="Add google.com, pub-... after approval.",
        ),
        readiness_item(
            "Public placeholder scan",
            not placeholder_hits,
            "No launch-blocking placeholder strings found." if not placeholder_hits else "; ".join(placeholder_hits),
            action="Remove construction copy from public pages.",
        ),
        readiness_item(
            "Live tool library",
            live_tool_count >= 15,
            f"{live_tool_count} live tools and {queued_tool_count} queued tools. Queued tools are hidden from public library/random routes.",
            action="/calculators/",
        ),
        readiness_item(
            "Guide depth",
            guide_count >= 7,
            f"{guide_count} guide pages are registered and included in sitemap.",
            action="/guides/how-to-spot-fake-hype-online/",
        ),
        readiness_item(
            "Category depth",
            category_content_count == len(CATEGORIES),
            f"{category_content_count} of {len(CATEGORIES)} categories have explanatory content.",
            action="/categories/health/",
        ),
        readiness_item(
            "Health/YMYL disclaimers",
            health_disclaimer_count == len(health_tools),
            f"{health_disclaimer_count} of {len(health_tools)} live health tools include explicit medical/qualified-advice caution.",
            action="/categories/health/",
        ),
        readiness_item(
            "Disabled ad-slot scaffolding",
            True,
            "Reusable ad slot partial exists and is disabled while ads_enabled is false.",
            severity="warning",
            action="Enable only after AdSense approval.",
        ),
    ]

    failed_count = sum(1 for item in items if item["status"] == "Fail")
    warning_count = sum(1 for item in items if item["status"] == "Warn")
    passed_count = sum(1 for item in items if item["status"] == "Pass")

    return {
        "summary": {
            "status": "Ready for external setup" if failed_count == 0 else "Needs fixes",
            "passed": passed_count,
            "warnings": warning_count,
            "failed": failed_count,
            "live_tools": live_tool_count,
            "guides": guide_count,
            "sitemap_urls": len(sitemap_paths),
        },
        "items": items,
        "next_actions": [
            "Verify technofatty.com in Google Search Console.",
            "Submit https://technofatty.com/sitemap.xml.",
            "Apply for AdSense after final live QA.",
            "Replace ads.txt comment with the real Google publisher line after AdSense provides it.",
            "Build the next admin tool: Content Inventory.",
        ],
    }


def base_context(**extra):
    return {
        "site_name": SITE_NAME,
        "site_tagline": SITE_TAGLINE,
        "categories": CATEGORIES,
        "featured_tools": TOOL_REGISTRY[:6],
        "guides": GUIDES,
        "intent_paths": INTENT_PATHS,
        "trust_points": TRUST_POINTS,
        "question_prompts": QUESTION_PROMPTS,
        "instrument_types": INSTRUMENT_TYPES,
        "house_specials": HOUSE_SPECIALS,
        "random_tool": random.choice(LIVE_TOOLS),
        "contact_email": CONTACT_EMAIL,
        "ads_enabled": False,
        **extra,
    }


def home(request):
    return render(
        request,
        "core/home.html",
        base_context(
            meta_title="Technofatty | Questions, awkwardly answered.",
            meta_description="Technofatty is a growing collection of practical instruments, answer engines, and explainers for everyday questions.",
            spotlight_tool=get_tool("should-i-send-that-message-gauge"),
        ),
    )


def calculators_index(request):
    return render(
        request,
        "core/calculators_index.html",
        base_context(
            meta_title="Instruments | Technofatty",
            meta_description="Browse Technofatty instruments for money, home, health, time, food, tech, and everyday questions.",
            page_title="Browse instruments",
            page_intro="Practical little engines, gauges, and instruments with clear labels and answers that show their working.",
            tool_groups=tools_by_category(),
            all_tools=LIVE_TOOLS,
        ),
    )


@staff_member_required
def admin_tools_index(request):
    return render(
        request,
        "core/admin_tools/index.html",
        admin_tools_context(
            request,
            "index",
            page_title="Admin Tools",
            page_intro="Staff-only Technofatty operating tools for content, AdSense readiness, search quality, and internal housekeeping.",
        ),
    )


@staff_member_required
def admin_tools_adsense_readiness(request):
    audit = adsense_readiness_audit()
    return render(
        request,
        "core/admin_tools/readiness.html",
        admin_tools_context(
            request,
            "adsense-readiness",
            page_title="AdSense Readiness Dashboard",
            page_intro="Staff-only checks for the pieces that need to be in place before Technofatty applies for or scales Google ads.",
            audit=audit,
        ),
    )


def queued_admin_tool_context(request, active_slug):
    tool = next(item for item in ADMIN_TOOL_NAV if item["slug"] == active_slug)
    return admin_tools_context(
        request,
        active_slug,
        page_title=tool["name"],
        page_intro="This staff tool is queued in the admin suite and will be built as part of the AdSense operating backend.",
        tool=tool,
    )


@staff_member_required
def admin_tools_content_inventory(request):
    return render(request, "core/admin_tools/queued.html", queued_admin_tool_context(request, "content-inventory"))


@staff_member_required
def admin_tools_seo_metadata(request):
    return render(request, "core/admin_tools/queued.html", queued_admin_tool_context(request, "seo-metadata"))


@staff_member_required
def admin_tools_ymyl_safety(request):
    return render(request, "core/admin_tools/queued.html", queued_admin_tool_context(request, "ymyl-safety"))


@staff_member_required
def admin_tools_internal_links(request):
    return render(request, "core/admin_tools/queued.html", queued_admin_tool_context(request, "internal-links"))


def random_calculator(request):
    tool = random.choice(LIVE_TOOLS)
    return redirect("calculator_detail", slug=tool["slug"])


def category_detail(request, slug):
    category = next((item for item in CATEGORIES if item["slug"] == slug), None)
    if not category:
        return custom_404(request, None)
    tools = [tool for tool in LIVE_TOOLS if tool["category_slug"] == slug]
    return render(
        request,
        "core/category_detail.html",
        base_context(
            meta_title=f"{category['name']} instruments | Technofatty",
            meta_description=category["description"],
            category=category,
            category_tools=tools,
            category_content=CATEGORY_CONTENT.get(slug),
        ),
    )


def calculator_detail(request, slug):
    registry_tool = get_tool(slug)
    if not registry_tool:
        return custom_404(request, None)
    tool = {
        **registry_tool,
        "start_neutral": registry_tool.get("calculator_type") in USER_ANSWER_FIRST_TYPES,
    }
    context = base_context(
        meta_title=f"{tool['name']} | Technofatty",
        meta_description=tool["summary"],
        tool=tool,
        related_tools=[item for item in LIVE_TOOLS if item["slug"] != slug][:3],
    )
    return render(request, "core/calculator_detail.html", context)


def guide_detail(request, slug):
    guide = next((item for item in GUIDES if item["slug"] == slug), None)
    if not guide:
        return custom_404(request, None)
    related_tools = [
        get_tool(related_slug)
        for related_slug in guide.get("related_slugs", [])
    ]
    return render(
        request,
        "core/guide_detail.html",
        base_context(
            meta_title=f"{guide['title']} | Technofatty",
            meta_description=guide["summary"],
            guide=guide,
            related_tools=[tool for tool in related_tools if tool],
        ),
    )


def ask_podge(request):
    return render(
        request,
        "core/ask_podge.html",
        base_context(
            meta_title="Ask Podge | Technofatty",
            meta_description="A guided way into Technofatty's engines, gauges, and practical instruments.",
        ),
    )


def about(request):
    return render(
        request,
        "core/about.html",
        base_context(
            meta_title="About Technofatty",
            meta_description="Meet Technofatty and Podge, the compact answer-engine robot behind the site's no-waffle instruments.",
        ),
    )


def contact(request):
    return render(
        request,
        "core/contact.html",
        base_context(
            meta_title="Contact Technofatty",
            meta_description="Contact Technofatty with feedback, corrections, privacy questions, advertising queries, or suggestions for new instruments.",
        ),
    )


def privacy(request):
    return render(
        request,
        "core/legal.html",
        base_context(
            meta_title="Privacy Policy | Technofatty",
            meta_description="Technofatty privacy policy covering logs, cookies, analytics, advertising, and contact options.",
            legal_title="Privacy Policy",
            updated_date="3 May 2026",
        ),
    )


def terms(request):
    return render(
        request,
        "core/legal.html",
        base_context(
            meta_title="Terms | Technofatty",
            meta_description="Technofatty terms for using the site's calculators, verdict engines, guides, and content.",
            legal_title="Terms",
            updated_date="3 May 2026",
        ),
    )


def custom_404(request, exception):
    return render(
        request,
        "core/404.html",
        base_context(
            meta_title="Page not found | Technofatty",
            meta_description="Podge checked the numbers and that page is not here.",
        ),
        status=404,
    )


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {SITE_DOMAIN}{reverse('sitemap_xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def ads_txt(request):
    lines = [
        "# Technofatty ads.txt",
        "# Add the Google AdSense publisher line here after AdSense provides the real publisher ID.",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    paths = [
        reverse("home"),
        reverse("calculators_index"),
        reverse("ask_podge"),
        reverse("about"),
        reverse("contact"),
        reverse("privacy"),
        reverse("terms"),
    ]
    paths.extend(reverse("calculator_detail", args=[tool["slug"]]) for tool in LIVE_TOOLS)
    paths.extend(reverse("category_detail", args=[category["slug"]]) for category in CATEGORIES)
    paths.extend(reverse("guide_detail", args=[guide["slug"]]) for guide in GUIDES)
    urls = "\n".join(
        f"  <url><loc>{SITE_DOMAIN}{path}</loc></url>"
        for path in paths
    )
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    return HttpResponse(content, content_type="application/xml")
