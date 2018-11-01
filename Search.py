# coding=utf-8

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
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

# Listener handles incoming tweets from stream, inserts tweets to JSON format
class StdOutListener(StreamListener):
    def on_status(self, status):
        print(status.text)
        # print "Time Stamp: ",status.created_at
        try:
            Coords.update(status.coordinates)
            XY = (Coords.get('coordinates'))  # XY - coordinates
            print("X: ", XY[0])
            print("Y: ", XY[1])
        except:
            # Often times users opt into 'place' which is neighborhood size polygon
            # Calculate center of polygon
            Box = status.place.bounding_box.coordinates[0]
            XY = [(Box[0][0] + Box[2][0]) / 2, (Box[0][1] + Box[2][1]) / 2]

            # print("X: ", XY[0])
            # print("Y: ", XY[1])
            pass

        # Convert datetime object
        status.created_at = status.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Filter out retweets
        if (not status.retweeted) and ('RT @' not in status.text):
            # If there's a user-added location, use it
            if status.user.location is not None:
                tweets['tweets'].append({
                    'tweet': [
                        {
                            'tweet_date': status.created_at,
                            'tweet_text': status.text,
                            'tweet_user_name': status.user.name,
                            'tweet_location': status.user.location,
                        }
                    ]
                })
                dump_json(tweets)
            # If not, then long-lat
            else:
                tweets['tweets'].append({
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


def dump_json(tweet_data):
    with open("data/json_data.json", "w", encoding="utf-8") as write_file:
        json.dump(tweet_data, write_file, indent=4, ensure_ascii=False)
        write_file.close()


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, timeout=30.0)
    # Only records 'locations' OR 'tracks', NOT 'tracks (keywords) with locations'
    while True:
        try:
            # Call tweepy's userstream method
            print("searching..")
            stream.filter(locations=[-126.3,29.2,-72.4,49.2], async=False)  # Approx. bounding box of Bergen
            print("searching")
            # stream.filter(track=['trump'])
            break
        except Exception:
            # Abnormal exit: Reconnect
            nsecs = random.randint(60, 63)
            time.sleep(nsecs)


if __name__ == '__main__':
    main()


geo = [60.1033, 5.0840, 60.3209, 5.4112]

geo2= [5.064945, 60.241243,  5.443305, 60.528346]