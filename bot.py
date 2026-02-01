import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters, 
    ContextTypes
)
from telegram.constants import ChatAction, ParseMode
from anthropic import Anthropic

from config import *
from database import Database
from agents import get_agent, list_agents, AGENTS
from plugins.plugin_manager import PluginManager
from plugins.weather import WeatherPlugin
from plugins.news import NewsPlugin
from plugins.search import SearchPlugin
from plugins.games import GamesPlugin
from plugins.moltbook import MoltbookPlugin
from plugins.moderation import ModerationPlugin
from utils.keyboards import create_agent_keyboard, create_trivia_keyboard, create_settings_keyboard

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db = Database()
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
plugin_manager = PluginManager()

if ENABLE_WEATHER:
    plugin_manager.register_plugin('weather', WeatherPlugin)
if ENABLE_NEWS:
    plugin_manager.register_plugin('news', NewsPlugin)
if ENABLE_SEARCH:
    plugin_manager.register_plugin('search', SearchPlugin)
if ENABLE_GAMES:
    plugin_manager.register_plugin('games', GamesPlugin)
if ENABLE_MOLTBOOK:
    plugin_manager.register_plugin('moltbook', MoltbookPlugin)
if ENABLE_MODERATION:
    plugin_manager.register_plugin('moderation', ModerationPlugin)

