import telebot 
from telebot import types 
from telega_token import TOKEN
import json
from parsing import main

json_str = open('file_json.json', 'r', encoding='utf-8')
json_object = json.load(json_str)

new_list = [dict(i) for i in json_object]

token = TOKEN
bot = telebot.TeleBot(token)

def inlinekeyboard():
    inline_keyboard_title = types.InlineKeyboardMarkup()
    index = 1
    for line in new_list:
        new_line = line['title']
        num = f'{str(index)}. '
        button = types.InlineKeyboardButton(f'{num + new_line}', callback_data=f'{index}')
        index += 1
        inline_keyboard_title.add(button)
    return inline_keyboard_title

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
k1 = types.KeyboardButton('Да')
k2 = types.KeyboardButton('Нет')
keyboard.add(k1, k2)

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Здравствуйте {message.chat.first_name}, вы ищите себе подходящую машину?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_start)

def get_start(message):
    chat_id = message.chat.id
    if message.text == 'Да':
        main()
        bot.send_message(chat_id, 'Список машин:', reply_markup=inlinekeyboard())
    else:
        bot.send_message(chat_id, f'Досвидания {message.chat.first_name}')

new_list = [dict(i) for i in json_object]

file1 = open('info_link.txt', 'r')
file1 = file1.read()
file1 = file1.split('\n')
file1.pop(-1)

for line in new_list:
    for link in file1:
        line['link'] = link

file2 = open('info_usd.txt', 'r')
file2 = file2.read()
usd = file2

def get_clear_info(index):
    result = new_list[index]
    new_result = []
    for line1 in result.values():
        new_result.append(line1)
    finish = '\n'.join(new_result[:-1])
    return finish

@bot.callback_query_handler(func=lambda c: True)
def get_info(c):
    chat_id = c.message.chat.id

    def keyboard(index):
        inline_keyboard = types.InlineKeyboardMarkup()
        k1 = types.InlineKeyboardButton('Назад', callback_data=f'b {index}')
        k2 = types.InlineKeyboardButton('Назад к списку', callback_data='back list')
        k3 = types.InlineKeyboardButton('Вперед', callback_data=f'n {index}')
        k4 = types.InlineKeyboardButton('Курс USD', callback_data='usd')
        k5 = types.InlineKeyboardButton('Калькулятор', callback_data=f'calc {index}')
        k6 = types.InlineKeyboardButton('Ссылка', url=file1[index])
        k7 = types.InlineKeyboardButton('Выход', callback_data='exit')
        inline_keyboard.add(k1, k2, k3, k4, k5, k6, k7)
        return inline_keyboard
    print(c.data, c.from_user.first_name)

    if c.data == 'back list':
        bot.edit_message_text('Вы обратно вернулись в список:', chat_id, c.message.message_id, reply_markup=inlinekeyboard())
    elif c.data == 'exit':
        bot.edit_message_text('Досвидания', chat_id, c.message.message_id, reply_markup=None)
    elif c.data == 'usd':
        bot.send_message(chat_id, f'1$ = {usd} сом')
    elif c.data[:4] == 'calc':
        index = list(filter(lambda x: x.isdigit(), c.data))
        index = int(''.join(index))
        result = new_list[index]
        new_result = []
        for line1 in result.values():
            new_result.append(line1)
        num = new_result[1]
        num = list(filter(lambda x: x.isdigit(), num))
        num = ''.join(num)
        num = int(num)
        bot.send_message(chat_id, f'{new_result[0]}: {round(float(usd) * num)} сом')
    elif c.data[0] == 'b':
        try:
            index = list(filter(lambda x: x.isdigit(), c.data))
            index = ''.join(index)
            index = int(index) - 1
            bot.edit_message_text(f'{get_clear_info(index)}', chat_id, c.message.message_id, reply_markup=keyboard(index))
        except:
            bot.send_message(chat_id, 'Вы находитесь в начале списка')
    elif c.data[0] == 'n':
        try:
            index = list(filter(lambda x: x.isdigit(), c.data))
            index = ''.join(index)
            index = int(index) + 1
            bot.edit_message_text(f'{get_clear_info(index)}', chat_id, c.message.message_id, reply_markup=keyboard(index))
        except:
            bot.send_message(chat_id, 'Вы находитесь в конце списка')
    else:
        index = int(c.data) - 1
        bot.edit_message_text(f'{get_clear_info(index)}', chat_id, c.message.message_id, reply_markup=keyboard(index))

bot.polling()
