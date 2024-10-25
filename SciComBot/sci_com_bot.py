import telebot
import os
from telebot import types

bot = telebot.TeleBot('7811486667:AAGBf7cUvTFX6E0MJPlTCoHJis7s4mXg-cg')

# try:
@bot.message_handler(commands=["start"])
def start(message):
    sticker = open('stickers/welcome_bender.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    welcome_msg = f'Здравствуйте, {welcome_name}\n Я - SciComBot, и я провожу отбор кандидатов в научную роту.\nВыберете интересующий Вас раздел 👇'

    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb_about = types.KeyboardButton("❌#О_нас")
    kb_faq = types.KeyboardButton("❌#FAQ")
    kb_tg_channel = types.KeyboardButton("Telegram-канал")
    kb_ask = types.KeyboardButton('❌Задать вопрос')
    kb_get_docs = types.KeyboardButton("Зарегистрироваться")

    kb_markup.add(kb_about, kb_faq, kb_tg_channel, kb_ask, kb_get_docs)

    bot.send_message(message.from_user.id, welcome_msg.format(message.from_user), parse_mode='html',
                     reply_markup=kb_markup)


@bot.message_handler(content_types=["text"])
def welcome(message):
    if message.text == "Зарегистрироваться":
        bot.register_next_step_handler(message, is_russian)
        # ToDo:
        temp_btn_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        temp_btn_ok = types.KeyboardButton("Понятно")
        temp_btn_markup.add(temp_btn_ok)
        bot.send_message(message.from_user.id,
                         'Тут должна быть верификация пользователя по образованию, возрасту и гражданству',
                         reply_markup=temp_btn_markup)

    if message.text == "Telegram-канал":
        bot.send_message(message.chat.id, "https://t.me/+ntFED2PMwUo2MDZi")
    # ToDo:
    if message.text == "❌#О_нас":
        bot.send_message(message.chat.id,
                         "В разработке\n\nЗдесь будут отображаться новости о научной роте из хештега #О_нас")
    # ToDo:
    if message.text == "❌#FAQ":
        bot.send_message(message.chat.id,
                         "В разработке\n\nЗдесь будут отображаться ответы на частозадаваемые вопросы из хештега #FAQ")
    # ToDo:
    if message.text == "❌Задать вопрос":
        bot.send_message(message.chat.id,
                         "В разработке\n\nЗдесь будет предлагаться форма для вопроса, отправляемого личным сообщением")


@bot.message_handler(content_types=['text'])
def is_russian(message):
    btn_hied_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_yes_hied = types.KeyboardButton("Да")
    btn_no_hied = types.KeyboardButton("Нет")
    btn_hied_markup.add(btn_yes_hied, btn_no_hied)
    bot.send_message(message.from_user.id, 'Являетесь ли Вы гражданином Российской Федерации?',
                     reply_markup=btn_hied_markup)

    bot.register_next_step_handler(message, is_higher_education)


def is_higher_education(message):
    if message.text == "Да":
        btn_hied_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_yes_hied = types.KeyboardButton("Да")
        btn_no_hied = types.KeyboardButton("Нет")
        btn_hied_markup.add(btn_yes_hied, btn_no_hied)
        bot.send_message(message.from_user.id, 'Имеется ли у Вас оконченное высшее техническое образование?',
                         reply_markup=btn_hied_markup)
        bot.register_next_step_handler(message, is_aged)
    elif message.text == "Нет":
        bot.send_message(message.from_user.id,
                         'Извините, наличие гражданства Российской Федерации является обязательным условием для отбора в научную роту')
        bot.register_next_step_handler(message, is_russian)
    else:
        bot.send_message(message.from_user.id, 'Я Вас не понял(')
        bot.register_next_step_handler(message, is_russian)


def is_aged(message):
    btn_age_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn_one = types.KeyboardButton("1")
    btn_two = types.KeyboardButton("2")
    btn_three = types.KeyboardButton("3")
    btn_four = types.KeyboardButton("4")
    btn_five = types.KeyboardButton("5")
    btn_six = types.KeyboardButton("6")
    btn_seven = types.KeyboardButton("7")
    btn_eight = types.KeyboardButton("8")
    btn_nine = types.KeyboardButton("9")
    btn_zero = types.KeyboardButton("0")
    btn_age_markup.add(btn_one, btn_two, btn_three, btn_four, btn_five, btn_six, btn_seven, btn_eight, btn_nine,
                       btn_zero)
    btn_remove = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Укажите Ваш возраст',
                     reply_markup=btn_age_markup)
    # ToDo:
    bot.register_next_step_handler(message, get_source)
    bot.send_message(message.from_user.id, 'Здесь должна вызываться цифровая клавиатура', reply_markup=btn_remove)


