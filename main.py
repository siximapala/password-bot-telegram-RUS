import telebot
import random
from telebot import types
bot = telebot.TeleBot('##############################ТОКЕН')

unique_symbols_cond = False
numbers_cond = False
uppercase_cond = False
was_btn1_pressed = 1
was_btn2_pressed = 1
was_btn3_pressed = 1

# ГЕНЕРАТОР ПАРОЛЯ
def generate_password(length_pas):
    global unique_symbols_cond
    global numbers_cond
    global uppercase_cond
    alphabet_main = 'qwertyuiopasdfghjklzxcvbnm'
    alphabet_unique_symbols = '!@#$%'
    alphabet_numbers = '0123456789'
    alphabet_uppercase = 'QWERTYUIOPASDFGHJKLZXCVBNM'

    gen_code = ['0','0','0']

    if unique_symbols_cond == True:
        gen_code[0] = '1'
    if numbers_cond == True:
        gen_code[1] = '1'
    if uppercase_cond == True:
        gen_code[2] = '1'

    return_value = []
    choice_for_one = ''
    choice_advanced_two = ''
    choice_advanced_one = ''

    if gen_code == ['0','0','0']:
        for i in range(length_pas):
                return_value.append(random.choice(alphabet_main))
    elif gen_code == ['1','1','1']:
        for i in range(length_pas//4):
            return_value.append(random.choice(alphabet_main))
        length_pas -= length_pas//4
        for i in range (length_pas//3):
            return_value.append(random.choice(alphabet_unique_symbols))
        length_pas -= length_pas//3
        for i in range(length_pas//2):
            return_value.append(random.choice(alphabet_numbers))
        length_pas -= length_pas//2
        for i in range(length_pas): 
            return_value.append(random.choice(alphabet_uppercase))
        random.shuffle(return_value)
        
    elif gen_code == ['1','0','0']:
        choice_for_one = alphabet_unique_symbols
    elif gen_code == ['0','1','0']:
        choice_for_one = alphabet_numbers
    elif gen_code == ['0','0','1']:
        choice_for_one = alphabet_uppercase
    elif gen_code == ['1','1','0']:
        choice_advanced_one = alphabet_unique_symbols
        choice_advanced_two = alphabet_numbers
    elif gen_code == ['1','0','1']:
        choice_advanced_one = alphabet_unique_symbols
        choice_advanced_two = alphabet_uppercase
    elif gen_code == ['0','1','1']:
        choice_advanced_one = alphabet_numbers
        choice_advanced_two = alphabet_uppercase

    if choice_for_one != '':
        for i in range(length_pas//3):
            return_value.append(random.choice(choice_for_one))
        length_pas -= length_pas//3
        for i in range(length_pas):
            return_value.append(random.choice(alphabet_main))
            random.shuffle(return_value)
    if choice_advanced_one != '':
        for i in range(length_pas//3):
            return_value.append(random.choice(alphabet_main))
        length_pas -= length_pas//3
        for i in range(length_pas//2):
            return_value.append(random.choice(choice_advanced_one))
        length_pas -= length_pas//2
        for i in range(length_pas):
            return_value.append(random.choice(choice_advanced_two))
        random.shuffle(return_value)

    return ''.join(return_value)


#ДОП СООБЩЕНИЕ КОНТРОЛЬ НАЖАТЫХ ГАЛОЧЕК
def check_checks():
    result = ['НЕТ❌','НЕТ❌','НЕТ❌']
    global unique_symbols_cond
    global numbers_cond
    global uppercase_cond
    if unique_symbols_cond == True:
        result[0] = 'ДА✅'
    if numbers_cond == True:
        result[1] = 'ДА✅'
    if uppercase_cond == True:
        result[2] = 'ДА✅'
    return f"Выбранные параметры: \nУникальные символы: {result[0]} \nЦифры: {result[1]} \nПрописные буквы: {result[2]}"

# /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Уникальные Символы")
    btn2 = types.KeyboardButton("Цифры")
    btn3 = types.KeyboardButton("Строчные буквы")
    btn4 = types.KeyboardButton("Помощь")
    markup.add(btn1,btn2,btn3,btn4)
    username = message.from_user.username
    Main_title = f'Привет, <b>{username}</b>! \nЗдесь ты можешь сгенерировать пароль. Пароли не сохраняются в системе бота. Нажми на параметры, необходимые для пароля. \nПри нажатии параметр включится, отключится при повторном нажатии.'
    Main_title_sec = f'\n После того как ты введёшь число (длина пароля), произойдёт генерация. \nМакс. длина: 4000 символов. \nМин. длина: 7 символов.'
    bot.send_message(message.chat.id,Main_title,parse_mode='html',reply_markup=markup)
    bot.send_message(message.chat.id,Main_title_sec,reply_markup=markup)

#НАСТРОЙКИ ГЕНЕРАЦИИ
@bot.message_handler(content_types=['text'])
def message_reply(message):
    global unique_symbols_cond
    global numbers_cond
    global uppercase_cond
    global was_btn1_pressed
    global was_btn2_pressed
    global was_btn3_pressed
    if (message.text=="Уникальные Символы"):
        if was_btn1_pressed == 1:
            unique_symbols_cond = True
            bot.send_message(message.chat.id,"Использование уникальных символов включено! ✅")
            bot.send_message(message.chat.id,check_checks())
        elif was_btn1_pressed == -1:
            unique_symbols_cond = False
            bot.send_message(message.chat.id,"Использование уникальных символов выключено! ❌")
            bot.send_message(message.chat.id,check_checks())
        was_btn1_pressed *= -1
    if (message.text=="Цифры"):
        if was_btn2_pressed == 1:
            numbers_cond = True
            bot.send_message(message.chat.id,"Использование цифр включено! ✅")
            bot.send_message(message.chat.id,check_checks())
        elif was_btn2_pressed == -1:
            numbers_cond = False
            bot.send_message(message.chat.id,"Использование цифр выключено! ❌")
            bot.send_message(message.chat.id,check_checks())
        was_btn2_pressed *= -1
    if (message.text == "Строчные буквы"):
        if was_btn3_pressed == 1:
            uppercase_cond = True
            bot.send_message(message.chat.id,"Использование строчных букв включено! ✅")
            bot.send_message(message.chat.id,check_checks())
        elif was_btn3_pressed == -1:
            uppercase_cond = False
            bot.send_message(message.chat.id,"Использование строчных букв выключено! ❌")
            bot.send_message(message.chat.id,check_checks())
        was_btn3_pressed *= -1
    if (message.text == "Помощь"):
        bot.send_message(message.chat.id,"Ты можешь выбрать 3 настройки: Использование уникальных символов ('! @ # $ %'), цифр, СТРОЧНЫХ букв.")
        bot.send_message(message.chat.id,"После того, как ты напишешь число от 7 до 4000, произойдёт генерация пароля, который ты можешь копировать и использовать! \nСделал @tblmm.")
    else:
        password_length_numb = message.text
        try:
            password_length_numb = int(password_length_numb)
            if (password_length_numb < 6):
                bot.send_message(message.chat.id,"Пароль должен быть больше 6 символов!")
            elif password_length_numb > 4000:
                bot.send_message(message.chat.id,"Пароль должен быть меньше 4001 символа!")
            else:
                bot.send_message(message.chat.id,generate_password(password_length_numb))
        except:
            pass
bot.polling(none_stop=True) 
