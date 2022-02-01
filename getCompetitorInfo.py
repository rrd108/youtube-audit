import csv
import copy
from datetime import date, datetime
import os
import requests
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
            #print(stats['channelTitle'])
            #print(stats['statistics'])
            
            analytics.append({
                'channel' : stats['channelTitle'],
                'viewCount': stats['statistics']['viewCount'],
                'subscriberCount': stats['statistics']['subscriberCount'],
            })

            videos = yt.getLast10Videos(channelId, apiKey)

            # get video statistics
            videoStats = []
            currentDate = date.today()

            for video in videos['items']:
                if (video['snippet']['liveBroadcastContent'] != 'upcoming'):
                    r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + apiKey)
                    if (r.status_code != 200):
                        print('error: ' + str(r.status_code))
                        exit()

                    stats = r.json()

                    videoDate = datetime.strptime(video['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ')

                    videoStats.append({
                        'title': stats['items'][0]['snippet']['title'],
                        'publishedAt': video['snippet']['publishedAt'],
                        'age' : str((currentDate - videoDate.date()).days),
                        'viewCount': stats['items'][0]['statistics']['viewCount'],
                        'likeCount': stats['items'][0]['statistics']['likeCount'],
                    })
            #print(json.dumps(videoStats, indent=2, sort_keys=True))
            last10Views = str(sum(int(video['viewCount']) for video in videoStats[:10]))
            last10Likes = str(sum(int(video['likeCount']) for video in videoStats[:10]))
            ageOf10thVideo = str(videoStats[9]['age'])
            
            last28DaysViews = str(sum(int(video['viewCount']) for video in videoStats if int(video['age']) <= 28))
            last28DaysLikes = str(sum(int(video['likeCount']) for video in videoStats if int(video['age']) <= 28))
            last28DaysNumberOfVideos = str(len([video for video in videoStats if int(video['age']) <= 28]))
            
            # print(f'Total views of last 10: {last10Views}')
            # print(f'Total likes of last 10: {last10Likes}')
            # print(f'Age of 10th video: {ageOf10thVideo}')
            # print()

            # print(f'Number of videos in the last 28 days: {last28DaysNumberOfVideos}')
            # print(f'Total views of last 28 days: {last28DaysViews}')
            # print(f'Total likes of last 28 days: {last28DaysLikes}')
            # print()
            
            # TODO 5 most popular video views, likes and age
            r = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&key={apiKey}&maxResults=5&order=viewCount&type=video')
            if (r.status_code != 200):
                print('error: ' + str(r.status_code))
                exit()

            videos = r.json()
            besties = []
            for video in videos['items']:
                r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + apiKey)
                if (r.status_code != 200):
                    print('error: ' + str(r.status_code))
                    exit()

                stats = r.json()
                videoDate = datetime.strptime(video['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ')
                likeCount = -1
                if 'likeCount' in stats['items'][0]['statistics']: 
                    likeCount = stats['items'][0]['statistics']['likeCount']
                besties.append({
                    'title': stats['items'][0]['snippet']['title'],
                    'publishedAt': video['snippet']['publishedAt'],
                    'age' : str((currentDate - videoDate.date()).days),
                    'viewCount': stats['items'][0]['statistics']['viewCount'],
                    'likeCount': likeCount,
                })

            # print(f"Total views of best video: {str(besties[0]['viewCount'])}")
            # print(f"Total likes of best video: {str(besties[0]['likeCount'])}")
            # print(f"Age of best video: {str(besties[0]['age'])}")


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
                # TODO this solutions only works if competitiors.txt is in the same order as analyticsSubscribers
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