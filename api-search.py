import tweepy
import jsonpickle
import sys

consumer_key = '3YXUnNMFMes5sLetUS0PuueST'
consumer_secret = '5i4s4wGOWrLu2rFvoooUvDp9TydX1o97a8IhS42lTrJF79EjhR'
access_token = '4010831469-YHfZRjO8WcOIvvJMh8t26qMlebZj2zehXgHAjdz'
access_secret = 'PxKYXT5cAuqg6x57r24vdy6pHiHAEH4RhH6UwwPCUkboJ'
 
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

print(" ")
print("Downloading tweets on the following hashtags: ")
print(" ")

list_of_hashtags = {
				#English
				0:"#EUelections2019", 
				1:"#EuropeanElections2019",
				#Franch
				2:"#Europeennes2019",
				3:"#ElectionsEuropeennes2019",
				#Spanish
				4:"#EUElecciones2019",
				5:"#EleccionesEuropeas2019",
				#German
				6:"#Europawahl2019",
				7:"#Europawahl",
				#Italian
				8:"#ElezioniEuropee2019",
				9:"#Europee2019"
				}

for key, value in list_of_hashtags.items():
	print(value)
print(" ")

hashtag_count = 0
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1
tweetCount = 0
TotTweetCount = 0

print("Downloading max {0} tweets".format(maxTweets))
print(" ")

while hashtag_count < len(list_of_hashtags):
	searchQuery = list_of_hashtags[hashtag_count] # this is what we're searching for
	print("Downloading tweets on {0}".format(searchQuery))
	# We'll store the tweets in a text file.
	fName = searchQuery + '.txt' 
	with open(fName, 'w') as f:
		while tweetCount < maxTweets:
			try:
				if (max_id <= 0):
					if (not sinceId):
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
					else:
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', 
											since_id=sinceId) #Returns results with an ID greater than (that is, more recent than) the specified ID.
				else:
					if (not sinceId):
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended',
                                            max_id=str(max_id - 1)) #Returns results with an ID less than (that is, older than) or equal to the specified ID.
					else:
						new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended',
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
				if not new_tweets:
					print("No more tweets found on this hashtag")
					break
				for tweet in new_tweets:
					f.write(jsonpickle.encode(tweet._json, unpicklable=False)+ "\n")
				tweetCount += len(new_tweets)
				print("Downloaded {0} tweets".format(tweetCount))
				max_id = new_tweets[-1].id
			except tweepy.TweepError as e:
            # Just exit if any error
				print("some error : " + str(e))
				break
	print("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
	print(" ")
	TotTweetCount += tweetCount
	tweetCount = 0
	max_id = -1
	hashtag_count+=1
print("Downloaded {0} tweets in total".format(TotTweetCount))
