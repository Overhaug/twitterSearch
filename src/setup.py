import tweepy
import sys
import config

sys.path.append("..")

auth = tweepy.OAuthHandler(config.apiKey, config.secretKey)
auth.set_access_token(config.token, config.secretToken)

api = tweepy.API(auth)


# inherits from streamListener
# overrides on_status
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text, status.geo)

    def on_error(self, status_code):
        if status_code == 420:
            # False disconnects the stream
            return False

        # if True, reconnects the stream


thisStreamListener = CustomStreamListener()
thisStream = tweepy.Stream(auth=api.auth, listener=thisStreamListener)

for tweet in tweepy.Cursor(api.search, q="*", count=5, geocode="60.3652817,5.2890912,50km").items(5):
    print(tweet.created_at, "|", tweet.user.name, "|", tweet.text, "|", tweet.place.name if tweet.place else "Undefined place")


