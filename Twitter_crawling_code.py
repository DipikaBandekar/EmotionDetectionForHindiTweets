import codecs
import tweepy
import time
import  sys
import csv
import json
from tweepy import OAuthHandler

#required tokens for working with data from twitter using Tweepy
access_token = "103589925-PYiNRi6sAoSAFCau7Q5zDAqF7Kt8WwsK5EunWL3I"
access_token_secret = "u8N1nS93eN5npmtBOAxCwJgZE0W4wPCNe1CEuCB9lEIys"
consumer_key = "IIFBxSZv8YnhRJuvvDJVkR4ht"
consumer_secret = "zou3XOVMDXp9esingDNEowUeEPmTKkY4daZGYdmalovyd9JCxr"


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
               wait_on_rate_limit_notify=True)

#Authenticating with given tokens
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)


def twitter_miner(query):
    tweetCount=0
    maxTweets=1000
    while tweetCount < maxTweets:
        try:
           #Save the crawled data to a locally created text file. Here we crawl for the emotion Khushi(Happy)
            saveFile = codecs.open('Khushi.txt', 'a', 'utf-8')
            csvWriter = csv.writer(saveFile)

            #crawling in hindi and hence the option of 'hi'
            newTweets=api.search(q=query, lang="hi", count=100)

            for tweet in newTweets:
                # printing only tweet
                print ((tweet))
                csvWriter.writerow([tweet.text])
                tweetCount+=1
            saveFile.close()
        except tweepy.TweepError as e:
            print("some error : " + str(e))
            print("retrying in 20 seconds")
            time.sleep(20)

if __name__ == "__main__":
    print ("Welcome to Tweepy!\n")

    #We try to increase representation by crawling for all seeds in the similar spectrum of emotion (eg here. HAPPY)
    seeds = ["आनंद","गदगद","हर्षित","प्रसन्नता", "शुभ", "खुशी", "#खुशी", "#आनंद","#गदगद","#हर्षित","#प्रसन्नता", "#शुभ"]
    #Similarly crawling seeds for the remaining emotions
    #seeds = ["दुखी", "दु:ख", "दुखा", "#पीड़ा ", "पीड़ा", "कष्ट ", "संताप ", "शोक", "खेद", "पीर","लेश","#कष्ट ","#व्यथा", "#वेदना ","#संताप ","#शोक","#खेद","#पीर","#लेशयथा", "वेदना "]
    #seeds= ["गुस्सा ","क्रोध", "नाराज़ ","आक्रोश", "खफा ","रोष ","क्रोध","नफरत","#गुस्सा ","#क्रोध", "#नाराज़ ","#आक्रोश", "#खफा ","#रोष ","#क्रोध","#नफरत"]
    #seeds= ['हैरान', 'आश्चर्य', 'स्तब्ध', 'दंग', ' विस्मित', '#हैरान', '#आश्चर्य', '#स्तब्ध', '#दंग', '#विस्मित']
    #seeds = ["भय","भीति", "शंका", "ख़ौफ़ ", "परेशानी ", "डरना ", "डरपोक", "सहमाना ", "डर", "अंदेशा", "#भय", "#भीति", "#शंका", "#ख़ौफ़"]
    #seeds = ["#घृणा", "घृणा"]
    outfile="wimTest.txt"
    for seed in seeds:
        print("\nAttempting to fetch query '{0}':\n".format(seed))
        twitter_miner(seed)
