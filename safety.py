
import re

# List of crisis-related keywords
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "self harm", "end my life",
    "hurt myself", "cut myself", "can't go on", "want to die"
]

# Offensive word filters
OFFENSIVE_KEYWORDS = [
    "fuck", "shit", "bitch", "bastard", "asshole", "cunt"
]


def is_safe(text):
    """Check if text is safe to respond to."""
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower()

    # Check for crisis keywords
    for word in CRISIS_KEYWORDS:
        if word in text_lower:
            return False

    # Check for offensive keywords
    for word in OFFENSIVE_KEYWORDS:
        if word in text_lower:
            return False

    return True


def crisis_detected(text):
    """Return True if input contains crisis keywords."""
    if not text:
        return False

    text_lower = text.lower()

    for word in CRISIS_KEYWORDS:
        if word in text_lower:
            return True
    return False


def sanitize_text(text):
    """Replace offensive words with ****"""
    if not text:
        return text

    text_lower = text.lower()
    cleaned = text

    for word in OFFENSIVE_KEYWORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        cleaned = pattern.sub("****", cleaned)

    return cleaned
