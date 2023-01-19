import telebot
from decimal import Decimal, DecimalException
from gym.models import *
from connections import token
from datetime import datetime

bot = telebot.TeleBot(token=token)

def check(message):
    if Subscription.objects.get(
            user_chat_id__user_chat_id = message.chat.id).exercises == 0:
        return False
    else:
        return True

def sub_check(message):
    if not Subscription.objects.filter(
            user_chat_id__user_chat_id = message.chat.id):
        Subscription.objects.get_or_create(
            user_chat_id = User.objects.get(user_chat_id = message.chat.id),
            exercises = 0
        )

@bot.message_handler(commands=['start'])
def start(message):
    if not User.objects.filter(user_chat_id = message.chat.id):
        User.objects.get_or_create(
            user_chat_id = message.chat.id
        )
        Wallet.objects.get_or_create(
            user_chat_id = User.objects.get(user_chat_id = message.chat.id),
        )
    
    sub_check(message)
    if check(message):
        func_list = ['/categories', '/cart', '/payorder',
                     '/checkwallet', '/addtowallet', 
                     '/clearusercart', '/check_workout_exercises',
                     '/buy_workout_exercises', '/start_workout',
                     '/end_workout', '/select_trainer', '/list_workouts']
    else:
        bot.send_message(message.chat.id, 
                "You dont have workoud exercises! Buy with /buy_workout_exercises")
        func_list = ['/buy_workout_exercises', '/checkwallet',
                     '/addtowallet', '/list_workouts']

    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True)

    button_list = list()
    for i in func_list:
        button_list.append(telebot.types.KeyboardButton(i))
    keyboard.add(*button_list)

    bot.send_message(message.chat.id, 
        'Commands : ', reply_markup=keyboard)


