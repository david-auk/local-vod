## Instalation

### Requirements

Install required system packages: '**streamlabs**', '**ffmpeg**', '**tmux**'

Install required pip packages w/ `pip3 install -r requirements.txt`

### secret.py
Create a custom python file in the project called "secret.py"
> This is requred

##### Format: 'secret.py'

```python
secret = {
	'twitch': {
		'clientId': 'KEY',
		'clientSecret': 'KEY',
		'oauthSecret': 'KEY'
	},
	'telegram': {
		'api': 'KEY',
		'chatId': 'KEY'
	}
}

info = {
	'system': {
		'downloadDir': '/your/VOD/destination/',
		'pythonWorkDir': '/cloned/repo/path/'
	},
	'twitch': {
		'channels': [ 'channel1', 'channel2' ]
	},
	'plex': {
		'isAvalible': True,
		'host': 'hostAdress',
		'user': 'userName',
		'plexLibraryName': 'LibraryName',
		'plexToken': 'KEY'
	}
}
```
#### Acquiring secrets: Twitch
**clientId**

1. Go to your [Twitch Dev Console](https://dev.twitch.tv/console) and authenticate.
2. Go to [Register Your Application](https://dev.twitch.tv/console/apps/create) and create a simple application.
3. Now press the **Manage** button on your new application and copy the `Client ID` to replace 'KEY' in **secret.py**.

**clientSecret**

1. Press the **Manage** button on your new application.
2. Press the **New Secret** button in your new application.
3. Copy the `Client Secret` to replace 'KEY' in **secret.py**.

**oauthSecret**

1. Navigate to [Twitch.tv](https://twitch.tv) with a browser that is logged in.
2. Open the **web inspector** and navigate to the **console tab**.
3. At the botom you see a input bar, press it.
4. Paste the following command in the prompt:
	
```JavaScript
document.cookie.split("; ").find(item=>item.startsWith("auth-token="))?.split("=")[1]
```

5. Copy this result to replace 'KEY' in **secret.py**.

#### Acquiring secrets: Telegram
**api**

1. In telegram, open a chat with [BotFather](https://telegram.me/botfather).
2. Type **/newbot** and follow the instructions.
3. Copy the long `API` token and replace the 'KEY' in **secret.py**.

**chatId**

1. In telegram, start a chat with [ChatID-Bot](https://telegram.me/cid_bot).
2. Copy the numeric `ChatID` and replace the 'KEY' in **secret.py**.

> If this method doesn't work anymore you can try other methods to aquire your ChatID, it is account bound
#### Acquiring secrets: Plex
**plexToken**

1. Go to any of your content in plex.
2. Click the three dots at the bottom right.
3. Press 'Get Info'
4. Click on the 'View XML' button at the bottom left of the page.
5. In the last part of the url you will see `&X-Plex-Token=KEY`.
6. Copy this 'KEY' value in **secret.py**

## Use

`python3 main.py`
