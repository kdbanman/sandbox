#!/usr/bin/env python
#-*- coding: Utf-8 -*-

import json
import urllib2
import codecs



def start(url):

  compage = urllib2.urlopen(url).read()
  x = json.loads(compage)['data']['children']
  comcount = len(x) - 1
  
  comfile = open("%s.txt"%username, 'a')
  for i in range(0,comcount):
    
      rawdata = "Thread Title: %s\nUrl: http://www.reddit.com/r/%s/%s\n\nComment:\n%s\n\n~------------------------------------------~ \n\n"  %(x[i]['data']['link_title'], x[i]['data']['subreddit'], x[i]['data']['link_id'].replace("t3_","").replace("t1_",""), x[i]['data']['body'])
      
      comments = rawdata.encode('utf-8')
      print comments
    
      comfile.write(comments)
  
  nextpageurl = "http://www.reddit.com/user/%s/comments/.json?count=25&after=%s" %(username, x[i]['data']['name'])
  comfile.close()
    
  if comcount >= 24:
    start(nextpageurl)
  else:
    print "Either finished or messed up somewhere. Check the txt file"

global username 
username =  raw_input("Username:")
comurl = "http://www.reddit.com/user/%s/comments/.json" %username
start(comurl)
