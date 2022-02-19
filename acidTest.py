import csv
from datetime import date, datetime
import os
import requests
import youtube
import secrets
import sys

apiKey = secrets.apiKey

def main():
    competitiorsFile = sys.argv[1] if len(sys.argv) == 2 else 'competitiors.txt'

    filePath = os.path.abspath(os.path.dirname(__file__)) + '/'

    with open(filePath + competitiorsFile) as f:
        urls = f.readlines()

        analytics = []

        for url in urls:
            yt = youtube.Youtube(url)
            
            channelId = yt.getChannelId()
            #print(channelId)

            stats = yt.getChannelStats(channelId, apiKey)
            # quota 0
            print()
            print(stats['channelTitle'])
            print(stats['statistics'])

            videos = yt.getLast10Videos(channelId, apiKey)

            # get video statistics
            videoStats = []
            currentDate = date.today()

            for video in videos['items']:
                if (video['snippet']['liveBroadcastContent'] != 'upcoming'):
                    # quota 1
                    r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + apiKey)
                    if (r.status_code != 200):
                        print('videoData error: ' + str(r.status_code))
                        print(r.json()['error']['message'])
                        #exit()

                    if (r.status_code == 200):
                        vStats = r.json()

                        videoDate = datetime.strptime(video['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ')

                        videoStats.append({
                            'title': vStats['items'][0]['snippet']['title'],
                            'publishedAt': video['snippet']['publishedAt'],
                            'age' : str((currentDate - videoDate.date()).days),
                            'viewCount': vStats['items'][0]['statistics']['viewCount'],
                            'likeCount': vStats['items'][0]['statistics']['likeCount'],
                        })
            ageOf10thVideo = str(videoStats[9]['age'])
            
            last28DaysViews = str(sum(int(video['viewCount']) for video in videoStats if int(video['age']) <= 28))
            last28DaysLikes = str(sum(int(video['likeCount']) for video in videoStats if int(video['age']) <= 28))
            last28DaysNumberOfVideos = str(len([video for video in videoStats if int(video['age']) <= 28]))
            
            #print(f'Total views of last 10: {last10Views}')
            #print(f'Total likes of last 10: {last10Likes}')
            print(f'Age of 10th video: {ageOf10thVideo}')
            print()

            print(f'Number of videos in the last 28 days: {last28DaysNumberOfVideos}')
            print(f'Total views of last 28 days: {last28DaysViews}')
            print(f'Total likes of last 28 days: {last28DaysLikes}')
            print()
            
            # most popular video views, likes and age
            r = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&key={apiKey}&maxResults=1&order=viewCount&type=video')
            # quota 100
            if (r.status_code != 200):
                print('error: ' + str(r.status_code))
                exit()

            videos = r.json()
            for video in videos['items']:
                # quota 1
                r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + apiKey)
                if (r.status_code != 200):
                    print('error: ' + str(r.status_code))
                    exit()

                vStats = r.json()
                videoDate = datetime.strptime(video['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%SZ')
                likeCount = -1
                if 'likeCount' in vStats['items'][0]['statistics']: 
                    likeCount = vStats['items'][0]['statistics']['likeCount']
                best= {
                    'title': vStats['items'][0]['snippet']['title'],
                    'publishedAt': video['snippet']['publishedAt'],
                    'age' : str((currentDate - videoDate.date()).days),
                    'viewCount': vStats['items'][0]['statistics']['viewCount'],
                    'likeCount': likeCount,
                }

            print(f"Total views of best video: {str(best['viewCount'])}")
            print(f"Total likes of best video: {str(best['likeCount'])}")
            print(f"Age of best video: {str(best['age'])}")

            analytics.append({
                'channel' : stats['channelTitle'],
                'viewCount': stats['statistics']['viewCount'],
                'subscriberCount': stats['statistics']['subscriberCount'],
                'videoCount': stats['statistics']['videoCount'],
                'ageOf10thVideo': ageOf10thVideo,
                'last28DaysNumberOfVideos': last28DaysNumberOfVideos,
                'last28DaysViews': last28DaysViews,
                'last28DaysLikes': last28DaysLikes,
                'bestNumberOfVideos': best['age'],
                'bestViews': best['viewCount'],
                'bestLikes': best['likeCount'],

            })

        print(analytics)    

        keys = analytics[0].keys() 
        outputFile = open('acidTest.csv', 'w')
        dict_writer = csv.DictWriter(outputFile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(analytics)
        outputFile.close()
            
        print()
        print('acidTest.csv is updated')

if __name__ == "__main__":
    main()