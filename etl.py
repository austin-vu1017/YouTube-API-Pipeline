from sqlalchemy import create_engine
from pyspark.sql import SparkSession
from google.oauth2 import service_account
import os, pandas as pd, googleapiclient.discovery, googleapiclient.errors

DEVELOPER_KEY="AIzaSyAru82hLkwVztVx2xCJIdIzy-rKDMhUeyg"

def startup() -> service_account.Credentials:
    # service account credentials
    creds = service_account.Credentials.from_service_account_info(
        info=DEVELOPER_KEY,
        scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )
    
    return creds

def load_etl(creds : service_account.Credentials):
    api_service_name = "Youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)
        
    # create and run the query
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="US"
        )
    r = request.execute()
    transform_etl(r)

def transform_etl(response):
# storing popular video's metadata in dictionary
    popular_videos = {
        'id':[],
        'published_date':[],
        'title':[],
        'description':[],
        'thumbnail':[],
        'channel_name':[],
        'tags': [],
        'duration': [],
        'views': [],
        'likes': [],
        'favorites': [],
        'comments': [],
    }
    
    for item in response['items']:
        duration = response['items'][0]['contentDetails']['duration']
        views = response['items'][0]['statistics']['viewCount']
        likes = response['items'][0]['statistics']['likeCount']
        favorites = response['items'][0]['statistics']['favoriteCount']
        comments = response['items'][0]['statistics']['commentCount']
        video_id = response.id
        popular_videos['duration'].append(duration)
        popular_videos['views'].append(views)
        popular_videos['likes'].append(likes)
        popular_videos['favorites'].append(favorites)
        popular_videos['comments'].append(comments)
    
    
    pd.DataFrame(data=response).to_csv("popular_videos.csv", index=False)
    
def execute_etl():
    # Initialize spark session for youtube API
    spark = SparkSession.builder.appName("Youtube_API_ETL").getOrCreate()

    credentials = startup()
    load_etl(credentials)
    
if __name__ == '__main__':
    execute_etl()