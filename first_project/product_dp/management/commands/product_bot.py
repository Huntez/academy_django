import telebot
from product_dp.models import Product, Category, Users_Cart
from connections import token
from datetime import datetime

bot = telebot.TeleBot(token=token)

category_list = [cat.Name for cat in Category.objects.all()]

@bot.message_handler(commands=['Categories', 'Cart'])
def commands_handler(message):
    if message.text == '/Categories':
        keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True)

        for obj in Category.objects.all():
            button = telebot.types.KeyboardButton(obj.Name)
            keyboard.add(button)

        bot.send_message(message.chat.id, 
        'Categories : ', reply_markup=keyboard)

    if message.text == '/Cart':
        user_cart = [str(i.product)
        for i in Users_Cart.objects.filter(user_chat_id = 
                message.chat.id)]

        # kvadelupa = [i.Cost for i in 
        # Product.objects.filter(Name = )]

        user_cart_result = []
        for i in user_cart:
            if i not in user_cart_result:
                user_cart_result.append(i)
                user_cart_result.append(
                        str(user_cart.count(i)))

        bot.send_message(message.chat.id, 
                ' - '.join(user_cart_result))

# Need rework 
@bot.message_handler(content_types=['text'])
def category_button_handler(message):
    if message.text in category_list:
        objects = Product.objects.filter(
        Category__Name = message.text)

        keyboard = telebot.types.InlineKeyboardMarkup()
        
        for obj in objects:
            button = telebot.types.InlineKeyboardButton(obj.Name,
                callback_data=obj.Name)
            keyboard.add(button)

        bot.send_message(message.chat.id, 'products',
            reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data:
        Users_Cart.objects.get_or_create(
            user_chat_id = call.message.chat.id,
            product = Product.objects.get(Name=call.data),
            date = datetime.now()
        )

bot.infinity_polling()
