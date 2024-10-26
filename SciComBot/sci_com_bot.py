import datetime
import os

import telebot
from openpyxl.workbook import Workbook
from telebot import types

time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
print(f"{time}\nProcessing...")
bot = telebot.TeleBot('7811486667:AAGBf7cUvTFX6E0MJPlTCoHJis7s4mXg-cg')


def log_msg(message):
    user_id = message.from_user.id
    user_name = str(message.from_user.first_name)
    user_surname = str(message.from_user.last_name)

    date_of_msg = datetime.datetime.now().strftime("%d.%m.%Y")
    time_of_msg = datetime.datetime.now().strftime("%H:%M:%S")

    msg_txt = message.text
    log_info = (f"UID: {user_id}\n"
                f"Name: {user_name} {user_surname}\n"
                f"Text:\"{msg_txt}\"\n"
                f"Date: {date_of_msg}\n"
                f"Time: {time_of_msg}\n")

    # bot.send_message(988170385, log_info)
    print(log_info)


def go_to_main_menu(message, msg):
    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    kb_about = types.KeyboardButton("❌#О_нас")
    kb_faq = types.KeyboardButton("❌#FAQ")
    kb_tg_channel = types.KeyboardButton("Telegram-канал")
    kb_ask = types.KeyboardButton('❌Задать вопрос')
    kb_get_docs = types.KeyboardButton("Зарегистрироваться")

    kb_markup.add(kb_get_docs).row(kb_faq, kb_tg_channel, kb_about).add(kb_ask)
    bot.send_message(message.from_user.id, msg.format(message.from_user), parse_mode='html',
                     reply_markup=kb_markup)


def create_xlsx():
    work_book = Workbook()
    work_sheet = work_book.active
    head = ["Дата", "Время", "ID кандидата", "Фамилия", "Имя", "Отчество", "Дата рождения", "Наименование ВК",
            "Наименование ВУЗа", "Наименование специальности", "Средний балл"]
    work_sheet.append(head)
    work_book.save('Список кандидатов.xlsx')
    return work_book


list_of_candidates = create_xlsx()


def add_cands_2_xlsx(list_of_cands, message, surname, name, patronymic, birth, mil_stat, university, field_study,
                     score):
    user_id = message.from_user.id

    user_name = str(message.from_user.first_name)
    user_surname = str(message.from_user.last_name)
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    time = datetime.datetime.now().strftime("%H:%M:%S")
    row = [date, time, user_id, surname, name, patronymic, birth, mil_stat, university, field_study, score]
    sheet = list_of_cands.active
    sheet.append(row)


