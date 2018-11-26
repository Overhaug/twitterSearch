# twitterSearch
Search twitter for disaster events localization by using tweepy, pyspark and k-means

# Assuming you have pip3, run...
`pip3 install -r requirements.txt`

# Setup
Ensure spark 2.3.2 install and setup.

Windows 10 System Enviorment variables:
PYSPARK_DRIVER_PYTHON = jupyter
PYSPARK_DRIVER_PYTHON_OPTS = notebook
in cmd run: pyspark
Starts jupyter notebook with a pyspark shell.

# Running the scripts
1. Start TwitterStream.py and let it run for how long you want to sample tweets. 
Interupt the interpreter when done.

2. Open cmd and run pyspark. Select SparkDF.ipynb and run it.

3. HTML_client\Client.html. In order to lauch the webapp containing the geographic twitter plots.
- Example Raw Tweets contains a test sample set over USA
- Example Cluster Tweets contains the same dataset with k-mean over it.
- Live Clustered Tweets contains the batch currently sampled over california as default.

K-means is ment to be used over a small area with many tweets.
The sample size and cluster amount does not localize disaster events as it is now with the nation wide test data.

