"""
OpenAI GPT provider implementation.

Sends chat messages to the OpenAI API and returns the response with
token usage data for cost tracking.
"""


def send_message(api_key: str, model: str, messages: list, system: str = None) -> dict:
    """
    Send a chat message to OpenAI and return the response.

    Args:
        api_key: Decrypted OpenAI API key.
        model: OpenAI model identifier (e.g. 'gpt-4o').
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
