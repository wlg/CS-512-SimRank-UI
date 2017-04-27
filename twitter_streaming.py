#Listener code: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Import the necessary methods from tweepy library
import pdb
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import operator
import os
import pickle
import time

#Variables that contains the user credentials to access Twitter API 
consumer_key = 'S8XtmVeNeYp0F5s3Ba8294rOD'
consumer_secret = '7qbCN3piFWNMixcKCNgf8jNpv1TR71zWyahm5xq7CGE2o4LI0p'
access_token = '848576341700206592-THBDf8XxuL84ok0bwH7YKovFBFKezTS'
access_token_secret = 'qebXmt5NFERtGEnulgxD7MxIf7HvrXO3Tja2V8l1uVvNE'

#saves received tweets to saveFile
class StdOutListener(StreamListener):
  def __init__(self, time_limit=120):
    self.start_time = time.time()
    self.limit = time_limit
    self.saveFile = open('data_'+str(Der)+'_gen_'+str(Ger)+'.json', 'w') #cwd is unnecessary for a new file
    super(StdOutListener, self).__init__()

  def on_data(self, data):
      if (time.time() - self.start_time) < self.limit:
          self.saveFile.write(data)
          self.saveFile.write('\n')
          return True
      else:
          self.saveFile.close()
          return False

  """
  def __init__(self, time_limit=120):
      self.start_time = time.time()
      self.limit = time_limit
      self.saveFile = []
      super(StdOutListener, self).__init__()

  def on_data(self, data):
      if (time.time() - self.start_time) < self.limit:
          self.saveFile.append(data)
          return True
      else:
          return False
  """
#use hashtags from the last iteration to search for related hashtags in the Listener
def get_hashtags(X,Y,initial_filter):
  #X, dataset ID
  #Y, prev gen you get your hashtags from
  cwd = os.getcwd()
  hashtag_freqs = {} #store by hashtag : freq
  f = open(cwd + '\\data_'+str(X)+'_gen_'+str(Y)+'.txt', 'r')
  for tweet in f:
    if '#' in tweet:  #only consider tweets with hashtags
      splitted_tweet = tweet.split()
      for word in splitted_tweet:
        if word[0] == '#' and len(word) > 1: #do not consider words that are just the symbol '#'
          if word in hashtag_freqs:
            hashtag_freqs[word] += 1  #track frequency to take only the top 10 most popular hashtags
          else:
            hashtag_freqs[word] = 1

  #hashtag_freqs.pop('#', None)  #remove '#'
  sorted_freqs = sorted(hashtag_freqs.items(), key=operator.itemgetter(1))  #sort 
  sorted_freqs.reverse()
  most_pop = [pair[0] for pair in sorted_freqs][0:int(round(len(sorted_freqs)/4))] #top 25%

  #get prev hashtags from pickle
  if Y == 0:
    prev_hashtags = initial_filter
  else:
    prev_hashtags = pickle.load(open(cwd + '\\data_'+str(X)+'_hashtag_gen_'+str(Y)+'.p', 'rb'))

  new_filter = list(set(prev_hashtags + most_pop)) #old hashtags plus top 10 new hashtags
  pickle.dump(new_filter, open(cwd + '\\data_'+str(X)+'_hashtag_gen_'+str(Y+1)+'.p', 'wb'))
  return new_filter

def start_listener(Dat,Gen,initial_filter):
  #This handles Twitter authetification and the connection to Twitter Streaming API
  global Der
  Der = Dat
  global Ger
  Ger = Gen
  l = StdOutListener()
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  stream = Stream(auth=auth, listener=StdOutListener(time_limit=15)) #time_limit gives number of seconds Listener is opened for

  if Gen == 0:
    stream.filter(track=initial_filter)
    #stream.filter(track=['#music','#concert','#politics','#trump','#russia','#brexit','#gaming','#gamers','#pc','#xbox'])
  else: #gen 1 and after
    keywords = get_hashtags(Dat,Gen-1,initial_filter)
    stream.filter(track=keywords)

if __name__ == '__main__':
  start_listener()