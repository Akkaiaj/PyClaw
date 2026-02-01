from telegram.constants import ParseMode

def format_code(code: str, language: str = "") -> str:
    return f"```{language}\n{code}\n```"

def format_bold(text: str) -> str:
    return f"**{text}**"

def format_italic(text: str) -> str:
    return f"_{text}_"

def escape_markdown(text: str) -> str:
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text
