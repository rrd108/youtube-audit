import csv
import copy
import os
import youtube
import secrets

apiKey = secrets.apiKey

def main():
    filePath = os.path.abspath(os.path.dirname(__file__)) + '/'

    with open(filePath + 'competitiors.txt') as f:
        urls = f.readlines()

        analytics = []

        for url in urls:
            yt = youtube.Youtube(url)
            
            #print()
            channelId = yt.getChannelId()
            #print(channelId)

            stats = yt.getChannelStats(channelId, apiKey)
            print(stats['channelTitle'])
            
            analytics.append({
                'channel' : stats['channelTitle'],
                'viewCount': stats['statistics']['viewCount'],
                'subscriberCount': stats['statistics']['subscriberCount'],
            })

        tempAnalitycs = copy.deepcopy(analytics)
        firstTime = False
        # subscribers
        with open(filePath + 'analyticsSubscribers.csv', 'r+') as f:
            reader = csv.reader(f)
            data = list(reader)
            
            if (not len(data)):
                # first time running we just put the analytics into the csv
                firstTime = True
                writer = csv.writer(f)
                for row in tempAnalitycs:
                    # remove viewCount
                    row.pop('viewCount')
                    writer.writerow(row.values())


        # we already have some data in the csv file
        if (not firstTime):
            with open(filePath + 'analyticsSubscribers.csv', 'w') as f:
                # TODO this solutions only works if competitiors.txt is in the same order as analyticsSubscribers TODO
                for i, row in enumerate(tempAnalitycs):
                    data[i].append(tempAnalitycs[i]['subscriberCount'])
                
                writer = csv.writer(f)
                writer.writerows(data)
        # ---------- subscribers ends ----------

        tempAnalitycs = copy.deepcopy(analytics)
        firstTime = False
        # views
        with open(filePath + 'analyticsViews.csv', 'r+') as f:
            reader = csv.reader(f)
            data = list(reader)
            
            if (not len(data)):
                # first time running we just put the analytics into the csv
                firstTime = True
                writer = csv.writer(f)
                for row in tempAnalitycs:
                    # remove viewCount
                    row.pop('subscriberCount')
                    writer.writerow(row.values())


        # we already have some data in the csv file
        if (not firstTime):
            with open(filePath + 'analyticsViews.csv', 'w') as f:
                # TODO this solutions only works if competitiors.txt is in the same order as analyticsViews
                for i, row in enumerate(tempAnalitycs):
                    data[i].append(tempAnalitycs[i]['viewCount'])
                
                writer = csv.writer(f)
                writer.writerows(data)
        # ---------- views ends ----------
        

if __name__ == "__main__":
    main()