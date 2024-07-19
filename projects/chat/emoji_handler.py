
# emoji_handler.py

def get_emoji_list():
    """
    Returns a list of available emojis.
    
    Returns:
        list: A list of dictionaries containing emoji information.
    """
    # This is a simplified list of emojis. In a real application, this list would be more extensive.
    return [
        {"shortcode": ":smile:", "unicode": "😊"},
        {"shortcode": ":laugh:", "unicode": "😂"},
        {"shortcode": ":wink:", "unicode": "😉"},
        {"shortcode": ":heart:", "unicode": "❤️"},
        {"shortcode": ":thumbsup:", "unicode": "👍"},
        {"shortcode": ":star:", "unicode": "⭐"},
    ]

def replace_emoji_shortcodes(message: str) -> str:
    """
    Replaces emoji shortcodes with Unicode characters in the given message.
    
    Args:
        message (str): The input message containing emoji shortcodes.
    
    Returns:
        str: The message with emoji shortcodes replaced by Unicode characters.
    """
    emoji_list = get_emoji_list()
    for emoji in emoji_list:
        message = message.replace(emoji["shortcode"], emoji["unicode"])
    return message

# Example usage (can be removed in production)
if __name__ == "__main__":
    # Print available emojis
    print("Available emojis:")
    for emoji in get_emoji_list():
        print(f"{emoji['shortcode']} - {emoji['unicode']}")
    
    # Test emoji replacement
    test_message = "Hello! :smile: How are you? :thumbsup:"
    replaced_message = replace_emoji_shortcodes(test_message)
    print(f"\nOriginal message: {test_message}")
    print(f"Message with emojis: {replaced_message}")
