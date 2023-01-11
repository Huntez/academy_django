from decimal import Decimal, DecimalException
import telebot
from product_dp.models import Product, Category, Users_Cart, Wallet
from connections import token
from datetime import datetime

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def commands_handler(message):
    if not Wallet.objects.filter(user_chat_id = message.chat.id):
        Wallet.objects.get_or_create(
            user_chat_id = message.chat.id,
        )

    func_list = ['/categories', '/cart', '/payorder',
                 '/checkwallet', '/addtowallet', 
                 '/clearusercart']

    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True)

    for i in func_list:
        button = telebot.types.KeyboardButton(i)
        keyboard.add(button)

    bot.send_message(message.chat.id, 
        'Commands : ', reply_markup=keyboard)

@bot.message_handler(commands=['checkwallet'])
def check_wallet(message):

    bot.send_message(message.chat.id, Wallet.objects.filter(
    user_chat_id = message.chat.id)[0].balance)

@bot.message_handler(commands=['addtowallet'])
def walletsum(message):
    bot.send_message(message.chat.id, 
                     "Enter wallet sum to add : ")
    
    bot.register_next_step_handler(message, walletadding)

def walletadding(message):
    try:
        user = Wallet.objects.filter(
            user_chat_id = message.chat.id)[0]
        user.balance += Decimal(message.text)
        user.save()
    except DecimalException:
        bot.send_message(message.chat.id, 'Non Digit!')
    else:
        bot.send_message(message.chat.id, "Summ added to wallet!")


@bot.message_handler(commands=['categories'])
def categories_button(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True)

    for obj in Category.objects.all():
        button = telebot.types.KeyboardButton(obj.Name)
        keyboard.add(button)
    
    button = telebot.types.KeyboardButton('/start')
    keyboard.add(button)

    bot.send_message(message.chat.id, 
    'Categories : ', reply_markup=keyboard)


@bot.message_handler(func=lambda m: True
    if Category.objects.filter(Name = m.text) else False)
def category_button_handler(message):
    objects = Product.objects.filter(
    Category__Name = message.text)

    keyboard = telebot.types.InlineKeyboardMarkup()
    for obj in objects:
        button = telebot.types.InlineKeyboardButton(obj.Name,
            callback_data=obj.Name)
        keyboard.add(button)

    bot.send_message(message.chat.id, 'products',
        reply_markup=keyboard)


@bot.message_handler(commands=['cart', 'payorder'])
def cart_and_payment(message):
    user_cart = [str(i.product)
    for i in Users_Cart.objects.filter(user_chat_id = 
            message.chat.id)]

    if user_cart:
        product_cost = dict()
        for i in Product.objects.all():
            product_cost[i.Name] = i.Cost

        user_cart_result = dict()
        for i in user_cart:
            if i not in user_cart_result:
                user_cart_result[i] = user_cart.count(i)

        user_cart_cost = 0
        for res in user_cart_result:
            user_cart_cost += product_cost[res] * user_cart_result[res]

        if message.text == '/cart':
            bot.send_message(message.chat.id,
                '\n'.join(f'{key} - {value}'
                for key, value in user_cart_result.items()) + 
                f'\nOrder cost - {user_cart_cost}')

        if message.text == '/payorder':
            user = Wallet.objects.filter(
                    user_chat_id = message.chat.id)[0]
            if user.balance < user_cart_cost:
                bot.send_message(message.chat.id, "Not Enough money!")
            else:
                user.balance -= user_cart_cost
                user.save()
                clearusercart(message)

    else:
        bot.send_message(message.chat.id, "Cart empty!")


@bot.message_handler(commands=['clearusercart'])
def clearusercart(message):
    for i in Users_Cart.objects.filter(
            user_chat_id = message.chat.id):
        i.delete()
    bot.send_message(message.chat.id, "Complete!")


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data:
        Users_Cart.objects.get_or_create(
            user_chat_id = call.message.chat.id,
            product = Product.objects.get(Name=call.data),
            date = datetime.now()
        )
        bot.send_message(call.message.chat.id, 'Product added to /cart')

bot.infinity_polling()
