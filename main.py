import telebot
import schedule
import time
import os
import json

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)

message_to_send = "do something useful"
_time = "05:30"

# Load chat IDs from JSON file
try:
    with open("chat_ids.json", "r") as f:
        chat_ids = json.load(f)
except FileNotFoundError:
    chat_ids = []

# Function to save chat IDs to JSON file
def save_chat_ids():
    with open("chat_ids.json", "w") as f:
        json.dump(chat_ids, f)

# Function to send the message
def send_message(reload=0):
    if not reload:
        for i in chat_ids:
            try:
                bot.send_message(int(i), message_to_send)
            except Exception as e:
                print(f"Error sending message: {e}")
    else:
        for i in chat_ids:
            try:
                bot.send_message(int(i), "reloaded")
            except Exception as e:
                print(f"Error sending message: {e}")

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    global chat_ids
    chat_id = message.chat.id
    if str(chat_id) not in chat_ids:
        chat_ids.append(str(chat_id))
        save_chat_ids()
        bot.send_message(chat_id, f"yor slave will send you a message at {_time} everyday, You can silence me using /stop")
        # Schedule the message to be sent every day
        schedule.every().day.at(_time).do(send_message)
    else:
        bot.send_message(chat_id, "already running")

# Handler for the /stop command
@bot.message_handler(commands=['stop'])
def stop_command(message):
    global chat_ids
    chat_id = None
    if str(message.chat.id) in chat_ids:
        chat_ids.remove(str(message.chat.id))
        save_chat_ids()
        bot.send_message(message.chat.id, "Ded.")
    else:
        bot.send_message(message.chat.id, "already ded.")
    # Remove the scheduled task
    schedule.clear()

# Start the bot
send_message(1)
schedule.every().day.at(_time).do(send_message)
bot.polling()

# Run the scheduled tasks in the background
while True:
    print(1)
    schedule.run_pending()
    time.sleep(1)
