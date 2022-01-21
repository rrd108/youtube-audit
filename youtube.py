import requests
import re

class Youtube:

    def __init__(self, url) -> None:
        self.url = url.strip()

    def getChannelId(self):
        # get channel id form url
        # TODO I did not find a better way to get channel id from the known url
        # set conset cookie
        # TODO hardcoded date string
        consetCookie = {'CONSENT' : 'YES+cb.20220111-10-p0.hu+FX+376'}
        
        # get the channel id
        r = requests.get(self.url, cookies=consetCookie)
        if (r.status_code != 200):
            print('error: ' + str(r.status_code))
            exit()

        channelId = re.search('"browseId":"([^"]*)"', r.text).groups()[0]
        return channelId

    def getChannelStats(self, channelId, apiKey):
        r = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=' + channelId + '&key=' + apiKey)
        if (r.status_code != 200):
            print('error: ' + str(r.status_code))
            exit()
            
        stats = r.json()
        return {
            'channelTitle': stats['items'][0]['snippet']['title'],
            'statistics': stats['items'][0]['statistics']
        }

    def getLast10Videos(self, channelId, apiKey):
        # TODO we request here 15 videos, but we should get the last 10 or the last month - what is bigger - if last month had more than 10 vieos the statistics will be wrong
        r = requests.get(f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={channelId}&maxResults=15&key={apiKey}&type=video')
        if (r.status_code != 200):
            print('error: ' + str(r.status_code))
            exit()

        return r.json()