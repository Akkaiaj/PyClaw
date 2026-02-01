import re

class ModerationPlugin:
    def __init__(self):
        self.blocked_patterns = [
            r'\b(spam|scam|phishing)\b',
            r'(http|https)://bit\.ly',
        ]
    
    async def check_message(self, text: str) -> tuple:
        text_lower = text.lower()
        for pattern in self.blocked_patterns:
            if re.search(pattern, text_lower):
                return True, f"Matched pattern: {pattern}"
        if len(text) > 20 and sum(1 for c in text if c.isupper()) / len(text) > 0.7:
            return True, "Excessive caps"
        if re.search(r'(.)\1{10,}', text):
            return True, "Spam pattern detected"
        return False, None