# try:
@bot.message_handler(commands=["start"])
def start(message):
    sticker = open('stickers/welcome_bender.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    welcome_msg = f'Здравствуйте, {welcome_name}\n Я - SciComBot, и я провожу отбор кандидатов в научную роту.\nВыберете интересующий Вас раздел 👇'
    go_to_main_menu(message, welcome_msg)
    log_msg(message)


@bot.message_handler(content_types=["text"])
def welcome(message):
    if message.text == "Зарегистрироваться":
        bot.send_message(message.chat.id, "#ToDo\n"
                                          "Реакция происходит после отправки 2-х сообщений")

        bot.register_next_step_handler(message, is_russian)

    if message.text == "Telegram-канал":
        bot.send_message(message.chat.id, "https://t.me/+ntFED2PMwUo2MDZi")
    # ToDo:
    if message.text == "❌#О_нас":
        bot.send_message(message.chat.id,
                         "#Todo\n"
                         "В разработке\n\nЗдесь будут отображаться новости о научной роте из хештега #О_нас")
    # ToDo:
    if message.text == "❌#FAQ":
        bot.send_message(message.chat.id,
                         "#Todo\n"
                         "В разработке\n\nЗдесь будут отображаться ответы на частозадаваемые вопросы из хештега #FAQ")
    # ToDo:
    if message.text == "❌Задать вопрос":
        bot.send_message(message.chat.id,
                         "#Todo\n"
                         "В разработке\n\nЗдесь будет предлагаться форма для вопроса, отправляемого личным сообщением")
    log_msg(message)


@bot.message_handler(content_types=['text'])
def is_russian(message):
    btn_hied_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_yes = types.KeyboardButton("Да")
    btn_no = types.KeyboardButton("Нет")
    btn_hied_markup.add(btn_yes, btn_no)
    bot.send_message(message.from_user.id, 'Являетесь ли Вы гражданином Российской Федерации?',
                     reply_markup=btn_hied_markup)
    bot.register_next_step_handler(message, is_higher_education)
    log_msg(message)


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
        go_to_main_menu(message,
                        "Извините, наличие гражданства Российской Федерации является обязательным условием для отбора в научную роту")
    else:
        bot.send_message(message.from_user.id, 'Я Вас не понял(')
        is_russian(message)
    log_msg(message)


def is_aged(message):
    if message.text == "Да":

        btn_age_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn_one = types.KeyboardButton("1")
        btn_two = types.KeyboardButton("2")
        btn_three = types.KeyboardButton("3")
        btn_four = types.KeyboardButton("4")
        btn_five = types.KeyboardButton("25")
        btn_six = types.KeyboardButton("6")
        btn_seven = types.KeyboardButton("7")
        btn_eight = types.KeyboardButton("8")
        btn_nine = types.KeyboardButton("9")
        btn_zero = types.KeyboardButton("0")
        btn_age_markup.add(btn_one, btn_two, btn_three, btn_four, btn_five, btn_six, btn_seven, btn_eight, btn_nine,
                           btn_zero)
        # ToDo:
        bot.send_message(message.from_user.id, '#Todo\n'
                                               'Здесь должна вызываться цифровая клавиатура',
                         reply_markup=btn_age_markup)
        bot.send_message(message.from_user.id, 'Укажите Ваш возраст')

        bot.register_next_step_handler(message, get_source)

    elif message.text == "Нет":
        go_to_main_menu(message,
                        "Извините, наличие Высшего технического образования является обязательным условием для отбора в научную роту")
    else:
        bot.send_message(message.from_user.id, 'Я Вас не понял(')
        bot.send_message(message.from_user.id,
                         '#Todo\n'
                         'Здесь необходимо возвращаться на 1 шаг назад, а не на 2. Так как, в функции is_higher_education(message) текущий параметр message передается в функцию и функция срабатывает по этому параметру, а значит возвращается еще на шаг назад. В параметр необходимо передавать message из предыдущей функции. Осталось понять как...')
        is_higher_education(message)
    log_msg(message)


def get_source(message):
    if 18 < int(message.text) < 30:
        btn_remove = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Напишите, откуда о нас узнали?", reply_markup=btn_remove)
        bot.send_message(message.chat.id, "#Todo\n"
                                          "Здесь необходимо добавлять источники в отдельный файл")
        bot.register_next_step_handler(message, get_surname)


    else:
        go_to_main_menu(message,
                        'В Соответствии с положениями п.п."а", пункта 1, статьи 22 \"Граждане, подлежащие призыву на военную службу\"'
                        'Федерального закона от 28.03.1998 N 53-ФЗ (ред. от 02.10.2024) \"О воинской обязанности и военной службе\",'
                        'призыву  на  военную службу подлежат граждане мужского пола в возрасте от 18 до 30 лет, состоящие на воинском учете '
                        'или не состоящие, но обязанные состоять на воинском учете и не пребывающие в запасе ')
    log_msg(message)


def get_surname(message):
    bot.send_message(message.from_user.id, 'Напишите Вашу фамилию')
    global surname
    # bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    surname = message.text
    bot.register_next_step_handler(message, get_name)
    log_msg(message)


def get_name(message):
    bot.send_message(message.chat.id, "Введите ваше имя")
    global name
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    name = message.text
    bot.register_next_step_handler(message, get_patronymic)
    log_msg(message)


def get_patronymic(message):
    bot.send_message(message.from_user.id, 'Напишите ваше отчество')
    global patronymic
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    patronymic = message.text
    bot.register_next_step_handler(message, get_date_birth)
    log_msg(message)


def get_date_birth(message):
    bot.send_message(message.from_user.id, '#ToDO\n'
                                           'Здесь должна выводиться цифровая клавиатура')
    bot.send_message(message.from_user.id, 'Напишите свою дату рождения в формате (дд.мм.гггг)')
    global date_birth
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    date_birth = message.text
    bot.register_next_step_handler(message, get_military_station)
    log_msg(message)


def get_military_station(message):
    bot.send_message(message.from_user.id, 'Напишите название своего военного комиссариата')
    global mil_station
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    mil_station = message.text
    bot.register_next_step_handler(message, get_university)
    log_msg(message)


def get_university(message):
    bot.send_message(message.from_user.id, 'Напишите название своего ВУЗа')
    global university
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    university = message.text
    bot.register_next_step_handler(message, get_field_study)
    log_msg(message)


def get_field_study(message):
    bot.send_message(message.from_user.id, 'Напишите направление подготовки в ВУЗе')
    global field_study
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    field_study = message.text
    bot.register_next_step_handler(message, get_score)
    log_msg(message)


def get_score(message):
    bot.send_message(message.from_user.id, 'Напишите средний балл по диплому (х.х)')
    global score
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)
    score = message.text
    bot.register_next_step_handler(message, send_examples)
    log_msg(message)


