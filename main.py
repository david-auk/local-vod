import requests
import secret
import functions

# Replace with your Twitch client ID and client secret
client_id = secret.twitchSecret['clientId']
client_secret = secret.twitchSecret['clientSecret']
downloadDir = secret.generalInfo['downloadDir']
oauthSecret = secret.twitchSecret['oauthSecret']

# Replace with the name of the Twitch channel you want to download
channels = secret.twitchInfo['channels']

for channel_name in channels:

	if functions.tmuxSessionRunning(f'{channel_name}_dl-session'):
		print(f'Already downloading stream of: {channel_name}')
		quit()

	# Get an OAuth token
	oauth_url = f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
	response = requests.post(oauth_url).json()
	oauth_token = response['access_token']

	# Get the current stream data
	url = f'https://api.twitch.tv/helix/streams?user_login={channel_name}'
	headers = {'Client-ID': client_id, 'Authorization': f'Bearer {oauth_token}', 'Accept': 'application/vnd.twitchtv.v5+json'}
	response = requests.get(url, headers=headers).json()

	# Check if the stream is live
	if response['data']:

		# Getting facts
		channelNameClean = response['data'][0]['user_name']
		startTime = response['data'][0]['started_at']

		print(f'Starting download: {channel_name} {functions.elapsedTime(startTime)} minutes after stream started.')
		
		functions.checkOrCreateDir(f'{downloadDir}/{channel_name}')

		filename = f'\'{downloadDir}/{channel_name}/{functions.currentTime()}.mp4\''#.replace("*", ",")
		command = f'streamlink twitch.tv/{channel_name} best "--http-header=Authorization=OAuth {oauthSecret}" --twitch-disable-ads --stdout | ffmpeg -y -i - -c copy {filename}'
		functions.runInTmux(f'{channel_name}_dl-session', command)
	else:
		print(f'{channel_name} is Offline..')