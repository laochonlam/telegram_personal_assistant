# -*- coding: utf-8 -*-

from transitions.extensions import GraphMachine
from googletrans import Translator

from lxml import etree, html
import requests
import json
import urllib.request
import pymysql

# Machine Learning
from keras.applications import InceptionV3
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np

inputShape = (299, 299)
preprocess = preprocess_input
Network = InceptionV3
model = Network(weights="imagenet")

translator = Translator()
db = pymysql.connect("140.116.245.244","laochanlam", "telegram", "chatbot")
cursor = db.cursor()
welcome_word = "What can I help you? \n  /t - translate mode\n  /f - film query mode\n  /n - notes mode\n  /c - image classifcation mode"

class TocMachine(GraphMachine):
    
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    # Translate function Here
    def is_going_to_translation_mode(self, update, bot):
        text = update.message.text
        print("translate detect")
        if (text.lower() == '/translate' or text.lower() == '/t'):
            update.message.reply_text("Translate mode")
            return True

    def on_enter_translation_mode(self, update, bot):
        print('Entering translate mode')
        
    def on_exit_translation_mode(self, update, bot):
        print('Leaving translate mode')

    def on_enter_translating(self, update, bot):
        translate_detect_object = translator.detect(update.message.text)
        if (translate_detect_object.lang.find("zh-CN") != -1) or (translate_detect_object.lang.find("zh-tw") != -1):
            print("find chinese")
            translated_object = translator.translate(
                update.message.text, src="zh-tw", dest="en")
        else:
            print("no find chinese")
            translated_object = translator.translate(
                update.message.text, dest="zh-tw")
        # print(translate_detect_object.lang)
        print(translated_object)
        update.message.reply_text(translated_object.text)
        self.go_back_to_translation_mode(update, bot)

    def on_exit_translating(self, update, bot):
        print('Leaving translating')

    # film query function Here
    def is_going_to_film_query_mode(self, update, bot):
        text = update.message.text
        print("film query detect")
        if (text.lower() == '/filmquery' or text.lower() == '/f'):
            update.message.reply_text("film query mode")
            return True

    def on_enter_film_query_mode(self, update, bot):
        print('Entering film query mode')

    def on_exit_film_query_mode(self, update, bot):
        print('Leaving film query mode')

    def on_enter_film_querying(self, update, bot):
        print("Enter film querying")
        # 台南新光影城
        result = requests.get("http://www.atmovies.com.tw/showtime/t06607/a06/")
        result.encoding = "UTF8"
        root = etree.fromstring(result.content, etree.HTMLParser())
        entry_filmname = update.message.text
        # Get film Title
        for film in root.xpath("//ul[@id=\"theaterShowtimeTable\"]"):
            filmname = film.xpath("./li[@class=\"filmTitle\"]/a/text()")
            if (filmname[0].find(entry_filmname) != -1):
                filmTimetable = film.xpath("./li[position()=2]/ul[position()=2]/li/text()")
                filmTimetable2 = film.xpath("./li[position()=2]/ul[position()=2]/li/a/text()")
                imageurl = film.xpath("./li[position()=2]/ul[position()=1]/li/a/img/@src")
                print(imageurl[0])
                tmp = "電影名稱: %s" % (filmname[0])
                # reply 
                bot.send_photo(chat_id=update.message.chat_id,
                               photo=imageurl[0])
                update.message.reply_text(tmp)
                print(filmTimetable)
                reply_string = ""
                update.message.reply_text("台南新光影城")
                for time in filmTimetable:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                for time in filmTimetable2:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                        
                update.message.reply_text(reply_string)

        # 台南國賓影城
        result = requests.get("http://www.atmovies.com.tw/showtime/t06608/a06/")
        result.encoding = "UTF8"
        root = etree.fromstring(result.content, etree.HTMLParser())
        entry_filmname = update.message.text
        # Get film Title
        for film in root.xpath("//ul[@id=\"theaterShowtimeTable\"]"):
            filmname = film.xpath("./li[@class=\"filmTitle\"]/a/text()")
            if (filmname[0].find(entry_filmname) != -1):
                filmTimetable = film.xpath(
                                    "./li[position()=2]/ul[position()=2]/li/text()")
                filmTimetable2 = film.xpath(
                        "./li[position()=2]/ul[position()=2]/li/a/text()")
                # reply
                print(filmTimetable)
                reply_string = ""
                update.message.reply_text("台南國賓影城")
                for time in filmTimetable:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                for time in filmTimetable2:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                        
                update.message.reply_text(reply_string)

        # 台南大遠百威秀影城
        result = requests.get("http://www.atmovies.com.tw/showtime/t06609/a06/")
        result.encoding = "UTF8"
        root = etree.fromstring(result.content, etree.HTMLParser())
        entry_filmname = update.message.text
        # Get film Title
        for film in root.xpath("//ul[@id=\"theaterShowtimeTable\"]"):
            filmname = film.xpath("./li[@class=\"filmTitle\"]/a/text()")
            if (filmname[0].find(entry_filmname) != -1):
                filmTimetable = film.xpath(
                                    "./li[position()=2]/ul[position()=2]/li/text()")
                filmTimetable2 = film.xpath(
                        "./li[position()=2]/ul[position()=2]/li/a/text()")
                # reply
                print(filmTimetable)
                reply_string = ""
                update.message.reply_text("台南大遠百威秀影城")
                for time in filmTimetable:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                for time in filmTimetable2:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                        
                update.message.reply_text(reply_string)

        # 台南南紡威秀影城
        result = requests.get("http://www.atmovies.com.tw/showtime/t06610/a06/")
        result.encoding = "UTF8"
        root = etree.fromstring(result.content, etree.HTMLParser())
        entry_filmname = update.message.text
        # Get film Title
        for film in root.xpath("//ul[@id=\"theaterShowtimeTable\"]"):
            filmname = film.xpath("./li[@class=\"filmTitle\"]/a/text()")
            if (filmname[0].find(entry_filmname) != -1):
                filmTimetable = film.xpath(
                                    "./li[position()=2]/ul[position()=2]/li/text()")
                filmTimetable2 = film.xpath(
                        "./li[position()=2]/ul[position()=2]/li/a/text()")
                # reply
                print(filmTimetable)
                reply_string = ""
                update.message.reply_text("台南南紡威秀影城")
                for time in filmTimetable:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                for time in filmTimetable2:
                    if (time.find("其他戲院") == -1):
                        reply_string += time + " | "
                update.message.reply_text(reply_string)

        self.go_back_to_film_query_mode(update, bot)

    def on_exit_film_querying(self, update, bot):
        print('Leaving film querying')

    # note function Here
    def is_going_to_notes_mode(self, update, bot):
        text = update.message.text
        print("notes detect")
        if (text.lower() == '/notes' or text.lower() == '/n'):
            update.message.reply_text("notes mode\nyou can write anything here\n\"/p\" to get records in previously 3 days\n\"/b\" to back to user mode.")
            return True

    def on_enter_notes_mode(self, update, bot):
        print('Entering notes mode')

    def on_exit_notes_mode(self, update, bot):
        print('Leaving notes mode')

    def on_enter_notes_jotting(self, update, bot):
        sql = "INSERT INTO notes(data) VALUES ('%s');" % (update.message.text)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        self.go_back_to_notes_mode(update, bot)

    def on_exit_notes_jotting(self, update, bot):
        print('Leaving notes_jotting')

    def on_enter_notes_getting(self, update, bot):
        sql = "SELECT * FROM notes WHERE DATE_ADD(CURRENT_DATE, INTERVAL - 3 DAY)"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for rows in results:
                reply_msg = "%d %s" % (rows[0], rows[1])
                update.message.reply_text(reply_msg)
        except:
            update.message.reply_text("ERROR")
        self.go_back_to_notes_mode(update, bot)

    def on_exit_notes_getting(self, update, bot):
        print('Leaving notes_getting')
    
    def is_getting_notes(self, update, bot):
        text = update.message.text
        print("getting detect")
        return text.lower() == '/pull' or text.lower() == '/p'

    # image_classification function Here
    def is_going_to_image_classification_mode(self, update, bot):
        text = update.message.text
        print("image classification detect")
        if (text.lower() == '/image_classification' or text.lower() == '/c'):
            update.message.reply_text("image classification mode\nyou can send any image to me, then I will predict what it is.")
            return True

    def on_enter_image_classification_mode(self, update, bot):
        print('Entering image classification mode')

    def on_exit_image_classification_mode(self, update, bot):
        print('Leaving image classification mode')

    def on_enter_processing(self, update, bot):
        print(update.message.photo)
        if (update.message.photo):
            rec_image = bot.getFile(update.message.photo.pop().file_id)
            imageurl = rec_image.file_path
            print(imageurl)
            urllib.request.urlretrieve(imageurl, "img/for_predict.jpg")
            img_location = "img/for_predict.jpg"

            # Machine Learning
            image = load_img(img_location, target_size=inputShape)
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess(image)

            predict = model.predict(image)
            P = imagenet_utils.decode_predictions(predict)

            reply_msg = "Umm... I think...\n"
            for (i, (imagenetID, label, prob)) in enumerate(P[0]):
                reply_msg += ("{}. {}: {:.2f}%\n".format(i + 1, label.replace("_", " "), prob * 100))
            reply_msg+= "\nis that right? <3"
            update.message.reply_text(reply_msg)
        else:
            reply_msg = "please send me the photo."
            update.message.reply_text(reply_msg)
        self.go_back_to_image_classification_mode(update, bot)

    def on_exit_processing(self, update, bot):
        print('Leaving processing')


    # General
    def is_going_back_to_user(self, update, bot):
        text = update.message.text
        if  (text.lower() == '/back' or text.lower() == '/b'):
            return True
    def on_enter_user(self, update, bot):
        update.message.reply_text(welcome_word)
        print("user mode")
