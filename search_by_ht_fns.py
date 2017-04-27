import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle

#given an input tweet, find similar tweets and hashtags

def get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, similar_hashtags):
  similar_tweets = []
  for (hashtag, score) in similar_hashtags:
    tweets = graph_dict[hashtag] #for hashtags of that tweet
    for t in tweets:
      if t not in input_hashtag_tweets and t not in similar_tweets: #find relative complement (no tweets contain that hashtag) and prevent duplicates
        similar_tweets.append(t)
  similar_tweets = list(set(similar_tweets))

  similar_tweet_strings = []
  if similar_tweets == []:
    return 'no new'
  else:
    for t in similar_tweets:
      similar_tweet_strings.append(str(tweet_ids[t]))
  return similar_tweet_strings

def get_hashtags(graph_dict, input_hashtag, hashtag_ids, similar_hashtags):
  similar_hashtag_strings = []
  if similar_hashtags == []:
    return 'no new'
  else:
    for ID in similar_hashtags: #can't use id b/c built-in fn; var are case sensitive
      hashtag = hashtag_ids[ID[0]]
      similar_hashtag_strings.append(hashtag)
  return similar_hashtag_strings

def compute_sim(input_hashtag, graph_dict, tweet_ids, hashtag_ids, scores):
  related_hashtags = {}
  stop_signal = 'on'
  for (x,y) in scores: 
    if x != y:
      if x == input_hashtag:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_hashtags[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet
  if stop_signal == 'on':
    return 'no similar'

  sorted_rel_scores = sorted(related_hashtags.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()

  #sort hashtags into categories of scores. The % are arbitrary, for now.
  #High: top 20%. Mid: 20-30%. Low: 30-40%
  #high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .2)]
  #low = sorted_rel_scores[int(len(sorted_rel_scores) * .3) : int(len(sorted_rel_scores) * .4)]
  low = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .4)]
  return low

def compute_sim_tweets(search_term, graph_dict, tweet_ids, hashtag_ids, scores):
  #from user input, get input_hashtag
  rev_hashtag_ids = {v: k for k, v in hashtag_ids.iteritems()} #reverse hashtag_ids to get hashtag : id
  if search_term not in rev_hashtag_ids:
    return 'not in'
  input_hashtag = int(rev_hashtag_ids[search_term]) #get id
  if input_hashtag not in graph_dict:
    return 'not in'
  input_hashtag_tweets =  graph_dict[input_hashtag] #get hashtag neighbors of input tweet
  
  low = compute_sim(input_hashtag, graph_dict, tweet_ids, hashtag_ids, scores)
  if low == 'no similar':
    return 'no similar'
  low_tweets = get_tweets(graph_dict, input_hashtag_tweets, tweet_ids, input_hashtag, low)
  return low_tweets

def compute_sim_hashtags(search_term, graph_dict, tweet_ids, hashtag_ids, scores):
  #from user input, get input_hashtag
  rev_hashtag_ids = {v: k for k, v in hashtag_ids.iteritems()} #reverse hashtag_ids to get hashtag : id
  if search_term not in rev_hashtag_ids:
    return 'not in'
  input_hashtag = int(rev_hashtag_ids[search_term]) #get id
  if input_hashtag not in graph_dict:
    return 'not in'

  low = compute_sim(input_hashtag, graph_dict, tweet_ids, hashtag_ids, scores)
  if low == 'no similar':
    return 'no similar'
  low_hashtags = get_hashtags(graph_dict, input_hashtag, hashtag_ids, low)
  return low_hashtags
