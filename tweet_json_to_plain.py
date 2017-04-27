#Pandas code: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
import json
import pandas as pd
import pdb, sys, traceback
import matplotlib.pyplot as plt
import numpy as np
import os

def to_plain(X,Y):
  cwd = os.getcwd()
  #X = 9 #dataset ID
  #Y = 0 #current gen
  tweets_data_path = cwd + '\\data_'+str(X)+'_gen_'+str(Y)+'.json'

  k=1
  tweets_data = [] #Can't store too many tweets b/c of memory error
  tweets_file = open(tweets_data_path, "r")
  for line in tweets_file:
      #if k > 20000:
      #    break
      try:
          tweet = json.loads(line) #dictionary object
          if u'text' in tweet: #some tweets don't have the key 'text'
              tweets_data.append(tweet)
      except:
          continue
      k+=1

  tweets = pd.DataFrame() 
  tweets['text'] = map(lambda tweet: tweet['text'], tweets_data) #create 'text' column in dataframe
  tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
  tweets = tweets[tweets['lang'].str.contains("en")==True] #only keep tweets in english

  import io
  f = open(cwd + '\\data_'+str(X)+'_gen_'+str(Y)+'.txt', 'w')
  for line in tweets['text']:
      line = line.replace('\\','') #avoid UnicodeDecodeError: 'unicodeescape' codec can't decode byte
      pre_tweet = line.encode('UTF-8') #convert to unicode
      tweet = pre_tweet.decode('unicode_escape').encode('ascii','ignore') #get rid of unicode artifacts in hashtags
      f.write(tweet.replace('\n',' ') + '\n' + '\n') #'\n' within a tweet may break a single tweet into multiple lines
      #so first remove \n bc we want to keep each tweet on one line

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
