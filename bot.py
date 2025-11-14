"""
Telegram bot for the personal finance agent.
"""
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent import FinanceAgent
from database import DatabaseManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database and agent
db = DatabaseManager()
agent = FinanceAgent(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    db=db
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = f"""¡Hola {user.first_name}! 👋

Soy tu asistente personal de finanzas. Puedo ayudarte a:

💰 Registrar gastos e ingresos
📊 Consultar tu saldo
📈 Analizar tus gastos por período
🏷️ Ver en qué categorías gastas más
📅 Comparar gastos entre meses

Solo escríbeme de forma natural. Por ejemplo:
- "Gasté 50 pesos en comida"
- "Recibí mi salario de 5000"
- "Cuánto dinero tengo?"
- "Cuánto gasté esta semana?"
- "En qué he gastado más este mes?"

¡Empecemos! 🚀"""
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """🤖 Comandos disponibles:

/start - Iniciar el bot
/help - Mostrar esta ayuda
/balance - Ver tu saldo actual

También puedes escribirme de forma natural y te entenderé. Por ejemplo:

📝 Registrar gastos:
- "Gasté 50 en comida"
- "Compré ropa por 200 pesos"

💵 Registrar ingresos:
- "Recibí mi salario de 5000"
- "Gané 100 por freelance"

❓ Consultas:
- "Cuánto dinero tengo?"
- "Cuánto gasté esta semana?"
- "En qué he gastado más?"
- "Compara mis gastos del mes pasado con este mes"
"""
    
    await update.message.reply_text(help_text)


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current balance."""
    user_id = update.effective_user.id
    response = agent.process_message(user_id, "cuál es mi saldo actual?")
    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Process message with agent
    response = agent.process_message(user_id, user_message)
    
    # Send response
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    print(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "Lo siento, ocurrió un error al procesar tu mensaje. Por favor intenta de nuevo."
        )


def main():
    """Start the bot."""
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN no está configurado en el archivo .env")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
