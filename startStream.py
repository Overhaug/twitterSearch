import tweepy
import csv
import json
from configs import config


auth = tweepy.OAuthHandler(config.apiKey, config.secretKey)
auth.set_access_token(config.token, config.secretToken)

api = tweepy.API(auth)

# Dict to store geocodes
GEOCODE = {
    "Bergen": "60.3652817,5.2890912,50km",
}


# inherits from streamListener
# overrides on_status
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # False disconnects the stream
            return False

        # if True, reconnects the stream


# Define search by geocode
def search():
    tweets = []
    for tweet in tweepy.Cursor(api.search, q="*", count=100, geocode=GEOCODE.get("Bergen")).items(100):
        print(tweet.created_at, '|', tweet.text, '|', tweet.user.name, '|', tweet.place if tweet.place else "Undefined"
                                                                                                            " place")
        tweetz = {
                'tweet': [
                    {
                        'tweet_date': str(tweet.created_at),
                        'tweet_text': str(tweet.text),
                        'tweet_user_name': str(tweet.user.name),
                        'tweet_location': str(tweet.user.name),
                    }]
            }

        tweets.append(tweetz)

    return tweets


def dump_json(tweets):
    with open("data/json_data.json", "w") as write_file:
        json.dump(tweets, write_file, indent=4)


thisStreamListener = CustomStreamListener()
thisStream = tweepy.Stream(auth=api.auth, listener=thisStreamListener)

# thisStream.filter(track=['#trump'], async=True)

result = search()

dump_json(result)

# , "|", tweet.user.name, "|", tweet.text, "|",
#              tweet.place.name if tweet.place else "Undefined place"