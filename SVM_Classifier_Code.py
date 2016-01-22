# -*- coding: utf-8 -*-

import codecs
import os, re
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, make_scorer

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
    emotion.append(re.sub("\n", " ", emotionLines[l]))


#Printing the evaluation accuracy of the classifier
def evaluate_model(target_true,target_predicted):
    print (classification_report(target_true,target_predicted) )
    print ("The accuracy score is {:.2%}".format(accuracy_score(target_true,target_predicted)))



#list of tags for our emotions [#happy,#sad,#anger,#surprise,#fear,#disgust]
tagLexicon= ["#खुशी","#दुखी","#गुस्सा","#हैरान", "#भय", "#घृणा"]

#list of synonyms for each emotion tag so that we can crawl based on these respective emotions so as to have representative data
happy = ["आनंद","गदगद","हर्षित","प्रसन्नता", "शुभ", "खुशी", "#खुशी"]
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



newData = [(k, "".join(myData[k][i]).split("\t")[-1]) for k in myData for i in range(len(myData[k]))]
data =[]
target = []
#appending tweet data to data list and appending target label to target list
for i in range(0, len(newData)):
    # skip missing data
    data.append(newData[i][1])
    target.append(newData[i][0])

#SVM vectorizes the input data for appropriate representation as numerical data
count_vectorizer = CountVectorizer(binary='false')
data = count_vectorizer.fit_transform(data)
#The term frequency inverse document frequency transformer is used to show how important  a word is to a document
tfidf_data = TfidfTransformer(use_idf=False).fit_transform(data)

#Perform cross validation to split data into train set and test set
data_train,data_test,target_train,target_test = cross_validation.train_test_split(tfidf_data,target,test_size=0.1,random_state=37)

#count of the total number of tweets in each class of emotion
print ("Tweets in all classes",countdict)

#In order to identify the majority class we identify the class of emotion which has maximum presence in tweets
maximum = max(countdict, key=countdict.get)
print("Majority class",maximum, round((countdict[maximum]/ sum(countdict.values()))*100),"%")

#Fitting of data by the classifier accoding to the given train set
model = SVC(probability=False,random_state=33,kernel='linear',shrinking=True)
model.fit(data_train, target_train)

#Start predictions based on accumalated learning from train set
predicted = model.predict(data_test)

evaluate_model(target_test,predicted)







