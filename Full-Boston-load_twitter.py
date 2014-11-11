import json
from unidecode import unidecode
import string
from Levenshtein import ratio
import nltk
import datetime
import sqlite3 as lite
import re
#should I specify English, or any other language?

# Word splitter pattern
pattern_split = re.compile(r"\W+")

#read the keyword from the text file
def readKeyWords(files):
    keywordsES = []
    f = open(files,"r")
    for line in f.readlines():
        keywordsES.append(unidecode(line.strip("\n")))
    f.close()
    return keywordsES

	
def	cal_sentiment(text):
	sentiment = trust = surprise = 0
	words = pattern_split.split(text.lower())
	filenameAFINN = './dic/AFINN-111.txt'
	afinn = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
	sentiments = map(lambda word: afinn.get(word, 0), words)
	if sentiments:
		sentiment = int(sum(sentiments)) 

	trust_list = readKeyWords('./dic/Trust_EN')
	surp_list = readKeyWords('./dic/Surprise_En')	
	for w in trust_list:
		if w in words:
			trust+=1
	for word in surp_list:
		if word in words:
			surprise+=1
	return sentiment, trust, surprise


def removePunctuations(text):
    for symbol in string.punctuation:
        text = text.replace(symbol," ")
    return text
   

def twitTimeToDBTime(time):
    #TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"
    TIME_FORMAT = "%a %b %d %H:%M:%S +0000 %Y"
    createdAt = datetime.datetime.strptime(time,TIME_FORMAT)
    return createdAt.strftime("%Y-%m-%d %H:%M:%S")


def checkForRumorWords(text):
	keywords = readKeyWords("Boston-keywords")
	flag = False    
	text = removePunctuations(text)
	text = unidecode(text)
	for word in keywords:
		if word in text.split():
			flag = True
			break
		if flag:
			break
	return flag



def read_twitter(rumorCode,filepath,database):   
    possibe_hashtag = set(["BostonMarathon","Marathon","bostonmarathon","marathonmonday","MarathonMonday","marathonBDC","marathonMonday"])
    # "thelongrun"
    with open(filepath) as f:
		con = lite.connect(database)
		for line in f:
			try:
				tweet  = json.loads(line)
				hashtags = []
				reply_user_id = retweet_text_id = re_user_id = retweet_location =''
				sentiment = trust = surprise = 0
				user_lang = tweet['user']['lang']
				if user_lang == 'en':
					created_at = tweet['created_at']
					created_at = twitTimeToDBTime(tweet['created_at'])
					reply_user_id = tweet["in_reply_to_user_id"]
					text_id = tweet['id']
					text = tweet['text']
					text1 = removePunctuations(text)
				
					sentiment, trust, surprise = cal_sentiment(text1)
				
								
					user_id = tweet['user']['id']
					user_location = tweet['user']['location']
					user_followers = tweet['user']['followers_count']
					user_friends =  tweet['user']['friends_count']
				
					user_geo = tweet['geo']
					user_place = tweet['place']
				
					if tweet.has_key('entities'):
						if tweet['entities'].has_key('hashtags'):
							for item in tweet['entities']['hashtags']:
								if item.has_key('text'):  		
									hashtags.append(item['text'])
								
					if tweet.has_key('retweeted_status'):
						retweet_text_id = tweet['retweeted_status']['id']
						if tweet['retweeted_status'].has_key('user'):
							re_user_id = tweet['retweeted_status']['user']['id']
							retweet_location = tweet['retweeted_status']['user']['location']
			
					if checkForRumorWords(text) or [x for x in possibe_hashtag if x in hashtags]:    	
						rumorData = [rumorCode,created_at,text_id,user_id,user_location,text,reply_user_id,user_followers, user_friends, user_lang, user_geo, user_place, retweet_text_id, re_user_id, retweet_location,sentiment, trust, surprise,str(hashtags)]	
						with con:			
							cur=con.cursor()			
							cur.execute("INSERT INTO t_rumor(rumor_code,createdAt,text_id,userId,user_location,text,reply_user_id, \
							user_followers, user_friends, user_lang, user_geo, user_place, retweet_text_id, re_user_id, retweet_location,sentiment, trust, surprise, hashtag) \
							VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",rumorData)
					else:
						contine
			except:
				continue
		print filepath
		print datetime.datetime.now()
	

read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T00:00.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T00:15.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T00:30.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T00:45.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T01:00.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T01:15.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T01:30.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T01:45.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T02:00.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T02:15.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T02:30.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T02:45.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T03:00.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T03:15.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T03:30.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")
read_twitter("Boston","/media/mynewdrive/test/16/tweets.2013-04-16T03:45.M=000","/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db")


