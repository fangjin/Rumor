import traceback
import sqlite3 as lite
from datetime import timedelta
from datetime import datetime


def Count_Of_Events(duration,rumorCode):
    try:
        con = lite.connect('/home/jf/Documents/Rumor/Rachel/rumor.db')
        with con:
            cur = con.cursor()
            #sql = "select min(createdAt),max(createdAt) from t_rumor"
	    sql = "select min(createdAt),max(createdAt) from t_rumor where rumor_Code='1017'"
            cur.execute(sql)
            row = cur.fetchone()
            TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    #        createdAt = datetime.datetime.strptime(t,TIME_FORMAT)
            minTime = datetime.strptime(row[0],TIME_FORMAT)
            maxTime = datetime.strptime(row[1],TIME_FORMAT)
            
            countOfRumor ={}
            print maxTime
            print minTime
            
            noOfSegments = (maxTime - minTime)/duration
            print noOfSegments
            startTime= minTime
            endTime = minTime + timedelta(minutes=duration)
            while (startTime< maxTime):
                sql = "select count(1) from t_rumor where createdAt >=? and createdAt<=? "
                cur.execute(sql,[startTime,endTime])		
                row = cur.fetchone()
                itemKey = datetime.strftime(startTime,'%Y%m%d%H%M%S')
                countOfRumor[itemKey]= row[0]
		#print "{0}	{1}".format(itemKey, row[0])
                startTime=endTime
                endTime = startTime + timedelta(minutes=duration)
            #print countOfRumor
    except Exception as e:
            print "Error: %s" % e.args
            print traceback.format_exc()
Count_Of_Events(60,'1017')
