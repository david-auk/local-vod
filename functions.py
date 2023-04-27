import subprocess
import os
from datetime import datetime
import secret
import urllib.request
import requests

def checkOrCreateDir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def msg(query):
	telegramToken = secret.telegramSecret['api']
	hostId = secret.telegramSecret['chatId']

	formatedQuote = urllib.parse.quote(query)
	requests.get(f"https://api.telegram.org/bot{telegramToken}/sendMessage?chat_id={hostId}&text={formatedQuote}")


def currentTime():
	now = datetime.now()
	hour = str(now.hour).zfill(2)
	minute = str(now.minute).zfill(2)
	day = str(now.day).zfill(2)
	month = str(now.month).zfill(2)
	year = now.year
	hour_minute = str(hour) + ',' + str(minute)
	formatted_time = '[' + hour_minute + ']-' + str(day) + '-' + str(month) + '-' + str(year)
	return formatted_time

def elapsedTime(start_time_str):
	start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%SZ')
	end_time = datetime.now()
	elapsed_time = end_time - start_time
	elapsed_minutes = int(elapsed_time.total_seconds() // 60)
	return elapsed_minutes

def runInTmux(sessionName, command):
	escapedCommand = command.replace('"', '\\"')
	tmux_command = f'tmux new-session -d -s {sessionName} "{escapedCommand}"'
	subprocess.call(tmux_command, shell=True)

def tmuxSessionRunning(sessionTargetName):
	proc = subprocess.Popen(['tmux', 'list-sessions'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	output = proc.communicate()[0].decode()

	lines = output.splitlines()
	for line in lines:

		sessionName = line.split(':', 1)[0]
		if sessionName == sessionTargetName:
			return True

	return False
