from Tkinter import * #case sensitive
import pdb, traceback, sys
import operator
import numpy
from simrank_fns import *
import os
import pickle
import search_by_ht_fns as hasht
from new_graph import *

#takes ~8 sec to start up, dep on initial graph size
def main():
  #load G, scores and id labels
  root = Tk()
  root.geometry("1200x650")

  cwd = os.getcwd() 
  global Dat 
  Dat = 8 
  Gen = 1 #within tkinter, Y means something different
  data_file = 'data_' + str(Dat) + '_gen_'+ str(Gen)
  header = cwd + '\\' + data_file
  global graph_dict
  global tweet_ids
  global hashtag_ids
  global scores
  graph_dict = pickle.load( open(header +'_bigraph.p', "rb" ) )
  tweet_ids = pickle.load( open(header +'_tweets.p', "rb" ) ) 
  hashtag_ids = pickle.load( open(header +'_hashtags.p', "rb" ) ) 
  scores = pickle.load( open(header +'_scores.p', "rb" ) ) 

  label1 = Label( root, text="Search by a Tweet ID or a hashtag")
  label2 = Label( root, text="Input tweet")
  desc = Label( root, text="'Gather new tweets': Gathers ~50 new tweets using inputted hashtags and store new similarity results. Demo Run time: ~30 secs")
  desc_2 = Label( root, text="Format of 'Gather new tweets' input: Put # before each hashtag. Separate hashtags by space.")
  user_input = Entry(root, bd = 5)
  text = Text(root, height = 20, width = 200)
  scrollb = Scrollbar(root, command=text.yview)
  text['yscrollcommand'] = scrollb.set
  entry_name = Text(root, height = 2, width = 200)
  user_input_2 = Entry(root, bd = 5)

  for tweet in tweet_ids:
    text.insert(INSERT, str(tweet) + ' : ' + tweet_ids[tweet].replace('\n','') + '\n')

  def display_sim_tweets_tin(): #tin means tweet input
    text.delete(1.0, END)
    entry_name.delete(1.0, END)
    low_tweets = compute_sim_tweets(user_input.get(), graph_dict, tweet_ids, hashtag_ids, scores)
    if low_tweets == 'no similar':
      text.insert(INSERT, 'No similar tweets found'+'\n')
    elif low_tweets == 'no new':
      text.insert(INSERT, 'No new tweets found'+'\n')
    elif low_tweets == 'not valid':
      text.insert(INSERT, 'Enter a valid tweet id or hashtag'+'\n')
    else:
      for tweet in low_tweets:
        text.insert(INSERT, tweet + '\n')
    entry_name.delete(1.0, END)
    entry_name.insert(INSERT, get_tweet_from_id(user_input.get(), tweet_ids))

  def display_sim_hashtags_tin():
    text.delete(1.0, END)
    entry_name.delete(1.0, END)
    low_hashtags = compute_sim_hashtags(user_input.get(), graph_dict, tweet_ids, hashtag_ids, scores)
    if low_hashtags == 'no similar':
      text.insert(INSERT, 'No similar hashtags found'+'\n')
    elif low_hashtags == 'no new':
      text.insert(INSERT, 'No new hashtags found'+'\n')
    elif low_hashtags == 'not valid':
      text.insert(INSERT, 'Enter a valid tweet id or hashtag'+'\n')
    else:
      for hashtag in low_hashtags:
        text.insert(INSERT, hashtag + '\n')
    entry_name.delete(1.0, END)
    entry_name.insert(INSERT, get_tweet_from_id(user_input.get(), tweet_ids))

  def display_sim_tweets_hin(): #hin means hashtag input
    text.delete(1.0, END)
    entry_name.delete(1.0, END)
    low_tweets = hasht.compute_sim_tweets(user_input.get(), graph_dict, tweet_ids, hashtag_ids, scores)
    if low_tweets == 'no similar':
      text.insert(INSERT, 'No similar tweets found'+'\n')
    elif low_tweets == 'no new':
      text.insert(INSERT, 'No new tweets found'+'\n')
    elif low_tweets == 'not in':
      text.insert(INSERT, 'Hashtag not found in data'+'\n')
    else:
      for tweet in low_tweets:
        text.insert(INSERT, tweet + '\n')
    entry_name.delete(1.0, END)

  def display_sim_hashtags_hin():
    text.delete(1.0, END)
    entry_name.delete(1.0, END)
    low_hashtags = hasht.compute_sim_hashtags(user_input.get(), graph_dict, tweet_ids, hashtag_ids, scores)
    if low_hashtags == 'no similar':
      text.insert(INSERT, 'No similar hashtags found'+'\n')
    elif low_hashtags == 'no new':
      text.insert(INSERT, 'No new hashtags found'+'\n')
    elif low_hashtags == 'not in':
      text.insert(INSERT, 'Hashtag not found in data'+'\n')
    else:
      for hashtag in low_hashtags:
        text.insert(INSERT, hashtag + '\n')
    entry_name.delete(1.0, END)

  def search_tweets_inputtype(): #outputs similar tweets
    if '#' in user_input.get():
      if len(user_input.get()) == 1:
        text.delete(1.0, END)
        text.insert(INSERT, 'You cannot search by just a single hashtag symbol')
      elif ' ' in user_input.get():
        text.delete(1.0, END)
        text.insert(INSERT, 'Enter a single hashtag with no spaces. For multiple hashtags, refer to: Gather new tweets')  
      else:
        return display_sim_tweets_hin() #search by hashtag
    else:
      display_sim_tweets_tin() #search by tweet

  def search_hashtags_inputtype():  #outputs similar hashtags
    if '#' in user_input.get():
      if len(user_input.get()) == 1:
        text.delete(1.0, END)
        text.insert(INSERT, 'You cannot search by just a single hashtag symbol')
      elif ' ' in user_input.get():
        text.delete(1.0, END)
        text.insert(INSERT, 'Enter a single hashtag with no spaces. For multiple hashtags, refer to: Gather new tweets')  
      else:
        return display_sim_hashtags_hin() #search by hashtag

    else:
      display_sim_hashtags_tin() #search by tweet

  def show_tweet_ids():
    text.delete(1.0, END)
    for tweet in tweet_ids:
      text.insert(INSERT, str(tweet) + ' : ' + tweet_ids[tweet].replace('\n','') + '\n')
    entry_name.delete(1.0, END)

  def show_hashtags():
    text.delete(1.0, END)
    for hashtag in hashtag_ids:
      text.insert(INSERT, hashtag_ids[hashtag].replace('\n','') + '\n')
    entry_name.delete(1.0, END)

  def gather_new():
    global Dat
    global graph_dict
    global tweet_ids
    global hashtag_ids
    global scores
    passed = True
    splitted = user_input.get().split()
    for word in splitted:
      if word[0] != '#':
        text.delete(1.0, END)
        text.insert(INSERT, 'Enter a valid set of hashtags. See above description.'+'\n')
        passed = False
        break
    if passed:
      Dat = gather_new_data(Dat,splitted)  #assume at start, there is only one dataset (dataset 8)
      data_file = 'data_' + str(Dat) + '_gen_'+ str(Gen)
      header = cwd + '\\' + data_file
      graph_dict = pickle.load( open(header +'_bigraph.p', "rb" ) )
      tweet_ids = pickle.load( open(header +'_tweets.p', "rb" ) ) 
      hashtag_ids = pickle.load( open(header +'_hashtags.p', "rb" ) ) 
      scores = pickle.load( open(header +'_scores.p', "rb" ) ) 
      text.delete(1.0, END)
      for tweet in tweet_ids:
        text.insert(INSERT, str(tweet) + ' : ' + tweet_ids[tweet].replace('\n','') + '\n')
      entry_name.delete(1.0, END)

  def switch_data():
    global Dat
    global graph_dict
    global tweet_ids
    global hashtag_ids
    global scores
    user_dat = user_input_2.get()
    data_file = 'data_' + str(user_dat) + '_gen_'+ str(Gen)
    header = cwd + '\\' + data_file
    if os.path.exists(header+'_scores.p') == True:
      Dat = int(user_dat)
      graph_dict = pickle.load( open(header +'_bigraph.p', "rb" ) )
      tweet_ids = pickle.load( open(header +'_tweets.p', "rb" ) ) 
      hashtag_ids = pickle.load( open(header +'_hashtags.p', "rb" ) ) 
      scores = pickle.load( open(header +'_scores.p', "rb" ) ) 
      text.delete(1.0, END)
      for tweet in tweet_ids:
        text.insert(INSERT, str(tweet) + ' : ' + tweet_ids[tweet].replace('\n','') + '\n')
      entry_name.delete(1.0, END)
    else:
      text.delete(1.0, END)
      text.insert(INSERT, 'Not a valid dataset ID. Refer to: Show dataset IDs')
      entry_name.delete(1.0, END)

  def show_data():
    text.delete(1.0, END)
    for i in range(8,Dat+1):
      text.insert(INSERT,str(i)+'\n')
    entry_name.delete(1.0, END)

  search_tweets_button = Button(root, text ="Find similar tweets", command = search_tweets_inputtype)
  search_hts_button = Button(root, text ="Find similar hashtags", command = search_hashtags_inputtype)
  new_button = Button(root, text ="Gather new tweets", command = gather_new)
  tweet_ids_button = Button(root, text ="Show tweet ID inputs", command = show_tweet_ids)
  hashtag_button = Button(root, text ="Show hashtag inputs", command = show_hashtags)
  showdata_button = Button(root, text ="Show dataset IDs", command = show_data)

  switch_data_button = Button(root, text ="Switch datasets", command = switch_data)

  entry_name.pack(side = BOTTOM) #side is case sensitive
  label2.pack(side = BOTTOM)
  switch_data_button.pack(side = TOP)
  user_input_2.pack(side = TOP)
  text.pack()
  desc.pack()
  desc_2.pack()
  scrollb.pack(side = RIGHT, fill = Y)
  label1.pack(side = LEFT)
  user_input.pack(side = LEFT)
  search_tweets_button.pack(side = LEFT)
  search_hts_button.pack(side = LEFT)
  new_button.pack(side = LEFT)
  tweet_ids_button.pack(side = LEFT)
  hashtag_button.pack(side = LEFT)
  showdata_button.pack(side = LEFT)
  root.mainloop()

