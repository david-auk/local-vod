import functions
import secret
import argparse
import time

# Create the parser object
parser = argparse.ArgumentParser(description='A python script to download livestreams')
parser.add_argument('-d', '--data', default={ }, help='Set how long the wait time before next request, default: 0.01')
args = parser.parse_args()

data = args.data
if not data:
	print("add data with the flag -d or --data")
	quit()
else:
	data = eval(data)

# Getting facts
channel_name = data['channel_name']
channelNameClean = data['user_name']
startTime = data['started_at']
downloadDir = secret.info['system']['downloadDir']
oauthSecret = secret.secret['twitch']['oauthSecret']

# File Stuff
functions.checkOrCreateDir(f'{downloadDir}/{channel_name}')
filename = f'\'{downloadDir}/{channel_name}/{functions.currentTime()}.mp4\''

# Notifing Download started
functions.msg(f'Started downloading: {channel_name} {functions.elapsedTime(startTime)} minutes after stream started.')

# Getting the date to calulate runtime
timeBeforeDownload = functions.getCurrentTime()

# Running the command
#command = f'streamlink twitch.tv/{channel_name} best "--http-header=Authorization=OAuth {oauthSecret}" --twitch-disable-ads --stdout | ffmpeg -y -i - -c copy {filename}'
command = f'streamlink twitch.tv/{channel_name} best --twitch-disable-ads --stdout | ffmpeg -y -i - -c copy {filename}'
functions.runCommand(command)

# Calculating Download Time
downloadDuration = functions.elapsedTimeSince(timeBeforeDownload)

time.sleep(30)

# Checking if the stream really finished
client_id = secret.secret['twitch']['clientId']
client_secret = secret.secret['twitch']['clientSecret']
oauth_token = functions.getOauthToken(client_id, client_secret)

response = functions.getStreamData(channel_name, oauth_token, client_id)

# Notifing Download finished
if response['data']:# Downloaded {time} of {channel_name}'s stream
	functions.msg(f'Downloaded {downloadDuration} of {channel_name}\'s stream, but im detecting the stream is still live..')
else:
	functions.msg(f'Finished downloading: {channel_name}, the stream was {downloadDuration} long.')

## PLEX ##

if secret.info['plex']['isAvalible']:
	print("Getting plex facts")
	plexLibraryNumber = functions.getPlexLibraryNumber(secret.info['plex']['plexLibraryName'])

	print(f"Refreshing Library \'{secret.info['plex']['plexLibraryName']}\'")
	functions.refreshPlexLibrary(plexLibraryNumber)



time.sleep(15)