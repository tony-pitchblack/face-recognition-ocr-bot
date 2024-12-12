# -*- coding: utf-8 -*-
import datetime
import html
import os
import subprocess
import time
import traceback

import cv2
import numpy as np
import pymorphy2
import pytesseract
import telebot
from PIL import Image

from core.color_recognition import color_recognition
from core.config import Config
from core.database.operations import DataBase
from core.keywords import check_symbols
from core.keywords import exclude_words_up
from core.keywords import find_keywords
from core.keywords import keywords_up
from core.levenshtein import levenshtein_distance

from pathlib import Path

# CONFIGS_DIR = r'D:\UserProfile\yosifovaae\scripts\face_recognition\configs\'
CONFIGS_DIR = Path('./configs')

db = DataBase()
config = Config()

bot = telebot.TeleBot(config.bot_token)

pytesseract.pytesseract.tesseract_cmd = r'D:\UserProfile\yosifovaae\scripts\ocr\tesseract\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'D:\UserProfile\yosifovaae\scripts\ocr\tesseract\tessdata'


def text_recognition():
    """
    Эта функция получает и покадрово обрабатывает видеопоток, в случае распознавания в бегущей строке ключевых слов
    отправляет сообщение с текстом и другими параматерами строки в телеграм-канал
    :return: нет
    """
    keywords = keywords_up
    exclude_words = exclude_words_up

    morph = pymorphy2.MorphAnalyzer()

    # Получение доступа к видеопотоку прямого эфира
    with open(CONFIGS_DIR / 'news_url.txt', 'r') as f:
        news_url = f.read().strip()

    ffmpeg_cmd = ['ffmpeg', '-i', news_url, '-f', 'image2pipe', '-pix_fmt', 'rgb24', '-vf',
                  'scale=1280:720,setsar=1', '-vcodec', 'rawvideo', '-']
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    frame_count = 0

    while True:
        frame_bytes = ffmpeg_process.stdout.read(1280 * 720 * 3)
        frame_count += 1
        frame_np = np.frombuffer(frame_bytes, np.uint8)
        if np.all(frame_np == 0):
            return

        frame = frame_np.reshape((720, 1280, 3))
        if frame_count % 30 != 0:  # Обрабатываем только каждый 30-й кадр
            continue

        # Выход из цикла, если время работы не пришло (7:00) или окончено (24:00)
        current_time = datetime.datetime.now().time()
        if current_time < datetime.time(hour=7) or current_time > datetime.time(hour=23, minute=59):
            break

        # Обрезка кадра для подачи в модель и отдельно для отправки в телеграм-канал
        frame_cut1 = frame[10 * frame.shape[0] // 11:frame.shape[0], 1 * frame.shape[1] // 19:frame.shape[1], :] # was 15 not 18
        frame_cut2 = frame[10 * frame.shape[0] // 11:frame.shape[0], 3 * frame.shape[1] // 13:frame.shape[1], :]
        frame_cut3 = frame_cut2[1 * frame_cut2.shape[0] // 2:frame_cut2.shape[0], 3 * frame_cut2.shape[1] // 13:frame_cut2.shape[1], :]


        color = color_recognition(frame_cut3)
        # if frame_count % 50 == 0:
        #     image_check = Image.fromarray(frame_cut3)
        #     datetime_now = datetime.datetime.now()
        #     image_name = datetime_now.strftime('%d-%m-%Y %H_%M_%S')
        #     filename = f'frames/image_{color}_{image_name}.jpg'
        #     image_check.save(filename)
        #     print("color", color)
        #     print("image_name", image_name)
        #     # if color == "Неизвестный цвет":
        #     #     continue

        # Преобразование фрейма в черно-белый и распознавание моделью
        frame_uncol = cv2.cvtColor(frame_cut2, cv2.COLOR_BGR2GRAY)
        # print(frame_uncol)
        result = pytesseract.image_to_string(frame_uncol, lang='rus').strip().strip("./;").upper()

        if check_symbols(result):
            continue

        # Применение лемматизации к результату
        result_lemmatized = ' '.join([morph.parse(word)[0].normal_form.upper() for word in result.split()])
        print(f"Строка лем-я: {result_lemmatized}")
        print(f"Строка: {result}")

        # Проверка наличия ключевых слов в бегущей строке
        match_raw = find_keywords(keywords, result, exclude_words)
        match_lemm = find_keywords(keywords, result_lemmatized, exclude_words)
        print(f"КС в обычной и лем-й строках: {match_raw} {match_lemm}")

        if match_raw or match_lemm:
            if match_raw:
                keyword = match_raw
            if match_lemm:
                keyword = match_lemm

            datetime_now = datetime.datetime.now()
            image_name = datetime_now.strftime('%d-%m-%Y %H_%M_%S')

            # Сохранение изображения с динамически сгенерированным именем файла
            image = Image.fromarray(frame_cut1)
            filename = f'recognitions/image_{image_name}_{color}.jpg'
            # keyword = match_raw if match_raw else match_lemm
            print(f'Обнаружено ключевое слово: {keyword}')

            # Формирование сообщения с выделением ключевого слова жирным шрифтом
            result_message = result.replace(keyword, f'<b>{html.escape(keyword)}</b>')
            # result_message = result.replace(keyword, f'<b>{keyword}</b>')
            message = f"{result_message}\n\n"

            if color == "Белый":
                if datetime_now.time().hour < 15:
                    date_filter = datetime_now.replace(hour=7, minute=0, second=0, microsecond=0)
                elif 15 <= datetime_now.time().hour < 21:
                    date_filter = datetime_now.replace(hour=15, minute=0, second=0, microsecond=0)
                else:
                    date_filter = datetime_now.replace(hour=21, minute=0, second=0, microsecond=0)
            else:
                date_filter = datetime.datetime.now() - datetime.timedelta(hours=1)

            # Порог сходства для определения дубликатов
            threshold = 0.9

            # Проверка нечетких дубликатов. Получение существующих текстов из БД
            existing_texts = db.get_existing_texts(date_filter)
            is_duplicate = False
            print("Нечеткие дубли: ", existing_texts)
            for text in existing_texts:
                similarity = levenshtein_distance(result, text)
                print(similarity)
                if similarity >= threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                image.save(filename)
                bot.send_photo(chat_id=config.chat_id_ocr, photo=image, caption=message, parse_mode='HTML')
                db.insert_data(table='running_lines', image_path=filename, key_word=keyword,
                               text=result, datetime=datetime_now, line_color=color)
                print('В БД такой строки нет!')
            else:
                print('В БД уже есть похожая строка!')

            time.sleep(5)


try:
    while True:
        # Получение доступа к видеопотоку прямого эфира
        with open(r'D:\UserProfile\yosifovaae\scripts\face_recognition\configs\news_url.txt', 'r') as f:
            news_url = f.read().strip()
        text_recognition()

        # Выход из цикла, если время работы не пришло (7:00) или окончено (24:00)
        current_time = datetime.datetime.now().time()
        if current_time < datetime.time(hour=7) or current_time > datetime.time(hour=23, minute=59):
            break

except Exception as e:
    error = traceback.format_exc(limit=3)
    escaped_message = html.escape(error)
    text = f"<b>OCR бегущие строки</b> (<a href='tg://user?id=1710562566'>Anna</a>)\nСистема отключена!\n"
    bot.send_message(chat_id=config.chat_id_error, text=f"{text}\n\n{escaped_message}", parse_mode='html')
