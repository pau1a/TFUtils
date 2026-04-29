import random

from django.shortcuts import redirect, render


SITE_NAME = "Technofatty"
SITE_TAGLINE = "Questions, awkwardly answered."

CATEGORIES = [
    {"name": "Money", "slug": "money", "description": "Everyday money instruments for pay, tax, comparisons, and practical trade-offs."},
    {"name": "Home", "slug": "home", "description": "Room, surface, and household measuring instruments for practical jobs."},
    {"name": "Health", "slug": "health", "description": "Estimate-driven instruments with clear caveats where they matter."},
    {"name": "Time", "slug": "time", "description": "Dates, ages, countdowns, and workday questions without spreadsheet pain."},
    {"name": "Food", "slug": "food", "description": "Kitchen-friendly conversions, scaling, and timing helpers."},
    {"name": "Tech", "slug": "tech", "description": "Conversions, speed checks, and other compact instruments for technical odd jobs."},
    {"name": "Life", "slug": "life", "description": "Guidance instruments for timing, trade-offs, and other less tidy real-life questions."},
]

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
        "eyebrow": "Template-ready",
        "calculator_type": "placeholder",
    },
    {
        "name": "Water Intake Gauge",
        "slug": "water-intake-calculator",
        "category": "Health",
        "category_slug": "health",
        "summary": "Get a quick hydration estimate with a sensible disclaimer.",
        "eyebrow": "Template-ready",
        "calculator_type": "placeholder",
    },
    {
        "name": "Should I Send That Message Gauge",
        "slug": "should-i-send-that-message-gauge",
        "category": "Life",
        "category_slug": "life",
        "summary": "Weigh urgency, timing, and emotional charge before sending a difficult message.",
        "eyebrow": "Featured",
        "calculator_type": "send-that-message",
        "microcopy": "Use this to weigh urgency, clarity, timing, and emotional charge before you send.",
        "formula": "Message impulse score = urgency + clarity - emotional charge - lateness penalty",
        "worked_example": "A message with high urgency, good clarity, low emotional charge, and a sensible sending time scores much better than a blurry midnight spiral.",
        "disclaimer": "This is a subjective guidance gauge, not relationship, legal, medical, or professional advice.",
        "result_labels": ["Impulse score", "Urgency", "Emotional charge"],
        "faq": [
            {
                "question": "Is this meant as serious life advice?",
                "answer": "No. It is a framing instrument for awkward moments, not a substitute for judgment, context, or consent.",
            },
            {
                "question": "What makes a message risky here?",
                "answer": "Low clarity, low urgency, high emotional charge, and sending it very late at night all push the gauge toward waiting.",
            },
        ],
        "defaults": {
            "headline": "Draft it. Sleep on it.",
            "detail": "The current combination looks more impulsive than urgent, so it may be better to wait and review it later.",
            "badge": "Hold fire",
            "mood": "Podge recommends waiting.",
            "signals": ["2/10", "3/10", "8/10"],
            "explainer": "This gauge is not trying to make the choice for you. It simply makes urgency, clarity, lateness, and emotional heat visible at the same time.",
            "summary": "The current balance suggests waiting, rewriting, or reviewing it in a calmer moment.",
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
]

GUIDES = [
    {
        "slug": "how-to-calculate-percentage-change",
        "title": "How to calculate percentage change without overthinking it",
        "summary": "A plain-English explainer with the formula, a worked example, and when the result can mislead.",
    },
    {
        "slug": "when-a-quick-calculator-is-good-enough",
        "title": "When a quick instrument is good enough, and when it is not",
        "summary": "A short guide to estimates, disclaimers, and using Technofatty responsibly.",
    },
    {
        "slug": "why-most-calculator-sites-are-hard-to-use",
        "title": "Why most answer sites are hard to use",
        "summary": "What Technofatty is trying to fix: clutter, filler, and hiding the useful bit.",
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
        "question": "Should I send that message?",
        "answer": "Useful when timing, urgency, and emotional charge all matter.",
        "href": "/calculators/should-i-send-that-message-gauge/",
    },
    {
        "question": "Do I actually need the fancy version?",
        "answer": "Useful when durability, value, and price are all competing for attention.",
        "href": "/calculators/fancy-version-justification-engine/",
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
        "name": "Should I Send That Message Gauge",
        "slug": "should-i-send-that-message-gauge",
        "pitch": "A practical gauge for judging timing, urgency, and emotional charge before you hit send.",
    },
    {
        "name": "Fancy Version Justification Engine",
        "slug": "fancy-version-justification-engine",
        "pitch": "A practical comparison for deciding whether the better version is worth the extra cost.",
    },
]


def get_tool(slug):
    return next((tool for tool in TOOL_REGISTRY if tool["slug"] == slug), None)


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
        "random_tool": random.choice(TOOL_REGISTRY),
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
        ),
    )


def random_calculator(request):
    tool = random.choice(TOOL_REGISTRY)
    return redirect("calculator_detail", slug=tool["slug"])


def category_detail(request, slug):
    category = next((item for item in CATEGORIES if item["slug"] == slug), None)
    if not category:
        return custom_404(request, None)
    tools = [tool for tool in TOOL_REGISTRY if tool["category_slug"] == slug]
    return render(
        request,
        "core/category_detail.html",
        base_context(
            meta_title=f"{category['name']} instruments | Technofatty",
            meta_description=category["description"],
            category=category,
            category_tools=tools,
        ),
    )


def calculator_detail(request, slug):
    tool = get_tool(slug)
    if not tool:
        return custom_404(request, None)
    context = base_context(
        meta_title=f"{tool['name']} | Technofatty",
        meta_description=tool["summary"],
        tool=tool,
        related_tools=[item for item in TOOL_REGISTRY if item["slug"] != slug][:3],
    )
    return render(request, "core/calculator_detail.html", context)


def guide_detail(request, slug):
    guide = next((item for item in GUIDES if item["slug"] == slug), None)
    if not guide:
        return custom_404(request, None)
    return render(
        request,
        "core/guide_detail.html",
        base_context(
            meta_title=f"{guide['title']} | Technofatty",
            meta_description=guide["summary"],
            guide=guide,
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
            meta_description="Suggest an instrument, share feedback, or ask Technofatty for a useful new idea.",
        ),
    )


def privacy(request):
    return render(
        request,
        "core/legal.html",
        base_context(
            meta_title="Privacy Policy | Technofatty",
            meta_description="Technofatty privacy policy placeholder for the initial Django build.",
            legal_title="Privacy Policy",
        ),
    )


def terms(request):
    return render(
        request,
        "core/legal.html",
        base_context(
            meta_title="Terms | Technofatty",
            meta_description="Technofatty terms placeholder for the initial Django build.",
            legal_title="Terms",
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
