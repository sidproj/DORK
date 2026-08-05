from datetime import datetime

def runtime():

    now = datetime.now()

    return f"""
Current Date: {now:%A, %d %B %Y}

Current Time: {now:%I:%M %p}

The runtime information above is authoritative.

Use it whenever the user asks about dates or time.
""".strip()