import traceback
import sqlite3 as lite
from datetime import timedelta
from datetime import datetime

def Count_all():
    try:
        con = lite.connect('/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db')
        with con:
            cur = con.cursor()
	    sql = "select min(createdAt),max(createdAt) from t_rumor" #(u'2013-04-15 14:45:09', u'2013-04-16 04:00:42')
            cur.execute(sql)
	    row = cur.fetchone()
	    print row
    except Exception as e:
            print "Error: %s" % e.args
#Count_all()



def Count_all_tweets(duration):
    try:
        con = lite.connect('/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db')
        with con:
            cur = con.cursor()	    
            sql = "select min(createdAt),max(createdAt) from t_rumor"
	    #sql = "select min(createdAt),max(createdAt) from t_rumor where createdAt<'2012-09-06 00:00:00'
            cur.execute(sql)
            row = cur.fetchone()
            TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    	    #createdAt = datetime.datetime.strptime(t,TIME_FORMAT)
            minTime = datetime.strptime(row[0],TIME_FORMAT)
            maxTime = datetime.strptime(row[1],TIME_FORMAT)
            
            countOfRumor ={}
            print maxTime
            print minTime
            
            noOfSegments = (maxTime - minTime)/duration
            print noOfSegments
            startTime= minTime
            endTime = minTime + timedelta(minutes=duration)
            #while (startTime< maxTime):
	    while (str(endTime)<"2013-04-16 04:00:43"):
                sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=?"  # tweet accumulated volume
		#sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? and sentiment>0" # negative
		#sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? and sentiment=0" # neutral
		#sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? and trust>0" # trust
		#sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? and trust=0" #doubt
		#sql = "select count(distinct(userId)) from t_rumor where createdAt >=? and createdAt<=? "
                cur.execute(sql,[startTime,endTime])		
                row = cur.fetchone()
                itemKey = datetime.strftime(endTime,'%Y%m%d%H%M%S')
                countOfRumor[itemKey]= row[0]
		print "{0}	{1} ".format(itemKey, row[0])		
                #startTime= minTime
		startTime = startTime + timedelta(minutes=duration)
                endTime = endTime + timedelta(minutes=duration)
            #print countOfRumor
    except Exception as e:
            print "Error: %s" % e.args
            print traceback.format_exc()
Count_all_tweets(15)


def Count_Retweet(duration):
    try:
        con = lite.connect('/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db')
        with con:
            cur = con.cursor()
            sql = "select min(createdAt),max(createdAt) from t_rumor "
	    #sql = "select min(createdAt),max(createdAt) from t_rumor where createdAt<'2012-09-06 00:00:00'
            cur.execute(sql)
            row = cur.fetchone()
            TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    	    #createdAt = datetime.datetime.strptime(t,TIME_FORMAT)
            minTime = datetime.strptime(row[0],TIME_FORMAT)
            maxTime = datetime.strptime(row[1],TIME_FORMAT)
            
            countOfRumor ={}
            print maxTime
            print minTime
            
            noOfSegments = (maxTime - minTime)/duration
            print noOfSegments
            startTime= minTime
            endTime = minTime + timedelta(minutes=duration)
            #while (startTime< maxTime):
	    while (str(endTime)<"2013-04-16 04:00:43"):
		sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? and reply_user_id!=''   " # retweet
                cur.execute(sql,[startTime,endTime])		
                row = cur.fetchone()
                itemKey = datetime.strftime(endTime,'%Y%m%d%H%M%S')
                countOfRumor[itemKey]= row[0]
		print "{0}	{1} ".format(itemKey, row[0])		
                startTime= minTime
		#startTime = startTime + timedelta(minutes=duration)
                endTime = endTime + timedelta(minutes=duration)
            #print countOfRumor
    except Exception as e:
            print "Error: %s" % e.args
            print traceback.format_exc()
#Count_Retweet(15)




# used for Ghaph
def sample_gephi(database,out_file):
     start_date = datetime.strptime("2013-04-15 18:49:12","%Y-%m-%d %H:%M:%S") 
     start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

     end_date = datetime.strptime("2013-04-15 19:00:00","%Y-%m-%d %H:%M:%S") 
     end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

     try:
        network = open(out_file, 'a')
        con = lite.connect(database)
        sqlstate = "select userId, re_user_id from t_rumor where createdAt >='{}' and createdAt<='{}' and re_user_id!='' order by createdAt".format(start_date,end_date)
        index  = 0
        with con:
            cur = con.cursor()
            cur.execute(sqlstate,)
            #result=cur.fetchone()
            for row in cur.fetchall():		
		onerecord = str(index) + "\t" +row[0] + "\t" + row[1]        
		network.write(onerecord)
	        network.write("\n")
	        index = index +1
        network.close()
        print "Finished"
     except Exception as e:
            print "Error: %s" % e.args
#sample_gephi("/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db","10minutes_retweet.txt")



def re_text(database,out_file):
     start_date = datetime.strptime("2013-04-15 22:55:00","%Y-%m-%d %H:%M:%S") 
     start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")

     end_date = datetime.strptime("2013-04-15 22:59:59","%Y-%m-%d %H:%M:%S") 
     end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

     try:
        network = open(out_file, 'w')
        con = lite.connect(database)
        sqlstate = "select text_id, retweet_text_id from t_rumor where createdAt >='{}' and createdAt<='{}' order by createdAt".format(start_date,end_date)
        #index  = 0
        with con:
            cur = con.cursor()
            cur.execute(sqlstate,)
            #result=cur.fetchone()
            for row in cur.fetchall():
		if row[1]!='':		
			onerecord = row[0] + "\t" + row[1]
		else:
      			onerecord = row[0] + "\t" + "0"
		network.write("%s" % onerecord)
	        network.write("\n")
	        #index = index +1
        network.close()
        print "Finished"
     except Exception as e:
	print "Error: %s" % e.args

#re_text("/home/jf/Documents/Rumor/Rachel/Boston-code/test-Boston.db","Boston-transfer-5minutes.txt")
		


