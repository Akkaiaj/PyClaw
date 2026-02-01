from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_agent_keyboard():
    keyboard = [
        [InlineKeyboardButton("😊 Friendly", callback_data="agent_friendly"),
         InlineKeyboardButton("🎓 Expert", callback_data="agent_expert")],
        [InlineKeyboardButton("🔬 Researcher", callback_data="agent_researcher"),
         InlineKeyboardButton("🎨 Creative", callback_data="agent_creative")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_trivia_keyboard(options: list):
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"trivia_{opt}")] for opt in options]
    return InlineKeyboardMarkup(keyboard)

def create_settings_keyboard(auto_post: bool):
    auto_post_text = "🟢 Auto-post ON" if auto_post else "🔴 Auto-post OFF"
    keyboard = [
        [InlineKeyboardButton(auto_post_text, callback_data="toggle_autopost")],
        [InlineKeyboardButton("🔄 Change Agent", callback_data="show_agents")],
        [InlineKeyboardButton("🗑️ Clear Memory", callback_data="clear_memory")]
    ]
    return InlineKeyboardMarkup(keyboard)
