import subprocess
import os
from datetime import datetime, timedelta
import secret
import urllib.request
import requests
import base64

def encode(strToBeEncoded):
	encodedString = base64.b64encode(strToBeEncoded.encode('utf-8')).decode('utf-8')
	
	return encodedString

def decode(strToBeDecoded):
	decodedString = base64.b64decode(strToBeDecoded).decode('utf-8')

	return decodedString

def getPlexLibraryNumber(plexLibraryName):
	user = secret.info['plex']['user']
	host = secret.info['plex']['host']

	cmd = f'ssh {user}@{host} "sudo -u plex /usr/lib/plexmediaserver/Plex\\ Media\\ Scanner --list|grep \"{plexLibraryName}\"|tr -d [:space:]|sed -e \"s/:.*//\""'
	output = subprocess.check_output(cmd, shell=True)
	output = output.decode('utf-8').strip()

	return output

def refreshPlexLibrary(plexLibraryNumber):
	user = secret.info['plex']['user']
	host = secret.info['plex']['host']

	runCommand(f'ssh {user}@{host} "sudo -u plex /usr/lib/plexmediaserver/Plex\\ Media\\ Scanner -srp -c {plexLibraryNumber}" &> /dev/null')

def checkOrCreateDir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def msg(query):
	telegramToken = secret.secret['telegram']['api']
	hostId = secret.secret['telegram']['chatId']

	formatedQuote = urllib.parse.quote(query)
	requests.get(f"https://api.telegram.org/bot{telegramToken}/sendMessage?chat_id={hostId}&text={formatedQuote}")

def formattedDate():
	now = datetime.now()
	hour = str(now.hour).zfill(2)
	minute = str(now.minute).zfill(2)
	day = str(now.day).zfill(2)
	month = str(now.month).zfill(2)
	year = now.year
	hour_minute = str(hour) + ',' + str(minute)
	formatted_time = f'{year}-{month}-{day}-{hour}-{minute}'
	#formatted_time = '[' + hour_minute + ']-' + str(day) + '-' + str(month) + '-' + str(year)
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

def runCommand(command):
	subprocess_obj = subprocess.Popen(command, shell=True)

	# Wait for the subprocess to finish or until a keyboard interrupt occurs
	try:
		subprocess_obj.wait()
	except KeyboardInterrupt:
		subprocess_obj.terminate() # Terminate the subprocess if a keyboard interrupt occurs

def tmuxSessionRunning(sessionTargetName):
	proc = subprocess.Popen(['tmux', 'list-sessions'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	output = proc.communicate()[0].decode()

	lines = output.splitlines()
	for line in lines:

		sessionName = line.split(':', 1)[0]
		if sessionName == sessionTargetName:
			return True

	return False

def getOauthToken(client_id, client_secret):
	# Get an OAuth token
	oauth_url = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
	response = requests.post(oauth_url).json()
	oauth_token = response['access_token']

	return oauth_token

def getStreamData(channel_name, oauth_token, client_id):
	# Get the current stream data
	url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
	headers = {'Client-ID': client_id, 'Authorization': f'Bearer {oauth_token}', 'Accept': 'application/vnd.twitchtv.v5+json'}
	response = requests.get(url, headers=headers).json()

	return response

def getCurrentTime():
	date_format = "%Y-%m-%d %H:%M:%S"
	now = datetime.now()
	date_str = now.strftime(date_format)

	return date_str

def getDayFromDate(date_string):
	date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
	return date_obj.strftime("%A")

def getHourAndMinuteFromDate(date_string):
	date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
	return date_obj.strftime("%H:%M")

def elapsedTimeSince(date_str):
	date_format = "%Y-%m-%d %H:%M:%S"
	now = datetime.now()
	date = datetime.strptime(date_str, date_format)
	time_delta = now - date

	if time_delta.total_seconds() < 60:
		if time_delta.seconds < 2:
			secondsName = 'second'
		else:
			secondsName = 'second'

		return f"{time_delta.seconds} {secondsName}"
	elif time_delta.total_seconds() < 3600:
		minutes = time_delta.seconds // 60
		seconds = time_delta.seconds % 60
		if minutes < 2:
			minutesName = 'minute'
		else:
			minutesName = 'minutes'

		if seconds < 2:
			secondsName = 'second'
		else:
			secondsName = 'seconds'

		return f"{minutes} {minutesName}, {seconds} {secondsName}"

	else:
		hours = time_delta.seconds // 3600
		minutes = (time_delta.seconds // 60) % 60
		if minutes < 2:
			minutesName = 'minute'
		else:
			minutesName = 'minutes'

		if hours < 2:
			hoursName = 'hour'
		else:
			hoursName = 'hours'

		return f"{hours} {hoursName}, {minutes} {minutesName}"
