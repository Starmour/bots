# Подключаем библиотеку
import os
from datetime import datetime

import requests
import speech_recognition
import telebot
from PIL import Image, Image
from bs4 import BeautifulSoup
from keyboa import Keyboa
from openpyxl.workbook import Workbook
from pydub import AudioSegment
from telebot import types

print("Processing...")
# Здесь нужно вставить токен, который дал BotFather при регистрации
# Пример: token = '2007628239:AAEF4ZVqLiRKG7j49EC4vaRwXjJ6DN6xng8'
token = '7921587804:AAF0_qyr0YyEqZKUw6SzHFtOWLbuxuRIHWw'  # <<< Ваш токен

# В этой строчке мы заводим бота и даем ему запомнить токен
bot = telebot.TeleBot(token)
work_book = Workbook()
work_sheet = work_book.active


# Пишем первую функцию, которая отвечает "Привет" на команду /start
# Все функции общения приложения с ТГ спрятаны в функции под @

def log_2_xlsx(message):
    user_id = message.from_user.id
    user_name = str(message.from_user.first_name)
    user_surname = str(message.from_user.last_name)
    date_of_msg = datetime.fromtimestamp(message.date).strftime("%d.%m.%Y")
    time_of_msg = datetime.fromtimestamp(message.date).strftime("%H:%M:%S")
    msg_txt = message.text
    row = [user_id, date_of_msg, time_of_msg, user_name + " " + user_surname, msg_txt]
    work_sheet.append(row)
    work_book.save('log_list.xlsx')


