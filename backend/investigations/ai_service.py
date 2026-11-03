
from google import genai
from django.conf import settings


def generate_investigation_analysis(item, timeline):
    """Generate an investigation analysis using Gemini."""

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    prompt = f"""
    You are an assistant helping people investigate lost items.

    LOST ITEM DETAILS:
    Item: {item.item_name}
    Category: {item.category}
    Brand: {item.brand or 'Not provided'}
    Color: {item.color or 'Not provided'}
    Description: {item.description}
    Last known location: {item.location}, {item.city}

    JOURNEY TIMELINE:
    {timeline}

    TASK:
    1. Analyse the lost item details and timeline.
    2. Suggest 3-5 plausible places where the user could check.
    3. Explain why each place is worth checking.
    4. Give practical next steps.
    5. Mention any missing information that could help.

    IMPORTANT:
    - Never claim to know the exact location.
    - Do not assume theft or accuse anyone.
    - Clearly describe suggestions as possibilities, not facts.
    - Keep the response simple and helpful.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text


def generate_fallback_analysis(item, timeline):
    """Generate basic investigation suggestions without an AI API."""

    category = (item.category or "").lower()
    item_name = item.item_name or "your item"

    suggestions = []

    if any(word in category for word in ["electronic", "mobile", "phone", "laptop"]):
        suggestions.extend([
            (
                "Charging and usage areas",
                "Check near charging points, desks, and places where you commonly use the device."
            ),
            (
                "Transport and seating areas",
                "Retrace your journey and check vehicle seats, public transport, and waiting areas."
            ),
        ])

    elif any(word in category for word in ["wallet", "bag", "accessory"]):
        suggestions.extend([
            (
                "Personal storage areas",
                "Check pockets, bags, drawers, and places where you usually keep personal belongings."
            ),
            (
                "Recent stopping points",
                "Contact shops, reception desks, or other places you visited recently."
            ),
        ])

    elif any(word in category for word in ["document", "book", "stationery"]):
        suggestions.extend([
            (
                "Study and work areas",
                "Check desks, classrooms, libraries, and places where you last used the item."
            ),
            (
                "Storage and carrying areas",
                "Check folders, backpacks, shelves, and other places where you store documents."
            ),
        ])

    else:
        suggestions.extend([
            (
                "Last known location",
                "Carefully search the area where you last remember having the item."
            ),
            (
                "Recently visited places",
                "Contact the shops, buildings, or other locations you visited after last seeing the item."
            ),
        ])

    timeline_places = [
        entry.get("place")
        for entry in timeline
        if entry.get("place")
    ]

    if timeline_places:
        suggestions.append((
            "Retrace your recorded journey",
            "Revisit these recorded locations in order: "
            + ", ".join(timeline_places)
            + ". Check each place carefully."
        ))

    suggestions.append((
        "Ask for more information",
        "Contact the people responsible for places you visited and ask whether the item was handed in."
    ))

    result = [
        "SMART INVESTIGATION SUGGESTIONS",
        "",
        f"We could not reach the AI service. Here are some basic suggestions for finding {item_name}.",
        "",
    ]

    for number, (title, reason) in enumerate(suggestions[:5], start=1):
        result.append(f"{number}. {title}")
        result.append(reason)
        result.append("")

    result.extend([
        "NEXT STEPS",
        "- Confirm the last time and place you remember having the item.",
        "- Check the suggested locations systematically.",
        "- Add any missing journey details to improve your investigation.",
        "",
        "Note: These are general suggestions, not confirmed locations."
    ])

    return "\n".join(result)
