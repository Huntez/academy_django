import telebot
from product_dp.models import Product, Category, Users_Cart
from connections import token
from datetime import datetime

bot = telebot.TeleBot(token=token)

category_list = [cat.Name for cat in Category.objects.all()]
@bot.message_handler(commands=['start','Categories', 'Cart'])
def commands_handler(message):
    if message.text == '/start':
        keyboard = telebot.types.ReplyKeyboardMarkup(
            resize_keyboard=True)

        cbutton = telebot.types.KeyboardButton('/Categories')
        scbutton = telebot.types.KeyboardButton('/Cart')
        
        keyboard.add(cbutton, scbutton)

        bot.send_message(message.chat.id, 
            'Commands : ', reply_markup=keyboard)

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
        
        product_cost = dict()
        for i in Product.objects.all():
            product_cost[i.Name] = i.Cost

        user_cart_result = dict()
        for i in user_cart:
            if i not in user_cart_result:
                user_cart_result[i] = user_cart.count(i)

        user_cart_cost = 0
        for res, cost in zip(user_cart_result, product_cost):
            user_cart_cost += product_cost[res] * user_cart_result[res]

        bot.send_message(message.chat.id,
            '\n'.join(f'{key} - {value}'
            for key, value in user_cart_result.items()) + 
            f'\nOrder cost - {user_cart_cost}')

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
        bot.send_message(call.message.chat.id, 'Product added to /Cart')

bot.infinity_polling()
