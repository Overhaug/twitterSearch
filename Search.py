# coding=utf-8
# Twitter streaming
#

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import random
import json
import time
from configs import config

consumer_key = config.apiKey
consumer_secret = config.secretKey

access_token = config.token
access_token_secret = config.secretToken

Coords = dict()
XY = []
tweets = {
            'tweets': []
        }

keyWordList = list()


# Listener handles incoming tweets from stream, filters and passes data to dict as JSON serializable
class StdOutListener(StreamListener):
    def on_status(self, status):
        try:
            Coords.update(status.coordinates)
            XY = (Coords.get('coordinates'))  # XY - coordinates
        except:
            # If there are no XY coordinates, calculate center of polygon
            box = status.place.bounding_box.coordinates[0]
            XY = [(box[0][0] + box[2][0]) / 2, (box[0][1] + box[2][1]) / 2]
            pass

        # Convert datetime object to string
        status.created_at = status.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Filters only English tweets; filters out retweets, checks if tweet is truncated or not,
        # and checks if tweet contains at least one of the words in BagOfWords list
        # Appends data to global dict tweets, and lastly uses dump_json function to write data to file
        if status.lang == 'en':
            if not status.retweeted:
                if status.truncated:
                    for i in keyWordList[0]:
                        if i in status.extended_tweet['full_text'].lower():
                            tweets['tweets'].append(
                                {
                                    'tweet_id': status.id,
                                    'tweet_date': status.created_at,
                                    'tweet_text': status.extended_tweet['full_text'],
                                    'tweet_user_name': status.user.name,
                                    'tweet_location': XY,
                                }
                            )
                            dump_json(tweets)
                            break
                else:
                    for i in keyWordList[0]:
                        if i in status.text.lower():
                            tweets['tweets'].append(
                                {
                                    'tweet_id': status.id,
                                    'tweet_date': status.created_at,
                                    'tweet_text': status.text,
                                    'tweet_user_name': status.user.name,
                                    'tweet_location': XY,
                                }
                            )
                            dump_json(tweets)
                            break


# dumps dict tweets as json to file
def dump_json(tweet):
    with open('data/json_data.json', 'w', encoding='utf-8') as write_file:
        json.dump(tweet, write_file, indent=2, ensure_ascii=False)
    write_file.close()


# initializes stream, filters on geobox location (4 point coordinate)
def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode="extended", timeout=30.0)
    while True:
        try:
            # Enter (optional) keyword(s) and call tweepy's userstream method
            keyword = input('Optional: Enter keyword(s), separated by single comma and space, i.e: earthquake, '
                            'roadblock. If no keywords, press enter \n -> ')
            keyWordList.append(keyword.split(', '))
            print("searching..")
            stream.filter(locations=[-125.63,24.96,-66.39,49.31], async=False)
            break
        except Exception:
            nsecs = random.randint(60, 63)
            time.sleep(nsecs)


california = [-124.48, 32.53, -114.13, 42.01]


# Starts script
if __name__ == '__main__':
    main()
