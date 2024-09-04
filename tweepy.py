import os
from dotenv import load_dotenv
import tweepy


bearer_token = ""
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

# client = tweepy.Client(bearer_token)
client = tweepy.Client(consumer_key)

# Get Recent Tweets Count

# This endpoint/method returns count of Tweets from the last seven days that
# match a search query

query = "Tweepy -is:retweet"

# Granularity is what you want the timeseries count data to be grouped by
# You can request minute, hour, or day granularity
# The default granularity, if not specified is hour
response = client.get_recent_tweets_count(query, granularity="day")

for count in response.data:
    print(count)
