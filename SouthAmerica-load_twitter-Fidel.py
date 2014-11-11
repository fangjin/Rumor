import json
from unidecode import unidecode
import string
from Levenshtein import ratio
import nltk
import datetime
import sqlite3 as lite

keywords =[]
keyPerson =[]

#read the keyword from the text file
def readKeyWords(files):
    keywordsES = []
    f = open(files,"r")
    for line in f.readlines():
        keywordsES.append(unidecode(line.strip("\n").decode("latin-1")))
    f.close()
    return keywordsES


def removePunctuations(text):
    for symbol in string.punctuation:
        text = text.replace(symbol," ")
    return text

def ReadKeyPerson(files):

    keyPerson = []
    f = open(files,"r")
    for line in f.readlines():
        keyPerson.append(unidecode(line.strip("\n").decode("latin-1")))
    f.close()
    return keyPerson
    
def checkForRetwitterUser(text):

    text  = unidecode(text)
    flag = False
    for word1 in keyPerson:
	if ratio(word1.lower(), text.lower())>0.9:
	    flag = True
	    break

    return flag

def twitTimeToDBTime(t):
    TIME_FORMAT = "%a, %d %b %Y %H:%M:%S +0000"
    createdAt = datetime.datetime.strptime(t,TIME_FORMAT)
    return createdAt.strftime("%Y-%m-%d %H:%M:%S")


def checkForRumorWords(uLang,tLang,text):
    #keywords = []
    if uLang != "es" and tLang != "es":
        #keywords = readKeyWords("keyword2")
	return False
    flag = False    
    text = removePunctuations(text)
    text = unidecode(text)
    for word1 in keywords:
	if len(word1) >2:

            for word2 in text.split(" "):
                if ratio(word1.lower(),word2.lower()) >= 0.9:
		    #print "1~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		    #print word1
		    #print word2
		    #print "~~~~~~~~~~~~hello~~~~~~~~~~~~~~~~"
                    flag = True
                    break
            if flag:
                break
	     
            for pairs in nltk.bigrams(text):
                pairWords = pairs[0]+' '+pairs[1]
                if ratio(word1.lower(), pairWords.lower()) >= 0.8:
                    #print "2~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		    #print word1
		    print pairWords
		    #print "~~~~~~~~~~~~hello~~~~~~~~~~~~~~~~"
                    flag = True
                    break
            if flag:
                break

	     
	    for tris in nltk.trigrams(text):
	        trisWords = tris[0]+ ' ' + tris[1] + ' '+tris[2]
	        if ratio(word1.lower(), trisWords.lower()) >=0.8:
		    #print "3~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		    #print word1
		    print trisWords
		    #print "~~~~~~~~~~~~hello~~~~~~~~~~~~~~~~"
                    flag = True
                    break
	    if flag:
	        break
		
    return flag


def checkLocation(locations):

    if len(locations) < 3:
	return True

    flag = False
    locations  = unicode(locations);
    for location_word in locations.split(" "):
	if ratio(unicode('mexico'), location_word.lower()) >= 0.8:
	    flag = True
	    break
    return flag		


