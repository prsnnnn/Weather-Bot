from pyowm.owm import OWM  # We import the package with which we know the weather
import telebot  #Import the bot package via CMD input "pip install pytelegrambotapi"
import time
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM('YOUR_TOKEN', config_dict)#API key from openweathermap.org
bot = telebot.TeleBot('1762581649:AAFk0ZJjIsNPPvbOacmGWHv6gPGCuAq83b0')# We receive the token via BotFather in the telegram chat by the commands. / newbot the name of my APITelegramBot 
#owm = OWM('YOUR_OWM_API', config_dict)
#bot = telebot.TeleBot('YOUR_TELEGRAM_API')

# When a text message is written to the bot, this function is called
@bot.message_handler(content_types=['text'])
def send_message(message):
    """Send the message to user with the weather"""
    # We respond separately to messages / start and / help
    if message.text.lower() == "/start" or message.text.lower() == "/help":
        name=message.from_user.first_name
        bot.send_message(message.from_user.id, f"Hello, {name}. You can check the weather here. Just write the name of the city." + "\n")
    else:
        # I try to force the code to pass if the observation function does not find the city and outputs an error, then a branch to except occurs
        try:
        # The user enters the name of the city into the chat, after which we pass it to the function
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(message.text)
            weather = observation.weather
            temp = round(weather.temperature("celsius")["temp"])  # Assigning the temperature value from the table to the variable
            #temp = round(temp)
            status = weather.detailed_status
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), temp, "C", status)
            # We form and display the answer
            answer = "In the town " + message.text.title() + " now " + status + "." + "\n"
            answer += f"Temperature is about: {temp} С" + "\n\n"
            if temp < -10:
                answer += "It's very-very cold, dress like a tank!"
            elif temp < 10:
                answer += "It's cold, dress warmer."
            elif temp > 25:
                answer += "It's heat!."
            else:
                answer += "On the street like the rules !!!"
            bot.send_message(message.chat.id, answer)  # Reply with a message
        except Exception:
            answer = "City not found, try entering name again.\n"
            #print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), 'Error')
            bot.send_message(message.chat.id, answer)  # Reply with a message

# Launching the bot
bot.polling(none_stop=True)
