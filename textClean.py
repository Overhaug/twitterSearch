# https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/
import numpy as np
import pandas as pd
import nltk
import json
from pandas.io.json import json_normalize

file = "data/json_data.json"
df = pd.read_json(file, orient='columns')

df.columns
df.head(10)
texts = df["tweet_text"].head(10)
texts.head(10)

from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
joinedTweets = ''.join(texts)
tknzr.tokenize(joinedTweets)

# Create count numbers of hastags used in each tweet.
df['hastags'] = df['tweet_text'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
df[['tweet_text','hastags']].head()
df['hastags'].max()
df["hastags"]



#_____________ TextCleaning__________________
# Convert to lowercase
df['tweet_text'] = df['tweet_text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['tweet_text'].head()

# Remove punctuation
df['tweet_text'] = df['tweet_text'].str.replace('[^\w\s]','')
df['tweet_text'].head()

# Remove stopwords
#from nltk.corpus import stopwords
#stop = stopwords.words('english')
#train['tweet'] = train['tweet'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
#train['tweet'].head()

# Remove common words
freq = pd.Series(' '.join(df['tweet_text']).split()).value_counts()[:10]

# Remove rare words
freq = pd.Series(' '.join(df['tweet_text']).split()).value_counts()[-10:]
freq

# Library to combine words that are not spelled correct.
from textblob import TextBlob
df['tweet_text'][:5].apply(lambda x: str(TextBlob(x).correct()))