def read_twitter(rumorCode,filepath,database):
    
    start_time = datetime.datetime.now()

    with open(filepath) as f:
        index  = 0
	index_insert =0
	
	con = lite.connect(database)
		
        for line in f:
	    try:
		    tweet  = json.loads(line)
		    index  = index +1
		    #print index
		    #initialize the variables
		    user_description = user_status= user_followers=user_friends=lang=""
		    location = time_zone = user_id = text= text_id=created_at=""

		    klot_value = retwitter_user_id =""
		    uLang = tLang =""

		    sentiment =""
		    if tweet.has_key('interaction'):
			if tweet['interaction'].has_key('author'):
			    if 	tweet['interaction']['author'].has_key('username'):
				username=tweet['interaction']['author']['username']	    

		    if tweet.has_key('twitter'):
		        if tweet['twitter'].has_key('text'):
		            text = tweet['twitter']['text']
			if tweet['twitter'].has_key('user'):
	 	    	    if tweet['twitter']['user'].has_key('time_zone'):
		                time_zone = tweet['twitter']['user']['time_zone']
			    if tweet['twitter']['user'].has_key('location'):
				location = tweet['twitter']['user']['location']   

		        else:
		            if tweet['twitter'].has_key('retweet'):
		                if tweet['twitter']['retweet'].has_key('text'):
		                    text  = tweet['twitter']['retweet']['text']
		          
		            if tweet["twitter"]["retweet"]["user"].has_key("lang"):
		                uLang = tweet["twitter"]["retweet"]["user"]["lang"]

			    if tweet['twitter']['retweet']['user'].has_key('time_zone'):
		                time_zone = tweet['twitter']['retweet']['user']['time_zone']		
			
			    if tweet['twitter']['retweet']['user'].has_key('location'):
				location  = tweet['twitter']['retweet']['user']['location']

		

		        if tweet.has_key("language"):
		            if tweet["language"].has_key("tag"):
		                tLang = tweet["language"]["tag"]
		        
			if    index%10000 ==0:
				print "Have dealing with twitters:",
				print index     
		
			 

			#if checkLocation(time_zone) is False:
			#    if checkLocation(location) is False:
			#	continue
		
			 

		        if checkForRumorWords(uLang,tLang,text) is False:
		            #print "hello"
		            continue
		            
		             
		            

		     	index_insert = index_insert + 1
			if (index_insert%100 ==0):
			    print "Insert twitters:",
		            print  index_insert
			 
		        retwitter_user_id ="-1"
			sentiment = "0"
			klot_value = "0"
			user_followers ="0"
			user_friends ="0"
			user_status ="0"
		

		        # parser the twitter information
			if tweet['twitter'].has_key('id'):
			    text_id = tweet['twitter']['id']
		        if tweet['twitter'].has_key('user'):
		            if tweet['twitter']['user'].has_key('description'):
		                user_description = tweet['twitter']['user']['description']
		            if tweet['twitter']['user'].has_key('statuses_count'):
		                user_status = tweet['twitter']['user']['statuses_count']
		            if tweet['twitter']['user'].has_key('followers_count'):
		                user_followers = tweet['twitter']['user']['followers_count']
		            if tweet['twitter']['user'].has_key('friends_count'):
		                user_friends = tweet['twitter']['user']['friends_count']
		            if tweet['twitter']['user'].has_key('lang'):
		                ulang = tweet['twitter']['user']['lang']
		            if tweet['twitter']['user'].has_key('time_zone'):
		                time_zone = tweet['twitter']['user']['time_zone']         
		            if tweet['twitter']['user'].has_key('id'):
		                user_id  = tweet['twitter']['user']['id']
			    if tweet['twitter']['user'].has_key('location'):
				location = tweet['twitter']['user']['location']       

		            if tweet['twitter'].has_key('id'):
		                text_id = tweet['twitter']['id']
		            if tweet['twitter'].has_key('text'):
		                text = tweet['twitter']['text']
		            if tweet['twitter'].has_key('created_at'):
		                created_at = twitTimeToDBTime(tweet['twitter']['created_at'])

		            
		            

		        #parser the retwitter information
		        if tweet['twitter'].has_key('retweet'):	  
		            	
		            if tweet['twitter'].has_key('retweeted'):
		                if tweet['twitter']['retweeted'].has_key('user'):
		                    if tweet['twitter']['retweeted']['user'].has_key('id'):
		                        retwitter_user_id = tweet['twitter']['retweeted']['user']['id']
				if tweet['twitter']['retweeted'].has_key('id'):
				    re_text_id = tweet['twitter']['retweeted']['id']

		           
		                    
		            if tweet['twitter']['retweet'].has_key('user'):
		                if tweet['twitter']['retweet']['user'].has_key('description'):
		                    user_description = tweet['twitter']['retweet']['user']['description']
		                if tweet['twitter']['retweet']['user'].has_key('statuses_count'):
		                    user_status = tweet['twitter']['retweet']['user']['statuses_count']
		                if tweet['twitter']['retweet']['user'].has_key('followers_count'):
		                    user_followers = tweet['twitter']['retweet']['user']['followers_count']
		                if tweet['twitter']['retweet']['user'].has_key('friends_count'):
		                    user_friends = tweet['twitter']['retweet']['user']['friends_count']
		                if tweet['twitter']['retweet']['user'].has_key('lang'):
		                    ulang = tweet['twitter']['retweet']['user']['lang']
		                if tweet['twitter']['retweet']['user'].has_key('time_zone'):
		                    time_zone = tweet['twitter']['retweet']['user']['time_zone']         
		                if tweet['twitter']['retweet']['user'].has_key('id'):
		                    user_id  = tweet['twitter']['retweet']['user']['id']
				if tweet['twitter']['retweet']['user'].has_key('location'):
				    location  = tweet['twitter']['retweet']['user']['location']
				 

		                if tweet['twitter']['retweet'].has_key('id'):
		                    text_id = tweet['twitter']['retweet']['id']
		                if tweet['twitter']['retweet'].has_key('text'):
		                    text = tweet['twitter']['retweet']['text']
		                if tweet['twitter']['retweet'].has_key('created_at'):
		                    created_at = twitTimeToDBTime(tweet['twitter']['retweet']['created_at'])
		        
				
		       
		
			if tweet.has_key("salience"):
		            if tweet["salience"].has_key("content"):
		                if tweet["salience"]["content"].has_key("sentiment"):
		                    sentiment = tweet["salience"]["content"]["sentiment"]
		        if tweet.has_key("klout"):
		            if tweet["klout"].has_key("score"):
		                klot_value = tweet["klout"]["score"]
		
	
			rumorData = [rumorCode,text,text_id,username,int(user_id),uLang,user_description,created_at,time_zone,"-1","-1",location,tLang, \
					int(user_followers),int(user_friends),int(user_status),int(retwitter_user_id),re_text_id,\
					int(sentiment),int(klot_value)]

			with con:			
		                cur=con.cursor()			
		                cur.execute("INSERT INTO t_rumor(rumor_code,text,\
						text_id,username,userId,uLang,user_description,createdAt,time_zone,countryCode,countryName,\
						location,tLang,followers_accout,friends_account,states_account,re_user_id,re_text_id,\
						sentiment,score)\
						VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",rumorData)	
		
				
	    except:
	            continue	 
	end_time = datetime.datetime.now()
	print 	(end_time -start_time).seconds/60
	print "Finish"



keywords = readKeyWords("keyword5")


read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-16-01-35-13","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-16-13-35-13","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-17-12-00-36","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-18-00-00-36","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-18-12-00-37","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-19-00-00-37","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-19-12-00-38","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-20-00-00-38","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-20-12-00-40","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-21-00-00-40","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-21-12-00-40","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-22-00-00-40","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-22-12-00-41","/home/jf/Documents/Rumor/Rachel/rumor1017.db")
read_twitter("5","/home/jf/Documents/Rumor/tweet-data/5/datasift-twitter-2012-10-22-00-00-40","/home/jf/Documents/Rumor/Rachel/rumor1017.db")











