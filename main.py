import requests
import secret
import functions

# Replace with your Twitch client ID and client secret
client_id = secret.secret['twitch']['clientId']
client_secret = secret.secret['twitch']['clientSecret']
oauth_token = functions.getOauthToken(client_id, client_secret)
print(f"\nOAuht Token: {oauth_token}\n\n---")

# Replace with the name of the Twitch channel you want to download
channels = secret.info['twitch']['channels']
pythonWorkDir = secret.info['system']['pythonWorkDir']

for channel_name in channels:

	if functions.tmuxSessionRunning(f'{channel_name}_dl-session'):
		print(f'Already downloading stream of: {channel_name}')
		continue

	response = functions.getStreamData(channel_name, oauth_token, client_id)

	# Check if the stream is live
	if response['data']:
		encodedData = functions.encode(str(response['data']))
		command = f'python3 {pythonWorkDir}/download.py --data "{encodedData}"'
		functions.runInTmux(f'{channel_name}_dl-session', command)
		print(f'Starting download: {channel_name}')
	else:
		print(f'{channel_name} is Offline..')

print('---\n')