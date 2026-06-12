import re
import unicodedata


def generate_slug(text):
    """Generate a URL-friendly slug from text.

    Examples:
        'Kashmir Valley' -> 'kashmir-valley'
        'Goa (Beach)' -> 'goa-beach'
        'Dubai & Abu Dhabi' -> 'dubai-abu-dhabi'
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Lowercase
    text = text.lower().strip()

    # Replace non-alphanumeric with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Remove leading/trailing hyphens and collapse multiple hyphens
    text = re.sub(r'-+', '-', text).strip('-')

    return text
