#!/usr/bin/python
#
# wget wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
# unzip imm6010.zip

import math
import re
import sys
reload(sys)
import sqlite3 as lite
sys.setdefaultencoding('utf-8')

# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = '/home/jf/stock-predict/AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def	cal_sentiment(text):
	words = pattern_split.split(text.lower())
	sentiments = map(lambda word: afinn.get(word, 0), words)
	if sentiments:
		sentiment = int(sum(sentiments))        
	else:
		sentiment = 0
	return sentiment


signal=[",",".",")","]","(","[","*",";","...",":","&","/","\\",'"']
def	insert_sent(): 
	try:
		con = lite.connect( "/home/jf/Documents/Rumor/Boston-back.db")
		f = open("./boston-before-bomb","a")				
		with con:			
			cur=con.cursor()			
			sql = "select text, userId from t_rumor where createdAt>'2013-04-15 14:29:00' and createdAt<'2013-04-15 14:49:00' "
			cur.execute(sql)
			rs = cur.fetchall()
			
			for r in rs:
				text = r[0]				
				userId = r[1]
				f.write("%s" % text)
				
				sentiment_score = int(cal_sentiment(text))
				with con:
					cur = con.cursor()
					sql1 = "update t_rumor set sentiment=? where text =? "
					cur.execute(sql1,(sentiment_score,text))
					con.commit()
	except Exception as e:
		print "Error: %s" % e.args



def	get_content(): 
	try:
		con = lite.connect( "/home/jf/Documents/Rumor/Boston-back.db")
		f = open("./boston-before-bomb","a")				
		with con:			
			cur=con.cursor()			
			sql = "select text from t_rumor where createdAt<'2013-04-15 14:49:00' "
			cur.execute(sql)
			rs = cur.fetchall()			
			for r in rs:
				text = r[0]
				f.write("%s" % text)				
				
	except Exception as e:
		print "Error: %s" % e.args

if __name__ == '__main__':
	#insert_sent()
	get_content()
	
    


