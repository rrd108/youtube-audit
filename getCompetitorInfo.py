from datetime import date, datetime
import requests

import youtube

api_key = 'AIzaSyBI_T8eLqhIyTjH8EmGMS1olAsJZGAVX4c'

def main():
    with open('competitiors.txt') as f:
        urls = f.readlines()

        for url in urls:
            yt = youtube.Youtube(url)
            print()
            channelId = yt.getChannelId()
            print(channelId)

            # get channel main statistics
            r = requests.get('https://youtube.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=' + channelId + '&key=' + api_key)
            stats = r.json()
            print(stats['items'][0]['snippet']['title'])
            print(stats['items'][0]['statistics'])

            # get last 10 video ids
            # TODO we request here 15 videos, but we should get the last 10 or the last month - what is bigger - if last month had more than 10 vieos the statistics will be wrong
            r = requests.get(f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={channelId}&maxResults=15&key={api_key}&type=video')
            if (r.status_code != 200):
                print('error: ' + str(r.status_code))
                exit()

            videos = r.json()
            #print(json.dumps(videos, indent=2, sort_keys=True))

            # get video statistics
            videoStats = []
            currentDate = date.today()

            for video in videos['items']:
                if (video['snippet']['liveBroadcastContent'] != 'upcoming'):
                    r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + api_key)
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
            
            print(f'Total views of last 10: {last10Views}')
            print(f'Total likes of last 10: {last10Likes}')
            print(f'Age of 10th video: {ageOf10thVideo}')
            print()

            print(f'Number of videos in the last 28 days: {last28DaysNumberOfVideos}')
            print(f'Total views of last 28 days: {last28DaysViews}')
            print(f'Total likes of last 28 days: {last28DaysLikes}')
            print()
            
            # TODO 5 most popular video views, likes and age
            r = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&key={api_key}&maxResults=5&order=viewCount&type=video')
            if (r.status_code != 200):
                print('error: ' + str(r.status_code))
                exit()

            videos = r.json()
            besties = []
            for video in videos['items']:
                r = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=' + video['id']['videoId'] + '&key=' + api_key)
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
            #print(json.dumps(besties, indent=2, sort_keys=True))
            print(f"Total views of best video: {str(besties[0]['viewCount'])}")
            print(f"Total likes of best video: {str(besties[0]['likeCount'])}")
            print(f"Age of best video: {str(besties[0]['age'])}")
            #exit()

if __name__ == "__main__":
    main()