from flask import Flask
from flask_sslify import SSLify
from flask import request
from flask import jsonify
import config
import requests
import json
import datetime

firstweek = config.FIRSTWEEK
secondweek = config.SECONDWEEK

start_date = datetime.datetime(2021, 8, 30)
app = Flask(__name__)
sslify = SSLify(app)
URL = 'https://api.telegram.org/bot' + config.TOKEN + '/'

def week_is_first(day):
	global start_date
	delta_day = day - start_date
	if (abs(delta_day.days + 1) % 14) <= 7:
		return True
	else:
		return False

def send_message(chat_id, text):
    rURL = URL + 'sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'html'}
    r = requests.post(rURL, data)
    return r.json()

def send_day_data(chat_id, message):
    global firstweek
    global secondweek

    moscow_delta = datetime.timedelta(hours=3, minutes=0)
    if message == '/today':
        day = datetime.datetime.today() + moscow_delta
    elif message == '/tomorrow':
        day = datetime.datetime.today() + datetime.timedelta(days=1) + moscow_delta
    dayofweek = day.isoweekday()

    # send message
    if week_is_first(day):
	    send_message(chat_id, firstweek[dayofweek - 1])
    else:
        send_message(chat_id, secondweek[dayofweek - 1])


def send_week_data(chat_id, message):
    global firstweek
    global secondweek

    moscow_delta = datetime.timedelta(hours=3, minutes=0)
    if message == '/week':
        day = datetime.datetime.today() + moscow_delta
        if week_is_first(day):
            action = '/firstweek'
        else:
	        action = '/secondweek'
    else:
	    action = message

    # and send message
    if action == '/firstweek':
	    for week_day in firstweek:
	        send_message(chat_id, week_day)
    elif action == '/secondweek':
        for week_day in secondweek:
            send_message(chat_id, week_day)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if message == '/today' or message == '/tomorrow':
            send_day_data(chat_id, message)
        elif message == '/week' or message == '/firstweek' or message == '/secondweek':
            send_week_data(chat_id, message)
        elif message == '/start':
            send_message(chat_id, config.WELCOME)

        return jsonify(r)
    else:
        return '<h1><a href = {}>VSTUScheduleBot</a> web page</h1><p>Powered by Flask</p><p><a href = {}>Author page</p>'.format(config.BOT_LINK, config.AUTHOR)


