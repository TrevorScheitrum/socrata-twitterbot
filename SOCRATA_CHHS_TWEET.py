
# coding: utf-8

# In[1]:

#under development: limit tweet @ 140 chars for long SOCRATA titles


# In[1]:

#import the required libraries
import csv, requests, datetime, time
import simplejson as json
from twython import Twython
from local_settings import twython_tokens


# In[2]:

targeturl ='http://chhs.data.ca.gov/' #change this to the SOCRATA portal you want to target, don't forget ending /
descriptor='CHHS OPEN DATA PORTAL'   #change this to a recognizable descriptor for yourself


# In[3]:

r=requests.get(targeturl+"api/dcat.json") #build string according to SOCRATA's convention
j=r.json() #parse the json into a dictionary named j, coincidentally j's KVPs are also dictionaries


# SOCRATA has a limit to how many requests can be made every hour from a public pool without an application token.
# This can especially be a problem if your portal has over 100 datasets. Every time this program is run, you are
# making (x+1) request "pings" against SOCRATA servers, where x is the number of datasets on the target portal
# 
# If you are running into this, you will need to register an account with SOCRATA and append the following code
# behind your API calls:
# 
# ?$$app_token=INSERT-YOUR-APP-TOKEN-HERE

# In[4]:

#if it fetched the data successfully, continue; otherwise stop
#this could probably be implemented more pythonically.. but it works for now

if r.status_code==200:
    print "\nsuccessfully fetched json data, http return code 200"
else:
    sys.exit()


# In[5]:

today=datetime.datetime.today()
monday=today - datetime.timedelta(days=today.weekday())
final_list=[]
newdx={}
ignorelist=['k9fb-stqc','rpkf-ugbp','i7wi-ei4m','emt8-tzcf']
#enter the unique IDs you want to ignore, this is essentially building a "blacklist" of datasets that
#are updated EVERY SINGLE DAY, so people don't get bored reading the same tweets


# In[6]:

#this prints out what the bot found so you can see it in human form before it's tweeted
for i in j:
    if len(i['identifier']) == 9:
        created =datetime.datetime.strptime(i['created'] , '%Y-%m-%d')
        modified=datetime.datetime.strptime(i['modified'], '%Y-%m-%d')

        days_created =today-created
        days_modified=today-modified
        
        if days_modified.days<=1 and i['identifier'] not in ignorelist: #ignore catalog dataset
            #print "created",days_created.days,"days ago"
            #print "modified",days_modified.days,"days ago"
            #print i['title']
            #print "tags:",i['keyword'],"\n" #unicode, raw string
            
            unified=i['keyword'].replace(';',',')
            strlist=unified.split(',')
            
            print i['webService'],"\n",i['title'], "\ncreated on:",created,"\nupdated on:",modified
            
            if created==modified:
                final_list.append({'id':i['identifier'],'title':i['title'],'tag':strlist,'status':'new'})
            else:
                final_list.append({'id':i['identifier'],'title':i['title'],'tag':strlist,'status':'mod'})
            #final_list is a list of dictionaries: the "stack" of info for tweets


# In[7]:

#authenticate with your own twitter application tokens below
twitter = twython_tokens


# In[8]:

#attempt to tweet, may fail if the name is too long, additional error catches may need to be developed here.
try:
    for post in final_list:
        if post['status']=='mod':
            x="A dataset \""+post['title']+"\" has been updated: "+targeturl+"browse?q="+post['id']
            y="A dataset \""+post['title']+"\" has been updated: "
            print len(y)+22
            #len is 32+title+22, 140-54 available for title (86)
            
            twitter.update_status(status=x)
            time.sleep(20)
        elif post['status']=='new':
            x="A new dataset \""+post['title']+"\" has been published: "+targeturl+"resource/"+post['id']
            y=x="A new dataset \""+post['title']+"\" has been published: "
            print len(y)+22
            #len is 37+title+22, 140-59 available for title (81)
            
            twitter.update_status(status=x)
            time.sleep(20) #wait 20 seconds between tweets
except:
    pass


# In[ ]:

#i follow people, run this line to follow and to support us!
#commented out, inactive at this time
#twitter.create_friendship(screen_name='chhsportalnews')
#twitter.create_friendship(screen_name='josephjlei')
#twitter.create_friendship(screen_name='kari_mah')


# In[ ]:

#final_json=json.dumps(final_list)
#encode into json, not currently necessary but can be used to create a http accessible json endpoint


# this block was used to learn datetime lib, disregard
# 
# x=datetime.date(2015,1,1)
# y=datetime.date(2015,1,2)
# print x, y
# z=y-x
# print z #iam timedelta object
# print z.days
# 
# today=datetime.date.today()
# moddate=datetime.date(2015,6,4)
# days_since_mod=today-moddate
# 
# print today
# print moddate
# print days_since_mod.days
