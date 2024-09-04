import os
from dotenv import load_dotenv
import tweepy
from kafka import KafkaProducer
import json

# Load environment variables from secrets.env
load_dotenv('secrets.env')

# Access Twitter API credentials from environment variables
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))

# Set up Tweepy authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class TwitterStreamListener(tweepy):
    def on_status(self, status):
        # Convert the status object into a JSON-serializable dictionary
        tweet = {
            'text': status.text,
            'user': status.user.screen_name,
            'created_at': str(status.created_at),
        }
        # Send the tweet to Kafka
        producer.send('data-stream', tweet)
        print(f"Tweet sent to consumer: {tweet['text']}")

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False disconnects the stream
            return False

# Create a stream listener
listener = TwitterStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)

# Filter tweets containing specific keywords (e.g., 'bitcoin', 'crypto')
stream.filter(track=['bitcoin', 'crypto'])

# You can modify the 'track' parameter to monitor different keywords or use 'follow' to track specific users.