def logging(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    time_of_msg = datetime.fromtimestamp(message.date).strftime("%d.%m.%Y %H:%M:%S")
    msg_txt = message.text

    bot.send_message(988170385,
                     f"ID: {user_id}\nName: {user_name} {user_surname}\nText:\"{msg_txt}\"\nTime: {time_of_msg}")


@bot.message_handler(commands=['start'])
def say_hi(message):
    log_2_xlsx(message)
    sticker = open('stickers/welcome_bender.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    welcome_name = f'{message.from_user.first_name} {message.from_user.last_name}'
    welcome_msg = f'Здравствуйте, {welcome_name}!\nМеня зовут TestBot и я готов продемонстрировать Вам свои базовые функции.\nВыберете интересующий Вас раздел 👇'

    kb_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    kb_welcome = types.KeyboardButton("Приветствие")
    kb_img = types.KeyboardButton("🖼️Обработка изображений")
    kb_voice = types.KeyboardButton("🎙Перевод голоса в текст")
    kb_parser = types.KeyboardButton('🔨Html-parser')
    kb_openai = types.KeyboardButton("🔨OpenAI")
    kb_articles = types.KeyboardButton("📰Полезные статьи")

    kb_markup.add(kb_welcome).row(kb_img, kb_voice).row(kb_parser, kb_openai).add(kb_articles)

    # Определение конфигурации расположения кнопок
    bot.send_message(message.from_user.id, welcome_msg.format(message.from_user), parse_mode='html',
                     reply_markup=kb_markup)

    # INLINE BUTTONS IN MESSAGE
    # items = [["Приветствие"], ["🖼️Обработка изображений", "🎙Перевод голоса в текст"], ["🔨Html-parser", "OpenAI"]]
    # kb = Keyboa(items).keyboard
    # bot.send_message(message.from_user.id, welcome_msg.format(message.from_user), parse_mode='html',
    #                  reply_markup=kb)


@bot.message_handler(content_types=["text"])
def welcome(message):
    if message.text == "Приветствие":
        say_hi(message)
    if message.text == "🖼️Обработка изображений":
        log_2_xlsx(message)
        txt = open('show_scripts/reformatting_images.txt', 'rb')
        bot.send_message(message.chat.id, "Я могу изменять Ваши изображения.\n"
                                          "На данный момент я поддерживаю лишь функцию затемнения.\n"
                                          "Для того, чтобы воспользоваться ей отправьте мне Вашу картинку и я верну Вам ее через пару секунд.\n"
                                          "Прилагаю скрипт кода, которым я пользуюсь для данной функции")
        bot.send_document(message.chat.id, txt)

    # ToDo:
    if message.text == "🎙Перевод голоса в текст":
        log_2_xlsx(message)
        txt = open('show_scripts/audio_transcription.txt', 'rb')
        bot.send_message(message.chat.id,
                         "Я умею расшифровывать голосовые сообщения\n"
                         "Ввиду технических особенностей, длительность голосового сообщения ограничена 25 секундами, но я работаю над этим и совcем скоро вы сможете болтать часами, а я Вам все расшифрую.\n"
                         "Кстати, для того чтобы преобразовать Вашу речь в текст достаточно записать мне голосовое сообщение🎙 или отправить пересланное и я мигом отправлю Вам его расшифровку.")
        bot.send_document(message.chat.id, txt)
    # ToDo:
    if message.text == "🔨Html-parser":
        bot.send_message(message.chat.id,
                         "🔨В разработке\n\nЗдесь будет логика парсинга сайта")
        get_articles(message)

    # ToDo:
    if message.text == "🔨OpenAI":
        log_2_xlsx(message)
        bot.send_message(message.chat.id,
                         "🔨В разработке\n\nЗдесь будет применяться технологии OpenAI")

    if message.text == "📰Полезные статьи":
        log_2_xlsx(message)

        bot.send_message(message.from_user.id, "Полезная статья \"Парсим данные в Telegram на Python\"\n"
                                               "https: // skillbox.ru / media / code / parsim - dannye - v - telegram - na - python - chast - 2 - chitaem - i - analiziruem - soobshcheniya - iz - chatov /")
        bot.send_message(message.from_user.id, "Полезная статья \"Списки в Python\"\n"
                                               "https: // drive.google.com / file / d / 1XJyrBtQ4ZPbBlrpOs2twA0X4D1jN33FF / view")
        bot.send_message(message.from_user.id, "Полезная статья по созданию клавиатуры бота\n"
                                               "https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html")
        bot.send_message(message.from_user.id, "Полезная статья по работе с Json-файлами\n"
                                               "https://pythonist.ru/chtenie-i-zapis-v-fajl-json-obekta/")
        bot.send_message(message.from_user.id, "Как составить эффекитвное резюме\n"
                                               "https: // drive.google.com / file / d / 1uo763kscWwheM4jhV - q4Demz - h5r - cv3 / view")


def transform_image(filename, brightness):
    # Функция обработки изображения
    source_image = Image.open(filename)
    enhancer = Image.Brightness(source_image)
    # to reduce brightness by 50%, use factor 0.5
    source_image = enhancer.enhance(brightness / 100)
    source_image.save(filename)
    return filename


@bot.message_handler(content_types=['photo'])
def resend_photo(message):
    log_2_xlsx(message)
    bot.send_message(message.from_user.id, "Затемнение изображения...")

    # Функция отправки последнего обработанного изображения
    file_id = message.photo[-1].file_id
    filename = download_file(bot, file_id)
    transform_image(filename, 50)
    # Трансформируем изображение

    image = open(filename, 'rb')
    bot.send_photo(message.chat.id, image)
    image.close()

    # Не забываем удалять ненужные изображения
    if os.path.exists(filename):
        os.remove(filename)


def oga2wav(filename):
    # Конвертация формата файлов
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    # Перевод голоса в текст + удаление использованных файлов
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.WavFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    text = recognizer.recognize_google(wav_audio, language='ru')

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    # Скачивание файла, который прислал пользователь
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(content_types=['voice'])
def transcript(message):
    log_2_xlsx(message)
    bot.send_message(message.from_user.id, "Перевод голоса в текст...")
    # Функция, отправляющая текст в ответ на голосовое
    try:

        filename = download_file(bot, message.voice.file_id)
        text = recognize_speech(filename)
        bot.send_message(message.chat.id, text)

    except speech_recognition.exceptions.UnknownValueError as e:
        print(e)
        bot.send_message(message.from_user.id, "Извините, не могу распознать текст 😔\nПовторите, пожалуйста 🙏")


# Запускаем бота. Он будет работать до тех пор, пока работает ячейка (крутится значок слева).
# Остановим ячейку - остановится бот
def get_articles(message):
    try:
        log_2_xlsx(message)
        web_page = requests.get('https://live.skillbox.ru/playlists/code/python/')
        soup = BeautifulSoup(web_page.text, 'html.parser')
        items = soup.find_all(class_='playlist-inner__item')

        # INLINE BUTTONS IN MESSAGE
        articles = []
        ids = []
        for elem in items:
            item = []
            title = elem.find(class_='playlist-inner-card__link-text').text
            relative_url = elem.find(class_='playlist-inner-card__link').attrs['href']
            url = 'https://live.skillbox.ru' + relative_url
            # item.append(title)
            # item.append(url)
            # articles.append(item)
            articles.append(title[:30])
        print(articles)
        kb = Keyboa(articles).keyboard
        bot.send_message(message.from_user.id, "Статьи с сайта https://centersi.spb.ru/art/", reply_markup=kb)

    except Exception:
        print("Exception")


bot.polling()
