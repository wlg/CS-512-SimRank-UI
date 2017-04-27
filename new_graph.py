from twitter_streaming import *
from tweet_json_to_plain import *
from simrank_fns import *
from get_scores import *

def gather_new_data(Dat,initial_filter):
	Dat += 1 #new dataset ID
	start_listener(Dat,0,initial_filter)
	to_plain(Dat,0)
	start_listener(Dat,1,initial_filter)
	to_plain(Dat,1)
	output_scores(Dat,1)
	return Dat