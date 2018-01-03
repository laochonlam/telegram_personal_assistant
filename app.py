import sys
from io import BytesIO

import telegram
# telegram api
# https://python-telegram-bot.readthedocs.io/en/stable/

from flask import Flask, request, send_file

from fsm import TocMachine
# fsm api
# https://github.com/pytransitions/transitions#transitions


API_TOKEN = '481103945:AAGF-yzyQNX7f-XxPo_yG500j5UWw6ZYLsY'
WEBHOOK_URL = 'https://1ac428a3.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
welcome_word = "What can I help you? \n  /t - translate mode\n  /f - film query mode\n  /n - notes mode\n  /c - image classification mode"

machine = TocMachine(
    states=[
        'user',
        'translation_mode',
        'translating',
        'film_query_mode',
        'film_querying',
        'notes_mode',
        'notes_jotting',
        'notes_getting',
        'image_classification_mode',
        'processing'
    ],
    transitions=[
        # translate function here
        {
            'trigger': 'choose_mode',
            'source': 'user',
            'dest': 'translation_mode',
            'conditions': 'is_going_to_translation_mode'
        },
        {
            'trigger': 'translate',
            'source': 'translation_mode',
            'dest': 'user',
            'conditions': 'is_going_back_to_user'
        },
        {
            'trigger': 'translate',
            'source': 'translation_mode',
            'dest': 'translating',
        },
        {
            'trigger': 'go_back_to_translation_mode',
            'source': 'translating',
            'dest': 'translation_mode'
        },
        # film query function here
        {
            'trigger': 'choose_mode',
            'source': 'user',
            'dest': 'film_query_mode',
            'conditions': 'is_going_to_film_query_mode'
        },
        {
            'trigger': 'film_query',
            'source': 'film_query_mode',
            'dest': 'user',
            'conditions': 'is_going_back_to_user'
        },
        {
            'trigger': 'film_query',
            'source': 'film_query_mode',
            'dest': 'film_querying',
        },
        {
            'trigger': 'go_back_to_film_query_mode',
            'source': 'film_querying',
            'dest': 'film_query_mode'
        },
        # note function here
        {
            'trigger': 'choose_mode',
            'source': 'user',
            'dest': 'notes_mode',
            'conditions': 'is_going_to_notes_mode'
        },
        {
            'trigger': 'action',
            'source': 'notes_mode',
            'dest': 'user',
            'conditions': 'is_going_back_to_user'
        },
        {
            'trigger': 'action',
            'source': 'notes_mode',
            'dest': 'notes_getting',
            'conditions': 'is_getting_notes'
        },
        {
            'trigger': 'action',
            'source': 'notes_mode',
            'dest': 'notes_jotting',
        },
        {
            'trigger': 'go_back_to_notes_mode',
            'source': 'notes_jotting',
            'dest': 'notes_mode'
        },
        {
            'trigger': 'go_back_to_notes_mode',
            'source': 'notes_getting',
            'dest': 'notes_mode'
        },
        # image_classification function here
        {
            'trigger': 'choose_mode',
            'source': 'user',
            'dest': 'image_classification_mode',
            'conditions': 'is_going_to_image_classification_mode'
        },
        {
            'trigger': 'image_classification',
            'source': 'image_classification_mode',
            'dest': 'user',
            'conditions': 'is_going_back_to_user'
        },
        {
            'trigger': 'image_classification',
            'source': 'image_classification_mode',
            'dest': 'processing',
        },
        {
            'trigger': 'go_back_to_image_classification_mode',
            'source': 'processing',
            'dest': 'image_classification_mode'
        },
        # Welcome word
        {
            'trigger': 'choose_mode',
            'source': 'user',
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # print(bot.getFile(update.message.photo.file_id))
    if (machine.is_user()):
        machine.choose_mode(update, bot)
    elif (machine.is_translation_mode()):
        machine.translate(update, bot)
    elif (machine.is_film_query_mode()):
        machine.film_query(update, bot)
    elif (machine.is_notes_mode()):
        machine.action(update, bot)
    elif (machine.is_image_classification_mode()):
        machine.image_classification(update, bot)
        
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
