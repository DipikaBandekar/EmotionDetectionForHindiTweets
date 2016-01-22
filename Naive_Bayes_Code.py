# -*- coding: utf-8 -*-

import codecs
import nltk
import os, re
from collections import defaultdict
from random import shuffle

#parses the input file and gets all the annotated tweets
def getListOfLines():

    #reading the input file by name
    infileObject = codecs.open("TweetsFile.txt", "r", "utf-8")
    listOfLines = infileObject.readlines()
    return listOfLines

#appending all the emotion tags to list called emotion
lines = getListOfLines()
emotionLines = [line for line in lines]
emotion = []
for l in range(0,len(emotionLines)):
    emotion.append(re.sub("\r\n", " ", emotionLines[l]))


#list of tags for our emotions [#happy,#sad,#anger,#surprise,#fear,#disgust]
tagLexicon= ["#खुशी","#दुखी","#गुस्सा","#हैरान", "#भय", "#घृणा"]

#list of synonyms for each emotion tag so that we can crawl based on these respective emotions so as to have representative data
happy = ["आनंद","गदगद","हर्षित","प्रसन्नता", "शुभ", "खुशी", "#खुशी", "#आनंद","#गदगद","#हर्षित","#प्रसन्नता", "#शुभ"]
sad = ["दुखी", "दु:ख", "दुखा", "#पीड़ा ", "पीड़ा", "कष्ट ", "संताप ", "शोक", "खेद", "पीर","लेश","#कष्ट ","#व्यथा", "#वेदना ","#संताप ","#शोक","#खेद","#पीर","#लेशयथा", "वेदना "]
anger= ["गुस्सा ","क्रोध", "नाराज़ ","आक्रोश", "खफा ","रोष ","क्रोध","नफरत","#गुस्सा ","#क्रोध", "#नाराज़ ","#आक्रोश", "#खफा ","#रोष ","#क्रोध","#नफरत"]
surprise= ['हैरान', 'आश्चर्य', 'स्तब्ध', 'दंग', ' विस्मित', '#हैरान', '#आश्चर्य', '#स्तब्ध', '#दंग', '#विस्मित']
fear = ["भय","भीति", "शंका", "ख़ौफ़ ", "परेशानी ", "डरना ", "डरपोक", "सहमाना ", "डर", "अंदेशा", "#भय", "#भीति", "#शंका", "#ख़ौफ़"]
disgust = ["#घृणा", "घृणा"]

myData = {}
countdict ={}

# splitting each tweet and looking for the presence of any of the special keywords that help classify the emotion for the tweet
for cat in tagLexicon:
    if cat == "#खुशी":
        counter=0
        for i in happy:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]
        countdict["#खुशी"]= counter

    elif cat == "#दुखी":
        counter=0
        for i in sad:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]
        countdict["#दुखी"]= counter

    elif cat == "#गुस्सा":
        counter=0
        for i in anger:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]
        countdict["#गुस्सा"]= counter

    elif cat == "#हैरान":
        counter=0
        for i in surprise:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]

        countdict["#हैरान"]= counter
    elif cat == "#भय":
        counter=0
        for i in fear:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]

        countdict["#भय"]= counter

    elif cat == "#घृणा":
        counter=0
        for i in fear:
            for tweet in emotion:
                if i in tweet.split():
                    if cat in myData.keys():
                        myData[cat] = myData[cat] + [tweet]
                        counter+=1
                    else:
                        myData[cat] = [tweet]
        countdict["#घृणा"]= counter

    else:
        myData[cat] = [tweet for tweet in emotion if cat in tweet.split()]

#print("myData",myData)
newData = [(k, "".join(myData[k][i]).split("\t")[-1]) for k in myData for i in range(len(myData[k]))]
shuffle(newData)


def getFeatures(dataPoint):
    features = defaultdict()
    #labels contain the tags and feats contain the data
    label, feats = dataPoint[0], dataPoint[1].split()
    for i in feats:
        features[i] = i
    return features, label

#Obtain featuresets for the data for better classification
featuresets = [getFeatures(i) for i in newData]
#print("featuresets",featuresets)

#performing cross validation to split into train data and test data
train_set, test_set1 = featuresets[:680], featuresets[681:851]

#Initiate training on the given train data with the help of  Naive Bayes Classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

#count of the total number of tweets in each class of emotion
print ("Tweets in all classes",countdict)

#In order to identify the majority class we identify the class of emotion which has maximum presence in tweets
maximum = max(countdict, key=countdict.get)
print("Majority class",maximum, round((countdict[maximum]/ sum(countdict.values()))*100),"%")

#print Accuracy of the classifier
print("Accuracy on testdata: ", round((nltk.classify.accuracy(classifier, test_set1))*100, 2), "%")


