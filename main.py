import requests
import secret
import functions

# Replace with your Twitch client ID and client secret
client_id = secret.secret['twitch']['clientId']
client_secret = secret.secret['twitch']['clientSecret']
oauth_token = functions.getOauthToken(client_id, client_secret)

# Replace with the name of the Twitch channel you want to download
channels = secret.info['twitch']['channels']
pythonWorkDir = secret.info['system']['pythonWorkDir']

for channel_name in channels:

	if functions.tmuxSessionRunning(f'{channel_name}_dl-session'):
		print(f'Already downloading stream of: {channel_name}')
		quit()

	response = functions.getStreamData(channel_name, oauth_token, client_id)

	# Check if the stream is live
	if response['data']:
		relevantData = { 'channel_name': channel_name, 'user_name': response['data'][0]['user_name'], 'started_at': response['data'][0]['started_at']}
		command = f'python3 {pythonWorkDir}/download.py --data "{relevantData}"'
		functions.runInTmux(f'{channel_name}_dl-session', command)
		print(f'Starting download: {channel_name}')
	else:
		print(f'{channel_name} is Offline..')