# -*- coding: utf-8 -*-

from transitions.extensions import GraphMachine
from googletrans import Translator

from lxml import etree, html
import requests
import json
import urllib.request

translator = Translator()

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
        return text.lower() == '/translate' or text.lower() == '/t'

    def on_enter_translation_mode(self, update, bot):
        update.message.reply_text("translation mode entered.")
        print('Entering translate mode')
        
    def on_exit_translation_mode(self, update, bot):
        update.message.reply_text("translation mode exited.")
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
        return text.lower() == 'filmquery' or text.lower() == '/f'

    def on_enter_film_query_mode(self, update, bot):
        update.message.reply_text("film query mode entered.")
        print('Entering film query mode')

    def on_exit_film_query_mode(self, update, bot):
        update.message.reply_text("film query mode exited.")
        print('Leaving film query mode')

    def on_enter_film_querying(self, update, bot):
        print("Enter film querying")
        result = requests.get("http://www.atmovies.com.tw/showtime/t06607/a06/")
        result.encoding = "UTF8"
        root = etree.fromstring(result.content, etree.HTMLParser())
        entry_filmname = update.message.text
        # Get film Title
        for film in root.xpath("//ul[@id=\"theaterShowtimeTable\"]"):
            filmname = film.xpath("./li[@class=\"filmTitle\"]/a/text()")
            if (filmname[0].find(entry_filmname) != -1):
                filmTimetable = film.xpath("./li[position()=2]/ul[position()=2]/li/text()")
                imageurl = film.xpath("./li[position()=2]/ul[position()=1]/li/a/img/@src")
                print(imageurl[0])
                tmp = "電影名稱: %s" % (filmname[0])
                # reply 
                bot.send_photo(chat_id=update.message.chat_id,
                               photo=imageurl[0])
                update.message.reply_text(tmp)
                for time in filmTimetable:
                    update.message.reply_text(time)

        self.go_back_to_film_query_mode(update, bot)

    def on_exit_film_querying(self, update, bot):
        print('Leaving film querying')

    # General
    def is_going_back_to_user(self, update, bot):
        text = update.message.text
        return text.lower() == '/back' or text.lower() == '/b'
