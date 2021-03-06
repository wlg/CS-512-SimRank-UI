import pdb, traceback, sys
import time
import operator
import numpy
from simrank_fns import *
import os
import pickle

#The text dumping code is commented out in output_scores to make the function run faster for the 'Gather new tweets' job in the UI
def output_scores(X,Y):
  cwd = os.getcwd()
  
  data_file = 'data_' + str(X) + '_gen_'+ str(Y)
  limit = 5000 #limit on number of nodes in graph (both tweets and hashtags). Total nodes usually ~3500 for Listener running for 5 min

  #get graph adj list, adj matrix, and the dicts that pair tweets w/ id and hashtags w/ id
  header = cwd + '\\' + data_file
  graph_dict, adj_matrix, tweet_ids, hashtag_ids, index_id = create_graph(header +'.txt', limit) 
  """
  fn_1 = header + '_bigraph.txt'
  sorted_graph = sorted(graph_dict.items())
  make_list_tuples(fn_1,sorted_graph)
  
  fn_2 = header + '_tweets.txt'
  make_list(fn_2,tweet_ids)

  fn_3 = header + '_hashtags.txt'
  sorted_hashtag_ids = collections.OrderedDict(sorted(hashtag_ids.items()))
  make_list(fn_3, sorted_hashtag_ids)
  """
  #store dict option so it can be loaded into hashtag_search.py later
  pickle.dump(graph_dict, open(header + '_bigraph.p', "wb" ))
  pickle.dump(tweet_ids, open(header + '_tweets.p', "wb" ))
  pickle.dump(hashtag_ids, open(header + '_hashtags.p', "wb" ))

  #calculate summed even powers of adj matrix to find which node pairs are within path of len K away
  am_sq = numpy.dot(adj_matrix, adj_matrix)
  test = am_sq
  sums = test
  #start_time = time.time()
  for i in range(1): 
    test = numpy.dot(test,am_sq) #range(k) means up to G^(2^(k+1))
    sums = sums + test
  #time_pt_1 = time.time() - start_time
  #print("Sum even powers of adj matrix: %s seconds" % (time_pt_1))
  for i in range(len(sums)):
    if numpy.count_nonzero(sums[i]) > 0:  #if there exists nonzeros in node
      sums[i,i] += 1 #make the diagonal entry of sums be nonzero so that it is included in id_nonzeros
  
  #get nonzeros of summed even powers of adj matrix to find node pairs which have decently big simrank scores. saves memory.
  #first convert each node into an index #. then convert back. may req 2 hashtables
  nonzeros = numpy.transpose(numpy.nonzero(sums))
  id_nonzeros = index_to_id(nonzeros, index_id)
  
  scores, sorted_scores = simrank(graph_dict, id_nonzeros) #run simrank to get node pair scores
  #fn_4 = header + '_scores.txt'
  #make_list_tuples(fn_4, sorted_scores)
  pickle.dump(scores, open(header + '_scores.p', "wb" ))
  #time_pt_2 = time.time() - start_time
  #print("Calculate Simrank and store scores: %s seconds" % (time_pt_2 - time_pt_1))

if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
