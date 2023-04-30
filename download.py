import functions
import secret
import argparse
import time
import requests

from plexapi.server import PlexServer

# Create the parser object
parser = argparse.ArgumentParser(description='A python script to download livestreams')
parser.add_argument('-d', '--data', default='', help='Set how long the wait time before next request, default: 0.01')
args = parser.parse_args()

data = args.data
if not data:
	print("add data with the flag -d or --data")
	quit()
else:
	data = eval(functions.decode(data))[0]

### <Getting facts> ###

# Channel info
channelNameUrl = data['user_login']
channelNameClean = data['user_name']

# Stream info
streamTitle = data['title']
streamGameName = data['game_name']
#streamStartTime = data['started_at']
streamLanguage = data['language']
streamThumbnailUrl = data['thumbnail_url']

# File info
downloadDir = secret.info['system']['downloadDir']
functions.checkOrCreateDir(f'{downloadDir}/{channelNameUrl}')
filename = f'\'{downloadDir}/{channelNameUrl}/{functions.currentTime()}.mp4\''

### </Getting facts> ###

# Getting the date to calulate runtime
timeBeforeDownload = functions.getCurrentTime()

# Running the command
#command = f'streamlink twitch.tv/{channelNameUrl} best "--http-header=Authorization=OAuth {oauthSecret}" --twitch-disable-ads --stdout | ffmpeg -y -i - -c copy {filename}'
command = f'streamlink twitch.tv/{channelNameUrl} best --twitch-disable-ads --stdout | ffmpeg -y -i - -c copy {filename}'
functions.runCommand(command)

# Calculating Download Time
downloadDuration = functions.elapsedTimeSince(timeBeforeDownload)

# Checking if the stream really finished
client_id = secret.secret['twitch']['clientId']
client_secret = secret.secret['twitch']['clientSecret']
oauth_token = functions.getOauthToken(client_id, client_secret)

response = functions.getStreamData(channelNameUrl, oauth_token, client_id)

# Notifing Download finished
if response['data']:# Downloaded {time} of {channel_name}'s stream
	functions.msg(f'Downloaded {downloadDuration} of {channelNameUrl}\'s stream, but im detecting the stream is still live..')
else:
	functions.msg(f'Finished downloading: {channelNameClean}, the stream was {downloadDuration} long.')

## PLEX ##

if secret.info['plex']['isAvalible']:
	print("Getting plex facts")
	plexLibraryNumber = functions.getPlexLibraryNumber(secret.info['plex']['plexLibraryName'])

	print(f"Refreshing Library \'{secret.info['plex']['plexLibraryName']}\'")
	functions.refreshPlexLibrary(plexLibraryNumber)

	# Set the URL and authentication token for your Plex server
	url = f"http://{secret.info['plex']['host']}:32400/library/sections/{plexLibraryNumber}/all"
	plexToken = secret.info['plex']['plexToken']

	plex = PlexServer(f"http://{secret.info['plex']['host']}:32400", plexToken)

	# Make the request and parse the response as JSON
	response = requests.get(url, headers={"Accept": "application/json", "X-Plex-Token": plexToken}).json()

	for item in data["MediaContainer"]["Metadata"]:
		# Channel
		if item["title"].lower().replace(' ', '') == channelNameUrl or item["title"].lower().replace(' ', '_') == channelNameUrl:
			channelResponse = requests.get(f"http://incus:32400{item['key']}", headers={"Accept": "application/json", "X-Plex-Token": plexToken})
			response = json.loads(channelResponse.text)
			# SEASON
			for episode in response["MediaContainer"]["Metadata"]:
				print(f"Season: {episode['title']}")
				print(f"ratingKey: {episode['ratingKey']}")
				seasonResponse = requests.get(f'http://incus:32400/library/metadata/{episode["ratingKey"]}/children', headers={"Accept": "application/json", "X-Plex-Token": plexToken}).json()
				# EPISODE
				for episode in seasonResponse['MediaContainer']['Metadata']:
					for media in episode['Media']:
						for part in media['Part']:
							if filename.split('/')[-1] == part['file'].split('/')[-1]: # If out of all the episodes in season the filenames match
								episodeRatingKey = episode['ratingKey']
								episode = plex.fetchItem(f'/library/metadata/{episodeRatingKey}')
								episode.batchEdits()
								episode.editTitle(streamTitle).editSummary(f'On Sunday 11:20 {channelNameClean} went live to stream: {streamGameName}').editTagline(streamLanguage)
								episode.saveEdits()

time.sleep(15)