Here's your complete Telegram group protection bot:

## **bot.py**

```python
import os
import logging
from telegram import Update, ChatMember
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatMemberStatus, ChatType

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('TELEGRAM_BOT_TOKEN environment variable not set')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        '👋 Welcome to the Group Protection Bot!\n\n'
        'I help administrators manage and protect your group.\n'
        'Use /help to see available commands.'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        '📋 **Available Commands:**\n\n'
        '/start - Show welcome message\n'
        '/help - Show this help message\n'
        '/id - Show your user ID and chat ID\n\n'
        '🛡️ **Moderation Commands** (Admin only):\n'
        '/ban - Ban a member (reply to their message)\n'
        '/unban - Unban a member (reply to their message)\n'
        '/kick - Remove a member (reply to their message)\n\n'
        '⚠️ Only group administrators can use moderation commands.\n'
        'The bot cannot ban or kick administrators.'
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send user and chat IDs when /id is issued."""
    user = update.effective_user
    chat = update.effective_chat
    
    id_text = (
        f'👤 **Your Info:**\n'
        f'User ID: `{user.id}`\n'
        f'Username: @{user.username if user.username else "N/A"}\n\n'
        f'💬 **Chat Info:**\n'
        f'Chat ID: `{chat.id}`\n'
        f'Chat Name: {chat.title or chat.first_name or "N/A"}'
    )
    await update.message.reply_text(id_text, parse_mode='Markdown')


async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Check if the user is an administrator in the current group."""
    if update.effective_chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        await update.message.reply_text('⚠️ This command can only be used in groups.')
        return False
    
    user_id = update.effective_user.id
    chat = update.effective_chat
    
    try:
        member = await context.bot.get_chat_member(chat.id, user_id)
        is_admin = member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
        
        if not is_admin:
            await update.message.reply_text('❌ Only administrators can use this command.')
        
        return is_admin
    except Exception as e:
        logger.error(f'Error checking admin status: {e}')
        await update.message.reply_text('⚠️ Error checking permissions.')
        return False


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ban a user by replying to their message."""
    # Check if user is admin
    if not await is_admin(update, context):
        return
    
    # Check if replying to a message
    if not update.message.reply_to_message:
        await update.message.reply_text('⚠️ Please reply to a message to ban a user.')
        return
    
    target_user = update.message.reply_to_message.from_user
    target_id = target_user.id
    chat = update.effective_chat
    
    # Prevent banning administrators
    try:
        target_member = await context.bot.get_chat_member(chat.id, target_id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            await update.message.reply_text('❌ Cannot ban administrators.')
            return
    except Exception as e:
        logger.error(f'Error checking target member status: {e}')
        await update.message.reply_text('⚠️ Error checking target user status.')
        return
    
    # Ban the user
    try:
        await context.bot.ban_chat_member(chat.id, target_id)
        await update.message.reply_text(
            f'✅ User {target_user.first_name} (`{target_id}`) has been banned.'
        )
        logger.info(f'User {target_id} banned from {chat.id}')
    except Exception as e:
        logger.error(f'Error banning user: {e}')
        await update.message.reply_text(f'⚠️ Error banning user: {str(e)}')


async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unban a user by replying to their message."""
    # Check if user is admin
    if not await is_admin(update, context):
        return
    
    # Check if replying to a message
    if not update.message.reply_to_message:
        await update.message.reply_text('⚠️ Please reply to a message from a banned user to unban them.')
        return
    
    target_user = update.message.reply_to_message.from_user
    target_id = target_user.id
    chat = update.effective_chat
    
    # Unban the user
    try:
        await context.bot.unban_chat_member(chat.id, target_id)
        await update.message.reply_text(
            f'✅ User {target_user.first_name} (`{target_id}`) has been unbanned.'
        )
        logger.info(f'User {target_id} unbanned from {chat.id}')
    except Exception as e:
        logger.error(f'Error unbanning user: {e}')
        await update.message.reply_text(f'⚠️ Error unbanning user: {str(e)}')


async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove a user from the group by replying to their message."""
    # Check if user is admin
    if not await is_admin(update, context):
        return
    
    # Check if replying to a message
    if not update.message.reply_to_message:
        await update.message.reply_text('⚠️ Please reply to a message to kick a user.')
        return
    
    target_user = update.message.reply_to_message.from_user
    target_id = target_user.id
    chat = update.effective_chat
    
    # Prevent kicking administrators
    try:
        target_member = await context.bot.get_chat_member(chat.id, target_id)
        if target_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            await update.message.reply_text('❌ Cannot kick administrators.')
            return
    except Exception as e:
        logger.error(f'Error checking target member status: {e}')
        await update.message.reply_text('⚠️ Error checking target user status.')
        return
    
    # Kick the user (ban temporarily, then unban to remove without permanent ban)
    try:
        await context.bot.ban_chat_member(chat.id, target_id)
        await context.bot.unban_chat_member(chat.id, target_id)
        await update.message.reply_text(
            f'✅ User {target_user.first_name} (`{target_id}`) has been removed.'
        )
        logger.info(f'User {target_id} kicked from {chat.id}')
    except Exception as e:
        logger.error(f'Error kicking user: {e}')
        await update.message.reply_text(f'⚠️ Error kicking user: {str(e)}')


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('id', get_id))
    application.add_handler(CommandHandler('ban', ban_user))
    application.add_handler(CommandHandler('unban', unban_user))
    application.add_handler(CommandHandler('kick', kick_user))
    
    # Run the bot
    logger.info('Bot starting...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
```

## **requirements.txt**

```
python-telegram-bot==20.7
```

---

**What to do next:**

1. **Copy both files** into your `youneshafeur555-oss/telegram-bot` repository
2. **Push to main branch**: Railway will auto-detect the change and redeploy
3. **Verify TELEGRAM_BOT_TOKEN is set**: Go to your service variables in Railway and confirm the bot token environment variable is present
4. **Test the bot**: Invite it to a group and run `/help`

**Key features:**
✅ `/start`, `/help`, `/id` — available to all users  
✅ `/ban`, `/unban`, `/kick` — admin-only with admin protection  
✅ Error handling and logging  
✅ Uses `TELEGRAM_BOT_TOKEN` from environment  
✅ Starts with `python bot.py`

The bot is now safe and production-ready!