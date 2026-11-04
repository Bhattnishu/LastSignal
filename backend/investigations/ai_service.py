import time

from google import genai
from django.conf import settings


def generate_investigation_analysis(item, timeline):
    """Generate an investigation analysis using Gemini with retries."""

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    prompt = f"""
    You are LastSignal, an AI assistant helping users find lost items.

    LOST ITEM:
    Name: {item.item_name}
    Category: {item.category}
    Brand: {item.brand or 'Unknown'}
    Color: {item.color or 'Unknown'}
    Description: {item.description}
    Last location: {item.location}, {item.city}

    TIMELINE:
    {timeline}

    Give a SHORT investigation report using exactly these sections:

    1. POSSIBLE PLACES TO CHECK
    Suggest 3-4 specific places.
    Give one short reason for each place (maximum 20 words).

    2. MISSING INFORMATION
    Mention at most 2 useful details that could improve the investigation.

    RULES:
    - Maximum 130 words.
    - Use simple language.
    - Avoid repeating item details.
    - Never claim to know the exact location.
    - Do not assume theft or accuse anyone.
    - Suggestions must be realistic and relevant.
    - Do not add greetings, introductions, next steps, or conclusions.
    """

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            if response.text:
                return response.text

            raise ValueError("Gemini returned an empty response.")

        except Exception as error:
            error_message = str(error)

            temporary_errors = (
                "429", "500", "502", "503", "504"
            )

            is_temporary = any(
                code in error_message
                for code in temporary_errors
            )

            if not is_temporary or attempt == max_attempts - 1:
                raise

            wait_time = 2 * (attempt + 1)

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds "
                f"(attempt {attempt + 1}/{max_attempts})."
            )

            time.sleep(wait_time)


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