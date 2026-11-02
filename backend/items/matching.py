from difflib import SequenceMatcher

def text_similarity(value1, value2):
    """Compare two text values and return a score from 0 to 1."""

    if not value1 or not value2:
        return 0

    value1 = value1.lower().strip()
    value2 = value2.lower().strip()

    return SequenceMatcher(None, value1, value2).ratio()


def description_similarity(description1, description2):
    """Compare important words in two descriptions."""

    if not description1 or not description2:
        return 0

    stop_words = {
        'the', 'a', 'an', 'is', 'was', 'and', 'or',
        'with', 'near', 'at', 'in', 'on', 'my', 'it',
        'this', 'that', 'to', 'of'
    }

    words1 = {
        word.lower().strip('.,!?')
        for word in description1.split()
        if word.lower().strip('.,!?') not in stop_words
    }

    words2 = {
        word.lower().strip('.,!?')
        for word in description2.split()
        if word.lower().strip('.,!?') not in stop_words
    }

    if not words1 or not words2:
        return 0

    common_words = words1.intersection(words2)
    total_words = words1.union(words2)

    return len(common_words) / len(total_words)


def calculate_match_score(lost_report, found_report):

    score = 0
    reasons = []

    # 1. Category: 20 points
    if lost_report.category == found_report.category:
        score += 20
        reasons.append("Same item category")

    # 2. Item name: 25 points
    name_score = text_similarity(
        lost_report.item_name,
        found_report.item_name
    )

    points = round(name_score * 25)
    score += points

    if points >= 15:
        reasons.append("Similar item names")

    # 3. Brand: 15 points
    if lost_report.brand and found_report.brand:
        brand_score = text_similarity(
            lost_report.brand,
            found_report.brand
        )

        points = round(brand_score * 15)
        score += points

        if points >= 10:
            reasons.append("Similar brand")

    # 4. Colour: 10 points
    if lost_report.color and found_report.color:
        color_score = text_similarity(
            lost_report.color,
            found_report.color
        )

        points = round(color_score * 10)
        score += points

        if points >= 7:
            reasons.append("Similar colour")

    # 5. City: 10 points
    if lost_report.city.lower().strip() == found_report.city.lower().strip():
        score += 10
        reasons.append("Same city")

    # 6. Location: 10 points
    location_score = text_similarity(
        lost_report.location,
        found_report.location
    )

    points = round(location_score * 10)
    score += points

    if points >= 6:
        reasons.append("Similar locations")

    # 7. Description: 10 points
    description_score = description_similarity(
        lost_report.description,
        found_report.description
    )

    points = round(description_score * 10)
    score += points

    if points >= 3:
        reasons.append("Similar description details")

    return {
        'score': min(score, 100),
        'reasons': reasons
    }
