import tweepy
import csv
from configs import config


auth = tweepy.OAuthHandler(config.apiKey, config.secretKey)
auth.set_access_token(config.token, config.secretToken)

api = tweepy.API(auth)


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


def write_data():
    with open('data/data.csv', mode="w", encoding="utf-8") as twitter_data:
        data_writer = csv.writer(twitter_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(result)


def define_location():
    for tweet in tweepy.Cursor(api.search, q="*", count=5, geocode="60.3652817,5.2890912,50km").items(5):
        print(tweet.created_at, "|", tweet.user.name, "|", tweet.text, "|",
              tweet.place.name if tweet.place else "Undefined place")
        r = tweet.created_at, tweet.user.name, tweet.text, tweet.place.name if tweet.place else "Undefined place"
        result.append(r)
    write_data()


thisStreamListener = CustomStreamListener()
thisStream = tweepy.Stream(auth=api.auth, listener=thisStreamListener)

result = []

define_location()