def send_examples(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.id - 1)

    add_cands_2_xlsx(list_of_candidates, message, name, surname, patronymic, date_birth, mil_station, university,
                     field_study,
                     score)
    doc = open("Список кандидатов.xlsx", 'rb')
    bot.send_message(message.from_user.id,
                     "#Todo\n"
                     "Данный документ отправляется пользователю только в тестовой версии для наглядности работы.\n"
                     "В рабочей версии документ будет отправлять только админам")

    bot.send_message(message.from_user.id,
                     "#Todo\n"
                     "Список кандидатов не заполняется, необходимо проверить работу функций create_xlsx и add_cands_2_xlsx \n")

    bot.send_document(988170385, doc)
    if message.text != "":
        bot.send_message(message.from_user.id,
                         'Отличная работа🔥\n Для завершения осталось заполнить 3 документа и отправить их мне в виде файлов.\nДержи образцы')
    txt = open('ads/1.Лист собеседования.txt', 'rb')
    bot.send_document(message.chat.id, txt)
    pdf = open('ads/2.Согласие.pdf', 'rb')
    bot.send_document(message.chat.id, pdf)
    photo = open('ads/3.Заявление.jpg', 'rb')
    bot.send_document(message.chat.id, photo)
    bot.send_message(message.from_user.id,
                     'Основанием для рассмотрения кандидатов отборочными комиссиями является:'
                     'ПЕРЕЧЕНЬ ДОКУМЕНТОВ, НЕОБХОДИМЫХ ДЛЯ В ВКЛЮЧЕНИЯ В РЕЙТИНГОВЫЙ СПИСОК КАНДИДАТОВ.\n\n'
                     "1) Лист собеседования;\n"
                     "(Заполнить, вложить фотографию и в электронном виде в формате .doc отправить личным сообщением."
                     "Необходим для получения справочной информации о кандидате, формирования его первичного портрета, проверки соответствия предъявляемым требованиям. "
                     "Листы собеседования уточняются после проведения беседы с кандидатами и проверки подлинности предоставленной информации путём сличения копий "
                     "предоставленных документов с их оригиналами)\n\n"
                     "2) Согласие на обработку персональных данных\n;"
                     "(Согласие на обработку нужно распечатать, заполнить от руки, поставить подпись, отсканировать и файл .pdf также отправить личным сообщением"
                     'Необходимо для опубликования Ваших данных в рейтинговых списках на сайте МОРФ)\n\n'
                     '3) Заявление на прохождение в научной роте Военной академии связи;'
                     "(Заявление написать от руки, отсканировать и отправить в формате .pdf. "
                     "Необходимо для подтверждения того, что кандидат будет рассматриваться в научную роту Военной академии связи)\n\n"
                     "4) Копия диплома;\n"
                     "(Копию диплома необходимо отправить в формате .pdf"
                     "Необходима для подтверждения уровня образования и проверки среднего балла)")
    log_msg(message)


@bot.message_handler(content_types=['document'])
def get_user_docs(message):
    os.makedirs(f'{message.from_user.first_name} {message.from_user.last_name}', exist_ok=True)
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = f'{message.from_user.first_name} {message.from_user.last_name}/{message.document.file_name} ({message.from_user.first_name} {message.from_user.last_name})'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, f"Отлично🔥\nПолучил от Вас:\n{message.document.file_name}")
    log_msg(message)


bot.polling(none_stop=True)