@bot.message_handler(commands=['buy_workout_exercises'])
def buy_workout_exercises(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for obj in Sub_product.objects.all():
        button = telebot.types.InlineKeyboardButton(f'{obj.name} - {obj.cost}',
            callback_data=obj.name)
        keyboard.add(button)

    bot.send_message(message.chat.id, 'Exercises',
        reply_markup=keyboard)

 
@bot.message_handler(commands=['start_workout'], func=check)
def start_workout(message):
    time = datetime.now()
    user = User.objects.get(user_chat_id = message.chat.id)

    if not user.on_workout:
        TrainingTime.objects.get_or_create(
            user_chat_id = User.objects.get(user_chat_id = message.chat.id),
            start_time = time
        )
        
        user.on_workout = True
        user.save()

        bot.send_message(message.chat.id, 
                         f'Workout start time - {time.strftime("%H:%M:%S")}')
    else:
        bot.send_message(message.chat.id, 'You already on workout!')
        
    bot.send_message(message.chat.id, 'If you want choice avaliable trainer! ' +
                     '/select_trainer')

@bot.message_handler(commands=['end_workout'], func=check)
def end_workout(message):
    time = datetime.now()
    user = User.objects.get(user_chat_id = message.chat.id)
    user_train = TrainingTime.objects.filter(
                user_chat_id__user_chat_id = message.chat.id).latest('user_chat_id')
    user_sub = Subscription.objects.get(
            user_chat_id__user_chat_id = message.chat.id)

    if user.on_workout:
        user.on_workout = False
        user.save()
        
        user_train.end_time = time
        user_train.save()

        user_sub.exercises -= 1
        user_sub.save()

        bot.send_message(message.chat.id,
                         f'End of workout - {time.strftime("%H:%M:%S")}')

        if user_sub.exercises == 0:
            bot.send_message(message.chat.id, 'Buy exercises for continue!')
            start(message)
    else:
        bot.send_message(message.chat.id, 'You not on workout!')


@bot.message_handler(commands=['list_workouts'])
def list_workouts(message):
    user_workout_list = list()
    for i in TrainingTime.objects.filter(
            user_chat_id__user_chat_id = message.chat.id):
            user_workout_list.append(
                f'Start time - {i.start_time},\
                \nEnd time - {i.end_time}\
                \nTrainer - {i.trainer}\n')

    bot.send_message(message.chat.id, '\n'.join(user_workout_list))


@bot.message_handler(commands=['select_trainer'], func=check)
def select_trainer(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    trainers = Trainer.objects.filter(free = True)

    if trainers:
        for obj in trainers:
            button = telebot.types.InlineKeyboardButton(f'{obj.name} {obj.surname}',
                callback_data=obj.name)
            keyboard.add(button)

            bot.send_message(message.chat.id, 'Avaliable trainers :', 
                             reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Non aviliable trainers!')


@bot.message_handler(commands=['check_workout_exercises'], func=check)
def check_workout_exercises(message):
    count = Subscription.objects.get(
            user_chat_id__user_chat_id = message.chat.id).exercises
    
    bot.send_message(message.chat.id, f'Workouts - {count}')

@bot.message_handler(commands=['checkwallet'])
def check_wallet(message):
    bot.send_message(message.chat.id, Wallet.objects.get(
    user_chat_id__user_chat_id  = message.chat.id).balance)

@bot.message_handler(commands=['addtowallet'])
def walletsum(message):
    bot.send_message(message.chat.id, 
                     "Enter wallet sum to add : ")
    
    bot.register_next_step_handler(message, walletadding)

def walletadding(message):
    try:
        user = Wallet.objects.get(
            user_chat_id__user_chat_id = message.chat.id)
        user.balance += Decimal(message.text)
        user.save()
    except DecimalException:
        bot.send_message(message.chat.id, 'Non Digit!')
    else:
        bot.send_message(message.chat.id, "Summ added to wallet!")

def wallet_pay(message, cost):
            user = Wallet.objects.get(
                    user_chat_id__user_chat_id = message.chat.id)
            if user.balance < cost:
                bot.send_message(message.chat.id, "Not Enough money!")
                return False
            else:
                user.balance -= cost
                user.save()
                return True


@bot.message_handler(commands=['categories'], func=check)
def categories_button(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True)
    
    if check(message):
        for obj in Category.objects.all():
            button = telebot.types.KeyboardButton(obj.name)
            keyboard.add(button)
    else:
        button = telebot.types.KeyboardButton('subscription')
        keyboard.add(button)
    
    button = telebot.types.KeyboardButton('/start')
    keyboard.add(button)

    bot.send_message(message.chat.id, 
    'Categories : ', reply_markup=keyboard)


@bot.message_handler(func=lambda m: True
    if Category.objects.filter(name = m.text) and check(m) else False)
def category_button_handler(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for obj in Product.objects.filter(category__name = message.text):
        button = telebot.types.InlineKeyboardButton(f'{obj.name} - {obj.cost}',
            callback_data=obj.name)
        keyboard.add(button)

    bot.send_message(message.chat.id, 'products',
        reply_markup=keyboard)


@bot.message_handler(commands=['cart', 'payorder'], func=check)
def cart_and_payment(message):
    user_cart = [str(i.product)
    for i in Users_Cart.objects.filter(
        user_chat_id__user_chat_id = message.chat.id)]

    if user_cart:
        user_cart_result = dict()
        for i in user_cart:
            if i not in user_cart_result:
                user_cart_result[i] = user_cart.count(i)

        user_cart_cost = sum([i.product.cost for i in
                Users_Cart.objects.filter(
                    user_chat_id__user_chat_id = message.chat.id)])

        if message.text == '/cart':
            bot.send_message(message.chat.id,
                '\n'.join(f'{key} - {value}'
                for key, value in user_cart_result.items()) + 
                f'\nOrder cost - {user_cart_cost}')

        if message.text == '/payorder':
                wallet_pay(message, user_cart_cost)
                clearusercart(message)

    else:
        bot.send_message(message.chat.id, "Cart empty!")


@bot.message_handler(commands=['clearusercart'], func=check)
def clearusercart(message):
    for i in Users_Cart.objects.filter(
            user_chat_id__user_chat_id = message.chat.id):
        i.delete()
    bot.send_message(message.chat.id, "Complete!")


@bot.callback_query_handler(func=lambda call: True
                            if Trainer.objects.filter(name=call.data) else False)
def start_workout_callback(call):
    bot.send_message(call.message.chat.id, "KVAAA")


@bot.callback_query_handler(func=lambda call: True
                            if Sub_product.objects.filter(name=call.data) else False)
def sub_buy(call):
    sub_product = Sub_product.objects.get(name = call.data)

    sub_check(call.message)

    if wallet_pay(call.message, sub_product.cost):
        bot.send_message(call.message.chat.id, 'Succsess buy!')

        user = Subscription.objects.get(
                user_chat_id__user_chat_id = call.message.chat.id)
        user.exercises += sub_product.exercises
        user.save()

        start(call.message)


@bot.callback_query_handler(func=lambda call: True
                            if Product.objects.filter(name=call.data) else False)
def user_cart(call):
    Users_Cart.objects.get_or_create(
        user_chat_id = User.objects.get(user_chat_id = call.message.chat.id),
        product = Product.objects.get(name=call.data),
        category = Product.objects.get(name=call.data).category,
        date = datetime.now()
    )
    bot.send_message(call.message.chat.id, 'Product added to /cart')

bot.infinity_polling()
