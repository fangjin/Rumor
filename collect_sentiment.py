#!/usr/bin/env python
import string
import sys
import json
import datetime
import sqlite3 as lite
from unidecode import unidecode
from Levenshtein import ratio
import traceback

def removePunctuations(text):
	for symbol in string.punctuation:
		text = text.replace(symbol," ")
	return text

def twitTimeToDBTime(t):
	TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"
	createdAt = datetime.datetime.strptime(t,TIME_FORMAT)
	return createdAt.strftime("%Y-%m-%d")

def read_twitter(filePath):
	try:        
		twitterFile = open(filePath,'r')
		lines = twitterFile.readlines()
		#con = lite.connect('/home/jf/Currency/consumer-confidence/sentiment.db')
		con = lite.connect('/home/jf/Documents/Rumor/sentiment.db')
		for line in lines:
			try:
				tweet = json.loads(line)
				date = country_code = country = location =  ""
				sentiment=0
		    	
				if tweet.has_key("salience"):
					if tweet["salience"].has_key("content"):
						if tweet["salience"]["content"].has_key("sentiment"):
							sentiment=tweet["salience"]["content"]["sentiment"]
	
				if tweet.has_key("twitter"):
					if tweet["twitter"].has_key("retweet"): 
						if tweet["twitter"]["retweet"].has_key("user"):
							if tweet["twitter"]["retweet"]["user"].has_key("location"):
								location = removePunctuations(tweet["twitter"]["retweet"]["user"]["location"])
					else:
						if tweet["twitter"].has_key("place"):
							if tweet["twitter"]["place"].has_key("country_code"):
								country_code = tweet["twitter"]["place"]["country_code"]
						    		country = tweet["twitter"]["place"]["country"]
				
				if tweet.has_key("interaction"):			
					if tweet["interaction"].has_key("created_at"):
						date = twitTimeToDBTime(tweet["interaction"]["created_at"]) 
				    
				sentiData = [date,sentiment,country,country_code,location]
				if country!="" or country_code!="" or location!="":			
					with con:
						cur=con.cursor()
					       	cur.execute("INSERT INTO small_consumer_confidence(date,sentiment,country,country_code,location) VALUES(?,?,?,?,?)",sentiData)
           		except:
				continue
	except Exception as e:
		print "Error: %s" % e.args
		print traceback.format_exc()

           
#read_twitter("/home/jf/Currency/consumer-confidence/onerecord.json")
#read_twitter("/home/jf/Currency/consumer-confidence/twitter-2012-09-06-14-58-20")
read_twitter("/home/jf/Documents/Rumor/tweet-data/twitter-2012-09-06-14-58-20")