#given an input tweet, find similar tweets and hashtags
def get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, similar_tweets):
  similar_hashtags = []
  for (tweet, score) in similar_tweets:
    hashtags = graph_dict[tweet] #for hashtags of that tweet
    for h in hashtags:
      if h not in input_tweet_hashtags and h not in similar_hashtags: #find relative complement and prevent duplicates
        similar_hashtags.append(h)
  similar_hashtags = list(set(similar_hashtags))

  similar_hashtags_strings = []
  if similar_hashtags == []:
    return 'no new'
  else:
    for h in similar_hashtags:
      similar_hashtags_strings.append(str(hashtag_ids[h]))
  return similar_hashtags_strings

def get_tweets(graph_dict, input_tweet, tweet_ids, similar_tweets):
  similar_tweet_strings = []
  if similar_tweets == []:
    return 'no new'
  else:
    for ID in similar_tweets: #can't use id b/c built-in fn; var are case sensitive
      tweet = tweet_ids[ID[0]]
      similar_tweet_strings.append(tweet)
  return similar_tweet_strings

def get_tweet_from_id(tweet_id, tweet_ids):
  tweet_id = int(tweet_id)
  return tweet_ids[tweet_id]

def compute_sim(input_tweet, graph_dict, tweet_ids, hashtag_ids, scores):
  #from user input, get input_tweet (during create_graph, you assigned an id to input_tweet, so use that)
  input_tweet_hashtags =  graph_dict[input_tweet] #get hashtag neighbors of input tweet
  related_tweets = {}
  stop_signal = 'on'
  for (x,y) in scores: 
    if x != y:
      if x == input_tweet:  #only eval x b/c pairs are symmetrical
        stop_signal = 'off'
        related_tweets[y] = scores[(x,y)] #get all tweets w/ a score > 0 relative to input_tweet
  if stop_signal == 'on':
    return 'no similar'

  sorted_rel_scores = sorted(related_tweets.items(), key=operator.itemgetter(1))
  sorted_rel_scores.reverse()

  #sort hashtags into categories of scores. The % are arbitrary, for now. Don't output too many options for the user to read
  #High: top 30%. Low: 30-40%
  #high = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .3)]
  #low = sorted_rel_scores[int(len(sorted_rel_scores) * .3) : int(len(sorted_rel_scores) * .4)]
  low = sorted_rel_scores[0 : int(len(sorted_rel_scores) * .4)]
  return low

def compute_sim_tweets(search_term, graph_dict, tweet_ids, hashtag_ids, scores):
  if search_term.isdigit() == False:
    return 'not valid'
  elif int(search_term) not in graph_dict:
    return 'not valid'
  input_tweet = int(search_term) #compute outside of compute_sim b/c it's used as input in get_tweets
  low = compute_sim(input_tweet, graph_dict, tweet_ids, hashtag_ids, scores)
  if low == 'no similar':
    return 'no similar'
  low_tweets = get_tweets(graph_dict, input_tweet, tweet_ids, low)
  return low_tweets

def compute_sim_hashtags(search_term, graph_dict, tweet_ids, hashtag_ids, scores):
  if search_term.isdigit() == False:
    return 'not valid'
  elif int(search_term) not in graph_dict:
    return 'not valid'
  input_tweet = int(search_term)
  low = compute_sim(input_tweet, graph_dict, tweet_ids, hashtag_ids, scores)
  if low == 'no similar':
    return 'no similar'
  input_tweet_hashtags =  graph_dict[input_tweet]
  low_hashtags = get_hashtags(graph_dict, input_tweet_hashtags, hashtag_ids, input_tweet, low)
  return low_hashtags

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)

