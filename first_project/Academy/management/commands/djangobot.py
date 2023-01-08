import telebot
from Academy.models import Curator
from connections import token

bot = telebot.TeleBot(token=token)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Curators':
        object_list = [f'{i.Name} : {i.Surname}'
        for i in Curator.objects.all()]
        bot.send_message(message.chat.id, ' , '.join(object_list))

bot.infinity_polling()