# def get_name(message):
#     bot.send_message(message.chat.id, "Введите ваше имя")
#     global name
#     name = message.text
#     bot.send_message(message.from_user.id, 'Напишите Вашу фамилию')
#     bot.register_next_step_handler(message, get_surname)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_surname(message):
#     global surname
#     surname = message.text
#     bot.send_message(message.from_user.id, 'Напишите ваше отчество')
#     bot.register_next_step_handler(message, get_patronymic)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_patronymic(message):
#     global patronymic
#     patronymic = message.text
#     bot.send_message(message.from_user.id, 'Напишите свою дату рождения в формате (дд.мм.гггг)')
#     bot.register_next_step_handler(message, get_date_birth)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_date_birth(message):
#     global date_birth
#     date_birth = message.text
#     bot.send_message(message.from_user.id, 'Напишите название своего военного комиссариата')
#     bot.register_next_step_handler(message, get_military_station)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_military_station(message):
#     global mil_station
#     mil_station = message.text
#     bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')
#     bot.register_next_step_handler(message, get_university)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_university(message):
#     global university
#     university = message.text
#     bot.send_message(message.from_user.id, 'Напишите направление подготовки в ВУЗе')
#     bot.register_next_step_handler(message, get_field_study)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
#
#
# def get_field_study(message):
#     global field_study
#     field_study = message.text
#     bot.send_message(message.from_user.id, 'Напишите средний балл по диплому (х.х)')
#     bot.register_next_step_handler(message, get_source)
#     bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

def get_source(message):
    global source
    bot.send_message(message.chat.id, "Напишите, откуда о нас узнали?")

    source = message.text
    bot.send_message(message.from_user.id,
                     'Отличная работа🔥\n Для завершения осталось заполнить 3 документа и отправить их мне в виде файлов.\nДержи образцы')
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    txt = open('ads/1.Лист собеседования.txt', 'rb')
    bot.send_document(message.chat.id, txt)
    pdf = open('ads/2.Согласие.pdf', 'rb')
    bot.send_document(message.chat.id, pdf)
    photo = open('ads/3.Заявление.jpg', 'rb')
    bot.send_document(message.chat.id, photo)

    bot.send_message(message.from_user.id, 'Основанием для рассмотрения кандидатов отборочными комиссиями является:'
                                           'ПЕРЕЧЕНЬ ДОКУМЕНТОВ, НЕОБХОДИМЫХ ДЛЯ В ВКЛЮЧЕНИЯ В РЕЙТИНГОВЫЙ СПИСОК КАНДИДАТОВ.'
                                           "1) Лист собеседования;"
                                           "(Заполнить, вложить фотографию и в электронном виде в формате .doc отправить личным сообщением."
                                           "Необходим для получения справочной информации о кандидате, формирования его первичного портрета, проверки соответствия предъявляемым требованиям. Листы собеседования уточняются после проведения беседы с кандидатами и проверки подлинности предоставленной информации путём сличения копий предоставленных документов с их оригиналами)"

                                           "2) Согласие на обработку персональных данных;"
                                           "(Согласие на обработку нужно распечатать, заполнить от руки, поставить подпись, отсканировать и файл .pdf также отправить личным сообщением"
                                           'Необходимо для опубликования Ваших данных в рейтинговых списках на сайте МОРФ)'

                                           '3) Заявление на прохождение в научной роте Военной академии связи;'
                                           "(Заявление написать от руки, отсканировать и отправить в формате .pdf. Необходимо для подтверждения того, что кандидат будет рассматриваться в научную роту Военной академии связи)"

                                           "4) Копия диплома;"
                                           "(Копию диплома необходимо отправить в формате .pdf"
                                           "Необходима для подтверждения уровня образования и проверки среднего балла)")


def get_user_docs(message):
    os.makedirs(f'{message.from_user.first_name} {message.from_user.last_name}', exist_ok=True)
    chat_id = message.chat.id

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = f'{message.from_user.first_name} {message.from_user.last_name}/{message.document.file_name} ({message.from_user.first_name} {message.from_user.last_name})'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, f"Отлично🔥\nПолучил от Вас:\n{message.document.file_name}")


# nОтправьте в ответном сообщении:\n1) Фамилию Имя Отчество\n2) ВУЗ (дата окончания) \n3) Уровень образования\n4) Специальность \n5) Средний балл\n6) Откуда узнали о роте'
# except Exception as e:
#     bot.send_message(message.from_user.id, e.text)

bot.polling(none_stop=True)
