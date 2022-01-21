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