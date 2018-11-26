# https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/
import numpy as np
import pandas as pd
import nltk
import json
from pandas.io.json import json_normalize

# load json object
with open("data/json_data.json", encoding="utf-8") as f:
    d = json.load(f)

# Creates a dataframe; each row is a tweet, each column is a tweet attribute + tweet ID
df = json_normalize(data=d['tweets'], record_path='tweet',
                            meta=['tweet_id'])

df.columns
df.head(5)
df['tweet_text'].head()
#_____________ TextCleaning__________________
# Convert to lowercase
df['tweet_text'] = df['tweet_text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['tweet_text'].head()

# Remove punctuation
#rgx = '[^\w\s]'  # remove any word or whitespace character, this includes #
rgx = '[.,]'  # remove , or .
df['tweet_text'] = df['tweet_text'].str.replace(rgx, '')
df['tweet_text'].head()


# Create count numbers of hastags used in each tweet.
df['hastags'] = df['tweet_text'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))
df[['tweet_text','hastags']].head()
df['hastags'].max()
df["hastags"].sum()

# Filter by keyword
keyword = "trump"
df['keyword'] = df['tweet_text'].apply(lambda x: len([x for x in x.split() if x.startswith(keyword)]))
df[['keyword']].head()


keywordDf = df[(df['keyword'] >= 1)]
keywordDf["keyword"].head()
keywordDf["keyword"].max()
keywordDf.head()
keyword_json = keywordDf.to_json(orient='records')


def dump_json2(tweets, file):
    with open(file, "w") as write_file:
        json.dump(tweets, write_file, indent=4)

dump_json2(keyword_json, "data/keyword_data.json")




#______More Text cleaning____________
# Remove stopwords
#from nltk.corpus import stopwords
#stop = stopwords.words('english')
#df['tweet_text'] = df['tweet_text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
#df['tweet_text'].head()

# Remove common words
#freq = pd.Series(' '.join(df['tweet_text']).split()).value_counts()[:10]

# Remove rare words
#freq = pd.Series(' '.join(df['tweet_text']).split()).value_counts()[-10:]
#freq

# Library to combine words that are not spelled correct.
#from textblob import TextBlob
#df['tweet_text'][:5].apply(lambda x: str(TextBlob(x).correct()))


#df["tweet_text"].head(100)

# Stemming, removing suffices, brave and bravly is looked at as the same.
#from nltk.stem import PorterStemmer
#st = PorterStemmer() # Antar denne er ment for engelske ord.
#df['tweet_text'][:5].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))

# Lemmatization, Tries to reduce the words to its root word, rather then drop the ending of it.
#from textblob import Word
#nltk.download("wordnet")

#df['tweet_text'] = df['tweet_text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
#df['tweet_text'].head(10)

# Tokenize word list
#from nltk.tokenize import TweetTokenizer
#tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
#joinedTweets = ''.join(df["tweet_text"])
#tknzr.tokenize(joinedTweets)

#df["tweet_text"][0]

