import telebot
import config
import datetime
from telebot import types


# create bot
bot = telebot.TeleBot(config.TOKEN)
start_date = datetime.datetime(2021, 8, 30)	
first_week = ['Mon','Tue','Wed','Th','Fr','Sat','Sun']
second_week = ['Mon','Tue','Wed','Th','Fr','Sat','Sun']


##############################
@bot.message_handler(commands = ['start'])
def start_command(message):
	commands_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	commands_keyboard.row('/today', '/tomorrow', '/week')
	commands_keyboard.row('/firstweek', '/secondweek')
	bot.send_message(message.from_user.id, 'Привет, <i>{username}.</i>\n\n\
<b>Список команд:</b>\n\
/today - Расписание на сегодня\n/tomorrow - Расписание на завтра\n/week - Расписание на текущую неделю\n\
/firstweek - Расписание на первую неделю\n/secondweek - Расписание на вторую неделю\
'.format(username = message.from_user.username), parse_mode = 'html', reply_markup = commands_keyboard)

##############################
@bot.message_handler(commands = ['today', 'tomorrow'])
def days_command(message):
	global first_week
	global second_week

	# define a day
	if message.text == '/today':
		day = datetime.datetime.today()
	elif message.text == '/tomorrow':
		day = datetime.datetime.today() + datetime.timedelta(days=1)
	dayofweek = day.isoweekday()

	# send message
	if week_is_first(day):
		bot.send_message(message.from_user.id, first_week[dayofweek - 1], parse_mode = 'html')
	else:
		bot.send_message(message.from_user.id, second_week[dayofweek - 1], parse_mode = 'html')

##############################
@bot.message_handler(commands = ['week', 'firstweek', 'secondweek'])
def weeks_command(message):
	global first_week
	global second_week

	# if command /week we can define it as /firstweek or /secondweek
	if message.text == '/week':
		day = datetime.datetime.today()
		if week_is_first(day):
			action = '/firstweek'
		else:
			action = '/secondweek'
	else:
		action = message.text

	# and send message
	if action == '/firstweek':
		for week_day in first_week:
			bot.send_message(message.from_user.id, week_day, parse_mode = 'html')
	elif action == '/secondweek':
		for week_day in second_week:
			bot.send_message(message.from_user.id, week_day, parse_mode = 'html')

##############################
def week_is_first(day):
	global start_date
	delta_day = day - start_date 
	if ((delta_day.days + 1) % 14) <= 7:
		return True
	else:
		return False

##############################
bot.polling(none_stop = True)