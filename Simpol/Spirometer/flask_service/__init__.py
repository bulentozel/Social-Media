from flask import Flask
from flask_httpauth import HTTPBasicAuth
from LibOM.Tools import *

import pprint
pp = pprint.PrettyPrinter()

# Setting up connection to the Media Watch Tower:
#print "Connecting to WatchTower"
#ClientWT = WatchTower()

# Setting up connection to the Media Watch Tower:
new = dict()
new['Consumer_Key'] = 'c594ocOQwk4hlieUzQgAWBKPn'
new['Consumer_Secret'] = 'nQDv0ZKmIgJ15MVN1oWQyIMHA4PSMTLIhFNnvtuAGJDrpquVpa'
new['Access_Token'] = '95098920-yR4A2DMVoXf3O8tyWfAJN76Zw7CafXk9eU0dsvtA8'
new['Access_Token_Secret'] = 'wXV3rUYLmGN0rO0E6ZC1pWkn4A1EAVh74jF3W3Kk0suJC'
print("Connecting to Twitter")
ClientTwitter = Twitter(new)

# Loading the maker dictionary:
print("Loading dictionaries.")
MD = MakerDictionary()

# Retrieving influencer lists:
#WTInfluencers = ClientWT.retrieve_influencers()

"""
print('Determining followers list ..')
SeedInfluencers = csv_to_list('./data/seedusers.csv')
min_required_follow_counts = 100
followers = ClientTwitter.retrieve_followers(SeedInfluencers, min_required_follow_counts)
pp.pprint(followers['distro'])
ExtendedList = followers['theset'].union(SeedInfluencers)
print('Done with extension of members.')
print('Collecting followers ..')
followers = fClientTwitter.retrieve_followers(WTInfluencers[0:1], 100)
pp.pprint(followers)
print('Done collecting followers.')
"""

WTInfluencers = csv_to_list('./data/simpolproject_followers.csv')
print("Number of initial twitter users to follow: {}".format(len(WTInfluencers)))



# Collecting tweets of the influencers:
debates = ClientTwitter.retrieve_tweets(WTInfluencers, 200)
#debates = ClientTwitter.retrieve_tweets(WTInfluencers[0:1], 10)
#debates = ClientTwitter.retrieve_tweets(WTInfluencers, 50)

# Loading previous scoreboard:
SB = ScoreBoard()

try:
    SB.import_board("./data/scoreboard.p")
except IOError:
    print("No previously stored Scoreboard is found.")


# Populating the score board:

print("The user data retrieved from Twitter: " )
for inf in debates.keys():
    ntweets = debates[inf]['ntweets']
    if not ntweets: continue
    text = debates[inf]['content']
    nmappings, nwords, counts = extract_features(text, MD)
    features = {"source":0,"ntweets":ntweets, "nwords":nwords, "nmappings":nmappings, "counts":counts}
    SB.post_scores(inf, features)
    print("{} {} {} {}".format(inf, ntweets, nmappings, nwords))


# Store the baord:
SB.store_the_board("./data/scoreboard.p")


# Initialization of app and auhentication:
app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

import flask_service.api

