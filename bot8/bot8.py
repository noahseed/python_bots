import os
import openai
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv


load = load_dotenv()

# Chargez les clés d'API à partir des variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN')

# Configurez OpenAI avec votre clé d'API
openai.api_key = OPENAI_API_KEY

# Définissez un gestionnaire de commandes pour répondre à la commande /gpt3
def gpt3_handler(update, context):
    # Obtenez le texte du message de l'utilisateur
    user_input = update.message.text

    # Appelez l'API OpenAI pour générer une réponse
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=50
    )

    # Envoyez la réponse générée par GPT-3 à l'utilisateur sur Telegram
    update.message.reply_text(response.choices[0].text)

# Configurez le bot Telegram avec votre token d'accès
updater = Updater(TELEGRAM_ACCESS_TOKEN, use_context=True)

# Attachez le gestionnaire de commandes au bot Telegram
updater.dispatcher.add_handler(CommandHandler("gpt3", gpt3_handler))

# Démarrez le bot Telegram
updater.start_polling()
updater.idle()