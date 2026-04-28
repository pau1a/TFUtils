from django.shortcuts import render


SITE_NAME = "Technofatty"
SITE_TAGLINE = "Crunching numbers. Cutting fluff."

CATEGORIES = [
    {"name": "Money", "slug": "money", "description": "Everyday finance and salary tools that get to the point."},
    {"name": "Home", "slug": "home", "description": "Quick calculators for rooms, paint, flooring, and practical jobs."},
    {"name": "Health", "slug": "health", "description": "Simple estimate tools with clear caveats where they matter."},
    {"name": "Time", "slug": "time", "description": "Dates, ages, countdowns, and workday questions without spreadsheet pain."},
    {"name": "Food", "slug": "food", "description": "Kitchen-friendly conversions, scaling, and timing helpers."},
    {"name": "Tech", "slug": "tech", "description": "Conversions, speed checks, and lightweight practical utility tools."},
]

TOOLS = [
    {
        "name": "Percentage Change Calculator",
        "slug": "percentage-change-calculator",
        "category": "Money",
        "category_slug": "money",
        "summary": "Work out the percentage increase or decrease between two values.",
        "eyebrow": "Live demo",
    },
    {
        "name": "VAT Calculator",
        "slug": "vat-calculator",
        "category": "Money",
        "category_slug": "money",
        "summary": "Add or remove VAT from a price with clear totals.",
        "eyebrow": "Coming next",
    },
    {
        "name": "Room Area Calculator",
        "slug": "room-area-calculator",
        "category": "Home",
        "category_slug": "home",
        "summary": "Measure floor area fast before you buy paint, flooring, or furniture.",
        "eyebrow": "Template-ready",
    },
    {
        "name": "Days Between Dates",
        "slug": "days-between-dates",
        "category": "Time",
        "category_slug": "time",
        "summary": "See the number of days between two dates without calendar wrangling.",
        "eyebrow": "Template-ready",
    },
    {
        "name": "Recipe Scaler",
        "slug": "recipe-scaler",
        "category": "Food",
        "category_slug": "food",
        "summary": "Scale ingredients up or down without mental arithmetic.",
        "eyebrow": "Template-ready",
    },
    {
        "name": "Water Intake Calculator",
        "slug": "water-intake-calculator",
        "category": "Health",
        "category_slug": "health",
        "summary": "Get a quick hydration estimate with a sensible disclaimer.",
        "eyebrow": "Template-ready",
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
        "title": "When a quick calculator is good enough, and when it is not",
        "summary": "A short guide to estimates, disclaimers, and using calculators responsibly.",
    },
    {
        "slug": "why-most-calculator-sites-are-hard-to-use",
        "title": "Why most calculator sites are hard to use",
        "summary": "What Technofatty is trying to fix: clutter, filler, and hiding the answer.",
    },
]


def base_context(**extra):
    return {
        "site_name": SITE_NAME,
        "site_tagline": SITE_TAGLINE,
        "categories": CATEGORIES,
        "featured_tools": TOOLS[:6],
        "guides": GUIDES,
        **extra,
    }


def home(request):
    return render(
        request,
        "core/home.html",
        base_context(
            meta_title="Technofatty | Useful calculators without the waffle",
            meta_description="Technofatty is a growing collection of fast calculators, explainers, and practical tools for everyday decisions.",
        ),
    )


def calculators_index(request):
    return render(
        request,
        "core/calculators_index.html",
        base_context(
            meta_title="Calculators | Technofatty",
            meta_description="Browse practical calculators for money, home, health, time, food, tech, and everyday questions.",
            page_title="Browse calculators",
            page_intro="Practical tools, clear labels, and answers that show their working.",
        ),
    )


def category_detail(request, slug):
    category = next((item for item in CATEGORIES if item["slug"] == slug), None)
    if not category:
        return custom_404(request, None)
    tools = [tool for tool in TOOLS if tool["category_slug"] == slug]
    return render(
        request,
        "core/category_detail.html",
        base_context(
            meta_title=f"{category['name']} calculators | Technofatty",
            meta_description=category["description"],
            category=category,
            category_tools=tools,
        ),
    )


def calculator_detail(request, slug):
    tool = next((item for item in TOOLS if item["slug"] == slug), None)
    if not tool:
        return custom_404(request, None)
    context = base_context(
        meta_title=f"{tool['name']} | Technofatty",
        meta_description=tool["summary"],
        tool=tool,
        related_tools=[item for item in TOOLS if item["slug"] != slug][:3],
    )
    if slug == "percentage-change-calculator":
        context.update(
            {
                "formula": "Percentage change = ((new value - old value) / old value) x 100",
                "worked_example": "If the old value is 80 and the new value is 100, the change is 20. Divide 20 by 80, then multiply by 100 to get 25%.",
                "disclaimer": "This calculator gives a general estimate only. It is not financial, legal, medical, or professional advice.",
            }
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


def about(request):
    return render(
        request,
        "core/about.html",
        base_context(
            meta_title="About Technofatty",
            meta_description="Meet Technofatty and Podge, the compact calculator robot behind the site's no-waffle utility tools.",
        ),
    )


def contact(request):
    return render(
        request,
        "core/contact.html",
        base_context(
            meta_title="Contact Technofatty",
            meta_description="Suggest a calculator, share feedback, or ask Technofatty for a tool idea.",
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

# Create your views here.
