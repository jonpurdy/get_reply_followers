import tweepy
import csv

# Your details
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Bounds of the range of Tweets you want to pull
# (So you don't pull your entire timeline)
# since_id = "1267829476102033414"  # Oldest
# max_id = "1267871539501731841"    # Newest

# Tweepy OAuth process + API creation
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Holds the stuff we will output
# First list is for header row
replied_tweets = [["tweet_id", "aggregate_followers"]] 

# Get tweets
for status in tweepy.Cursor(api.user_timeline).items():
# Use below instead if you want to bound your Tweets using since_id and max_id
# for status in tweepy.Cursor(api.user_timeline, since_id=since_id, max_id=max_id).items():
    print("---\n%s\n%s" % (status.id, status.text))

    # Determine if it's a reply
    # First word of reply will be @username, so [0] is username
    # and [0][0] is first character of username (@)
    if status.text.split(" ")[0][0] == "@":

        followers = 0  # aggregate count for all replied users
        reply_usernames = [] # ensure we don't double count if they're mentioned more than once

        # Get the users who are being replied to        
        # Only get the users mentioned at the beginning
        for word in status.text.split(" "):
            # Is the world a username?
            if word[0] == "@":
                print(word[1:])
                # word[1:] is removing the @ from @username
                if word[1:] not in reply_usernames:
                    followers += api.get_user(word[1:]).followers_count
                    reply_usernames.append(word[1:])
            
            # If not a username, finish and move on
            else:
                replied_tweets.append([status.id, followers])
                break

for t in replied_tweets:
    print(t)
