"""
Google Gemini provider implementation.

Sends chat messages to the Google Generative AI API and returns the response
with token usage data for cost tracking.
"""


def send_message(api_key: str, model: str, messages: list, system: str = None) -> dict:
    """
    Send a chat message to Google Gemini and return the response.

    Args:
        api_key: Decrypted Google API key.
        model: Google model identifier (e.g. 'gemini-1.5-flash').
        messages: List of message dicts with 'role' and 'content' keys.
        system: Optional system prompt string.

    Returns:
        dict with keys:
            content (str): The assistant's response text.
            input_tokens (int): Input tokens consumed.
            output_tokens (int): Output tokens produced.
            error (str | None): Error message if the call failed.

    Note:
        Implementation is proprietary and not included in this public version.
    """
    raise NotImplementedError("Proprietary implementation")
