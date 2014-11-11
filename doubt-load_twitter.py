#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
from unidecode import unidecode
import string
from Levenshtein import ratio
import nltk
import datetime
import sqlite3 as lite
import os
import re
pattern_split = re.compile(r"\W+")

#read the keyword from the text file
def readKeyWords(files):
    keywordsES = []
    f = open(files,"r")
    for line in f.readlines():
        keywordsES.append(unidecode(line.strip("\n").replace("\r","").strip()))
    f.close()
    return keywordsES


def removePunctuations(text):
	for symbol in string.punctuation:
		text = text.replace(symbol," ")
	return text


def	cal_sentiment(text):
	flag = False
	doubt = 0
	text = removePunctuations(text.decode('utf8'))
	text_words = pattern_split.split(text.lower().strip())	
	doubt_list = readKeyWords('/home/jf/Documents/Rumor/Rachel/Boston-code/dic/doubt_Edward')

	for word1 in doubt_list:		
		for word2 in text_words:
			if word1 == word2:				
				doubt = 1
				flag = True
				#print word2
				break
		if flag:
			break

		for pairs in nltk.bigrams(text_words):
			pairWords = pairs[0]+' '+pairs[1]
			if word1 == pairWords:
				doubt = 1
				flag = True
				#print word1
				break
		if flag:
			break

		for tris in nltk.trigrams(text_words):
			trisWords = tris[0]+ ' ' + tris[1] + ' '+tris[2]
        		if word1 == trisWords:
				doubt = 1
				flag = True
				#print trisWords
				break
		if flag:
			break
	return doubt


def twitTimeToDBTime(time):
	TIME_FORMAT = "%a %b %d %H:%M:%S +0000 %Y"
	createdAt = datetime.datetime.strptime(time,TIME_FORMAT)
	return createdAt.strftime("%Y-%m-%d %H:%M:%S")


keywords = ["bostonmarathon", "marathon", "marathoning", "bomb","bombing","explosions","exploded","explode","explosion"]

def checkForRumorWords(text):
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


def read_twitter(filepath,database):
	possibe_hashtag = set(["BostonMarathon","Marathon","bostonmarathon","marathonmonday","MarathonMonday","marathonBDC","marathonMonday"]) 
	start_time = datetime.datetime.now()    
	with open(filepath) as f:
		con = lite.connect(database)
		for line in f:
			try:
				tweet  = json.loads(line)
				hashtags = []
				re_user_id = reply_user_id = text_id = retweet_text_id = re_created_at = ''
				doubt = 0
				user_lang = tweet['user']['lang']
				if user_lang == 'en':
					created_at = tweet["created_at"]
					created_at = twitTimeToDBTime(tweet['created_at'])
					reply_user_id = tweet["in_reply_to_user_id"]

					text = tweet["text"]                    
					doubt = cal_sentiment(text)
					text_id = tweet['id']
					user_id = tweet['user']['id']			    

					if tweet.has_key('retweeted_status'):
						re_user_id = tweet['retweeted_status']['user']['id']
						retweet_text_id = tweet['retweeted_status']['id']
						re_created_at = tweet['retweeted_status']['created_at']
						re_created_at = twitTimeToDBTime(re_created_at)
		 		    
					if tweet.has_key('entities'):			
					    	if tweet['entities'].has_key('hashtags'):
							for item in tweet['entities']['hashtags']:
								if item.has_key('text'):  		
						    			hashtags.append(item['text'])
		
					if checkForRumorWords(text) or [x for x in possibe_hashtag if x in hashtags]:    	
						rumorData = [created_at,int(user_id),text,reply_user_id,re_user_id,text_id,retweet_text_id,re_created_at,doubt]	
						with con:			
							cur=con.cursor()			
							cur.execute("INSERT INTO t_rumor(createdAt,userId,text,reply_user_id,re_user_id,text_id,retweet_text_id,re_created_at,doubt) VALUES(?,?,?,?,?,?,?,?,?)",rumorData)
				    
				else:
					continue									              
			except:
				continue
	print filepath
	print datetime.datetime.now()



for _file in os.listdir("/media/mynewdrive/Boston/done"):
	try:		
		read_twitter("/media/mynewdrive/Boston/done/"+_file,"/home/jf/Documents/Rumor/Rachel/Boston-code/transfer/4test-Boston.db")
	except:
		print _file, "  file read error"
		continue