last_responses = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    active_agent = await db.get_active_agent(user_id)
    agent = get_agent(active_agent)
    
    welcome_text = f"""🤖 **Welcome to PyClaw Supercharged!**

I'm an advanced AI assistant with memory, multiple personalities, and powerful plugins.

**Active Agent:** {agent.get_display_name()}

**🎭 Agents:**
{list_agents()}

**🧠 Knowledge Base:**
/remember <topic> <info> - Store a fact
/recall <topic> - Retrieve stored info
/forget <topic> - Delete a fact
/knowledge - List all stored topics

**🔌 Plugins:**
{'/weather <city> - Get weather' if ENABLE_WEATHER else ''}
{'/news [topic] - Latest headlines' if ENABLE_NEWS else ''}
{'/search <query> - Web search' if ENABLE_SEARCH else ''}
{'/trivia - Play trivia game' if ENABLE_GAMES else ''}
{'/riddle - Get a riddle' if ENABLE_GAMES else ''}
{'/math - Math challenge' if ENABLE_GAMES else ''}

**📱 Moltbook:**
{'/post - Post last response' if ENABLE_MOLTBOOK else ''}
{'/auto_post <on/off> - Toggle auto-posting' if ENABLE_MOLTBOOK else ''}
{'/feed - View Moltbook feed' if ENABLE_MOLTBOOK else ''}

**⚙️ Settings:**
/settings - Configure bot
/clear - Clear conversation history
/help - Show this message

Just send me a message to start chatting!
"""
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    auto_post = await db.get_auto_post(user_id)
    active_agent = await db.get_active_agent(user_id)
    agent = get_agent(active_agent)
    
    settings_text = f"""⚙️ **Bot Settings**

**Active Agent:** {agent.get_display_name()}
**Auto-post to Moltbook:** {'🟢 ON' if auto_post else '🔴 OFF'}

Use the buttons below to configure:
"""
    keyboard = create_settings_keyboard(auto_post)
    await update.message.reply_text(settings_text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

async def switch_agent_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = create_agent_keyboard()
    await update.message.reply_text("🎭 **Select an Agent:**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

async def friendly_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await db.set_active_agent(user_id, 'friendly')
    await update.message.reply_text("😊 Switched to Friendly Claude!")

async def expert_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await db.set_active_agent(user_id, 'expert')
    await update.message.reply_text("🎓 Switched to Expert Claude!")

async def researcher_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await db.set_active_agent(user_id, 'researcher')
    await update.message.reply_text("🔬 Switched to Research Assistant!")

async def creative_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await db.set_active_agent(user_id, 'creative')
    await update.message.reply_text("🎨 Switched to Creative Claude!")

async def remember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /remember <topic> <information>\nExample: /remember birthday My birthday is June 15th")
        return
    topic = context.args[0]
    content = ' '.join(context.args[1:])
    await db.store_knowledge(user_id, topic, content)
    await update.message.reply_text(f"✅ Stored **{topic}**: {content}", parse_mode=ParseMode.MARKDOWN)

async def recall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("❌ Usage: /recall <topic>\nExample: /recall birthday")
        return
    topic = context.args[0]
    content = await db.recall_knowledge(user_id, topic)
    if content:
        await update.message.reply_text(f"💡 **{topic}**: {content}", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"❌ No information stored for '{topic}'")

async def forget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("❌ Usage: /forget <topic>\nExample: /forget birthday")
        return
    topic = context.args[0]
    deleted = await db.forget_knowledge(user_id, topic)
    if deleted:
        await update.message.reply_text(f"🗑️ Deleted **{topic}**", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(f"❌ No information stored for '{topic}'")

async def list_knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    topics = await db.list_knowledge(user_id)
    if topics:
        topics_text = '\n'.join([f"• {topic}" for topic in topics])
        await update.message.reply_text(f"📚 **Your Knowledge Base:**\n\n{topics_text}", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("📚 Your knowledge base is empty. Use /remember to add facts!")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_WEATHER:
        await update.message.reply_text("❌ Weather plugin is disabled")
        return
    if not context.args:
        await update.message.reply_text("❌ Usage: /weather <city>\nExample: /weather London")
        return
    city = ' '.join(context.args)
    weather_plugin = plugin_manager.get_plugin('weather')
    result = await weather_plugin.get_weather(city)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_NEWS:
        await update.message.reply_text("❌ News plugin is disabled")
        return
    topic = ' '.join(context.args) if context.args else None
    news_plugin = plugin_manager.get_plugin('news')
    result = await news_plugin.get_news(topic)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_SEARCH:
        await update.message.reply_text("❌ Search plugin is disabled")
        return
    if not context.args:
        await update.message.reply_text("❌ Usage: /search <query>\nExample: /search Python tutorials")
        return
    await update.message.chat.send_action(action=ChatAction.TYPING)
    query = ' '.join(context.args)
    search_plugin = plugin_manager.get_plugin('search')
    result = await search_plugin.search(query)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

async def trivia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_GAMES:
        await update.message.reply_text("❌ Games plugin is disabled")
        return
    user_id = str(update.effective_user.id)
    games_plugin = plugin_manager.get_plugin('games')
    text, options = await games_plugin.start_trivia(user_id)
    keyboard = create_trivia_keyboard(options)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)

async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_GAMES:
        await update.message.reply_text("❌ Games plugin is disabled")
        return
    user_id = str(update.effective_user.id)
    games_plugin = plugin_manager.get_plugin('games')
    riddle = await games_plugin.get_riddle(user_id)
    await update.message.reply_text(riddle, parse_mode=ParseMode.MARKDOWN)

async def math_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_GAMES:
        await update.message.reply_text("❌ Games plugin is disabled")
        return
    games_plugin = plugin_manager.get_plugin('games')
    question, answer = await games_plugin.math_challenge()
    user_id = str(update.effective_user.id)
    context.user_data['math_answer'] = answer
    await update.message.reply_text(question, parse_mode=ParseMode.MARKDOWN)

async def post_to_moltbook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_MOLTBOOK:
        await update.message.reply_text("❌ Moltbook plugin is disabled")
        return
    user_id = str(update.effective_user.id)
    if user_id not in last_responses:
        await update.message.reply_text("❌ No recent response to post!")
        return
    moltbook_plugin = plugin_manager.get_plugin('moltbook')
    success, message = await moltbook_plugin.post_message(last_responses[user_id], user_id)
    await update.message.reply_text(message)

async def auto_post_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_MOLTBOOK:
        await update.message.reply_text("❌ Moltbook plugin is disabled")
        return
    user_id = str(update.effective_user.id)
    if not context.args or context.args[0].lower() not in ['on', 'off']:
        await update.message.reply_text("❌ Usage: /auto_post <on|off>")
        return
    enabled = context.args[0].lower() == 'on'
    await db.set_auto_post(user_id, enabled)
    status = "enabled" if enabled else "disabled"
    await update.message.reply_text(f"✅ Auto-post {status}!")

async def feed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ENABLE_MOLTBOOK:
        await update.message.reply_text("❌ Moltbook plugin is disabled")
        return
    await update.message.chat.send_action(action=ChatAction.TYPING)
    moltbook_plugin = plugin_manager.get_plugin('moltbook')
    feed = await moltbook_plugin.get_feed()
    await update.message.reply_text(feed, parse_mode=ParseMode.MARKDOWN)

async def clear_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    await db.clear_conversation(user_id)
    await update.message.reply_text("🧹 Conversation history cleared!")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    data = query.data
    
    if data.startswith('agent_'):
        agent_name = data.replace('agent_', '')
        await db.set_active_agent(user_id, agent_name)
        agent = get_agent(agent_name)
        await query.edit_message_text(f"✅ Switched to {agent.get_display_name()}!")
    elif data.startswith('trivia_'):
        answer = data.replace('trivia_', '')
        games_plugin = plugin_manager.get_plugin('games')
        result = await games_plugin.check_trivia_answer(user_id, answer)
        await query.edit_message_text(result, parse_mode=ParseMode.MARKDOWN)
    elif data == 'toggle_autopost':
        current = await db.get_auto_post(user_id)
        await db.set_auto_post(user_id, not current)
        keyboard = create_settings_keyboard(not current)
        await query.edit_message_reply_markup(reply_markup=keyboard)
    elif data == 'show_agents':
        keyboard = create_agent_keyboard()
        await query.edit_message_text("🎭 **Select an Agent:**", reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    elif data == 'clear_memory':
        await db.clear_conversation(user_id)
        await query.edit_message_text("🧹 Conversation history cleared!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_message = update.message.text
    
    if ENABLE_MODERATION:
        moderation = plugin_manager.get_plugin('moderation')
        is_flagged, reason = await moderation.check_message(user_message)
        if is_flagged:
            await db.log_moderation(user_id, user_message, reason)
            await update.message.reply_text("⚠️ Your message was flagged by moderation filters.")
            return
    
    if ENABLE_GAMES:
        games_plugin = plugin_manager.get_plugin('games')
        riddle_result = await games_plugin.check_riddle_answer(user_id, user_message)
        if riddle_result:
            await update.message.reply_text(riddle_result, parse_mode=ParseMode.MARKDOWN)
            return
    
    if 'math_answer' in context.user_data:
        correct = context.user_data['math_answer']
        if user_message.strip() == correct:
            await update.message.reply_text(f"✅ Correct! The answer is **{correct}**!", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(f"❌ Wrong! The correct answer was **{correct}**", parse_mode=ParseMode.MARKDOWN)
        del context.user_data['math_answer']
        return
    
    await update.message.chat.send_action(action=ChatAction.TYPING)
    
    active_agent_name = await db.get_active_agent(user_id)
    agent = get_agent(active_agent_name)
    
    await db.add_message(user_id, 'user', user_message, active_agent_name)
    history = await db.get_conversation_history(user_id, MAX_CONVERSATION_HISTORY)
    
    knowledge_topics = await db.list_knowledge(user_id)
    knowledge_context = []
    for topic in knowledge_topics[:5]:
        content = await db.recall_knowledge(user_id, topic)
        if content:
            knowledge_context.append(f"{topic}: {content}")
    
    messages = [{'role': msg['role'], 'content': msg['content']} for msg in history]
    
    if knowledge_context:
        knowledge_text = "\n".join(knowledge_context)
        system_prompt = f"{agent.get_system_prompt()}\n\nUser's stored knowledge:\n{knowledge_text}"
    else:
        system_prompt = agent.get_system_prompt()
    
    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        
        ai_response = response.content[0].text
        await db.add_message(user_id, 'assistant', ai_response, active_agent_name)
        last_responses[user_id] = ai_response
        await update.message.reply_text(ai_response, parse_mode=ParseMode.MARKDOWN)
        
        if ENABLE_MOLTBOOK:
            auto_post = await db.get_auto_post(user_id)
            if auto_post:
                moltbook_plugin = plugin_manager.get_plugin('moltbook')
                await moltbook_plugin.post_message(ai_response, user_id)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def post_init(application: Application):
    await db.init_db()
    logger.info("✅ Database initialized")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("clear", clear_conversation))
    
    application.add_handler(CommandHandler("agents", switch_agent_menu))
    application.add_handler(CommandHandler("friendly", friendly_agent))
    application.add_handler(CommandHandler("expert", expert_agent))
    application.add_handler(CommandHandler("researcher", researcher_agent))
    application.add_handler(CommandHandler("creative", creative_agent))
    
    application.add_handler(CommandHandler("remember", remember))
    application.add_handler(CommandHandler("recall", recall))
    application.add_handler(CommandHandler("forget", forget))
    application.add_handler(CommandHandler("knowledge", list_knowledge))
    
    if ENABLE_WEATHER:
        application.add_handler(CommandHandler("weather", weather_command))
    if ENABLE_NEWS:
        application.add_handler(CommandHandler("news", news_command))
    if ENABLE_SEARCH:
        application.add_handler(CommandHandler("search", search_command))
    if ENABLE_GAMES:
        application.add_handler(CommandHandler("trivia", trivia_command))
        application.add_handler(CommandHandler("riddle", riddle_command))
        application.add_handler(CommandHandler("math", math_command))
    if ENABLE_MOLTBOOK:
        application.add_handler(CommandHandler("post", post_to_moltbook))
        application.add_handler(CommandHandler("auto_post", auto_post_toggle))
        application.add_handler(CommandHandler("feed", feed_command))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("🚀 PyClaw Supercharged starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
