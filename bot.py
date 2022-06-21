import threading
import discord
from dotenv import dotenv_values
import telebot
import signal

config = dotenv_values(".env")
DISCORD_TOKEN = config["DISCORD"]
TELEGRAM_TOKEN = config["TELEGRAM"]

discordBot = discord.Client()
telegramBot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)

@discordBot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discordBot))

@discordBot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    messaggio = "Messaggio da " + username + ":\n" + user_message 

    inviaMessaggio(chatId, messaggio)

    if message.author == discordBot.user:
        return

    if message.channel.name == 'musica':
        print('messaggio da musica')

@telegramBot.message_handler(commands=['help', 'start'])
def savla_id(message):
    global chatId
    chatId = message.chat.id

def inviaMessaggio(chat_id, messaggio):
    telegramBot.send_message(chat_id, text=messaggio)

threadTelegram = threading.Thread(target=telegramBot.infinity_polling, args=[])

threadTelegram.start()

discordBot.run(DISCORD_TOKEN)