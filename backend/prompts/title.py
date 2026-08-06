TITLE_SYSTEM_PROMPT = """
Task:
Generate a concise title for the conversation.

Rules:
- Ignore greetings.
- Ignore acknowledgements.
- Focus on the user's first meaningful request.
- Maximum 6 words.
- If no meaningful request exists, output exactly: NO_TITLE.
- Output only the title or NO_TITLE.
""".strip()