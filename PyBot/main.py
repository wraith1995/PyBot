import json
import logging
import urllib
import urllib2
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from flask import Flask, jsonify, request, Response
import code

TOKEN= '50177117:AAGCMNPVi73DLAf-1hOnx6T247hfwG0hReM'
BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

app = Flask(__name__)

global_code_dict = dict()

@app.route('/me')
def display_me():
    urlfetch.set_default_fetch_deadline(60)
    return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe')))

@app.route('/setwh')
def set_webhook():
    urlfetch.set_default_fetch_deadline(60)
    return json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': "https://pybot-1023.appspot.com/webhook"}))))



@app.route('/webhook', methods=["PUT", "POST"])
def wh():
    
    urlfetch.set_default_fetch_deadline(60)
    r = request.get_json()
    logging.info("raw request:")
    logging.info(r)
    body = r
    #get items:
    update_id = body['update_id']
    message = body['message']
    message_id = message.get('message_id')
    date = message.get('date')
    text = message.get('text')
    fr = message.get('from')
    chat = message['chat']
    chat_id = chat['id']
    #let's do some analysis:

    def give_response(chat_id, text, message_id):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': text.encode('utf-8'),
                'disable_web_page_preview': 'true',
                'reply_to_message_id': str(message_id),
            })).read()
        

    
    if chat_id not in global_code_dict.keys():
        global_code_dict[chat_id] = code.InteractiveInterpreter()
        global_code_dict[chat_id].runcode("import sys")
        global_code_dict[chat_id].runcode("sys.stdout = open('{}', 'w+')".format(str(chat_id) + "stdout"))
        global_code_dict[chat_id].runcode("sys.stderr = open('{}', 'w+')".format(str(chat_id) + "stderr"))
        
    if text[0] == '/':
        if text == '/start':
            give_response(chat_id, "Ready. Please input command. Type /clear to clear enviro", message_id)
        elif text == '/clear':
            del global_code_dict[chat_id]
        else:
            give_response(chat_id, "Action not allowed, ass", message_id)
    elif 'import os' in text:
        give_response(chat_id, "Ass!", message_id)
    elif 'sys.' in text:
        give_response(chat_id, "Ass!", message_id)
    elif 'from os' in text:
        give_response(chat_id, "Ass!", message_id)
    elif 'from sys' in text:
        give_response(chat_id, "Ass!", message_id)
    elif 'import sys' in text:
        give_response(chat_id, "Ass!", message_id)
    else:
        global_code_dict[chat_id].runcode(text)
        global_code_dict[chat_id].runcode("sys.stdout.close()")
        global_code_dict[chat_id].runcode("sys.stderr.close()")
        out = open("{}".format(str(chat_id) + "stdout"), 'w+')
        err = open("{}".format(str(chat_id) + "stderr"), 'w+')
        cmd_res = out.read() + err.read()
        out.seek(0)
        err.seek(0)
        out.truncate()
        err.truncate()
        out.close()
        err.close()
        give_response(chat_id, cmd_res, message_id)
        
    

    resp = Response(r, status=200, mimetype='application/json')
    return resp
    


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
