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
        update.message.reply_text("film query mode entered.")
        return text.lower() == '/filmquery' or text.lower() == '/f'

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
        return text.lower() == '/notes' or text.lower() == '/n'

    def on_enter_notes_mode(self, update, bot):
        print('Entering notes mode')

    def on_exit_notes_mode(self, update, bot):
        print('Leaving notes mode')

    def on_enter_notes_jotting(self, update, bot):
        self.go_back_to_notes_mode(update, bot)

    def on_exit_notes_jotting(self, update, bot):
        print('Leaving notes_jotting')
    
    def is_jotting_notes(self, update, bot):
        text = update.message.text
        print("jotting detect")
        return text.lower() == '/jotting' or text.lower() == '/j'

    def is_getting_notes(self, update, bot):
        text = update.message.text
        print("getting detect")
        return text.lower() == '/getting' or text.lower() == '/g'

    # chat function Here
    # note function Here
    def is_going_to_chat_mode(self, update, bot):
        text = update.message.text
        print("chat detect")
        return text.lower() == '/chat' or text.lower() == '/c'

    def on_enter_chat_mode(self, update, bot):
        print('Entering chat mode')

    def on_exit_chat_mode(self, update, bot):
        print('Leaving chat mode')

    def on_enter_processing(self, update, bot):
        self.go_back_to_chat_mode(update, bot)

    def on_exit_processing(self, update, bot):
        print('Leaving processing')


    # General
    def is_going_back_to_user(self, update, bot):
        text = update.message.text
        return text.lower() == '/back' or text.lower() == '/b'
