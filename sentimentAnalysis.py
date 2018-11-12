import textblob
df['tweet_text'][:200].apply(lambda x: TextBlob(x).sentiment)

df['sentiment'] = df['tweet_text'].apply(lambda x: TextBlob(x).sentiment[0] )
df[['tweet_text','sentiment']].head()

df["sentiment"]


