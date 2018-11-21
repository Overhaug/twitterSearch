# coding=utf-8

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

BagOfWords = ['earthquake', 'help', 'richter scale', 'magnitude']


# Listener handles incoming tweets from stream, passes JSON objects to dict
class StdOutListener(StreamListener):
    def on_status(self, status):
        try:
            Coords.update(status.coordinates)
            XY = (Coords.get('coordinates'))  # XY - coordinates
        except:
            # Often times users opt into 'place' which is neighborhood size polygon
            # Calculate center of polygon
            Box = status.place.bounding_box.coordinates[0]
            XY = [(Box[0][0] + Box[2][0]) / 2, (Box[0][1] + Box[2][1]) / 2]
            pass

        # Convert datetime object to string
        status.created_at = status.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Filter out retweets

        if status.lang == 'en':
            if not status.retweeted:
                if status.truncated:
                    for i in BagOfWords:
                        if i in status.extended_tweet['full_text'].lower():
                            tweets['tweets'].append({
                                'tweet_id': status.id,
                                'tweet': [
                                    {
                                        'tweet_date': status.created_at,
                                        'tweet_text': status.extended_tweet['full_text'],
                                        'tweet_user_name': status.user.name,
                                        'tweet_location': XY,
                                    }
                                ]
                            })
                            dump_json(tweets)
                else:
                    for i in BagOfWords:
                        if i in status.text.lower():
                            tweets['tweets'].append({
                                'tweet_id': status.id,
                                'tweet': [
                                    {
                                        'tweet_date': status.created_at,
                                        'tweet_text': status.text,
                                        'tweet_user_name': status.user.name,
                                        'tweet_location': XY,
                                    }
                                ]
                            })
                            dump_json(tweets)

        # if status.truncated:
        #     print('truncated')
        #     if 'help' in str(status.text):
        #             if status.lang == 'en':
        #                 if not status.retweeted:
        #                     if status.truncated:
        #                         tweets['tweets'].append({
        #                             'tweet_id': status.id,
        #                             'tweet': [
        #                                 {
        #                                     'tweet_date': status.created_at,
        #                                     'tweet_text': status.extended_tweet['full_text'],
        #                                     'tweet_user_name': status.user.name,
        #                                     'tweet_location': XY,
        #                                 }
        #                             ]
        #                         })
        #                         dump_json(tweets)
        #                     else:
        #                         tweets['tweets'].append({
        #                             'tweet_id': status.id,
        #                             'tweet': [
        #                                 {
        #                                     'tweet_date': status.created_at,
        #                                     'tweet_text': status.text,
        #                                     'tweet_user_name': status.user.name,
        #                                     'tweet_location': XY,
        #                                 }
        #                             ]
        #                         })
        #                         dump_json(tweets)


def dump_json(tweet):
    with open('data/json_data.json', 'w+', encoding='utf-8') as write_file:
        json.dump(tweet, write_file, indent=2, ensure_ascii=False)
        write_file.close()


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode="extended", timeout=30.0)
    while True:
        try:
            # Call tweepy's userstream method
            print("searching..")
            stream.filter(locations=[-125.6, 31.2, -64.4, 49.3], async=False)
            break
        except Exception:
            # Abnormal exit: Reconnect
            nsecs = random.randint(60, 63)
            time.sleep(nsecs)


bergen = [60.1033, 5.0840, 60.3209, 5.4112]

california = [-124.48, 32.53, -114.13, 42.01]

usa = [-125.6, 31.2, -64.4, 49.3]

norway = [4.58, 57.85, 12.75, 64.34]


#def exit_handler():
#    with open("data/json_data.json", "w", encoding="utf-8") as write_file:
#        json.dump(tweets, write_file, indent=4, ensure_ascii=False)
#        write_file.close()


# atexit.register(exit_handler)


if __name__ == '__main__':
    main()
