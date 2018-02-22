#!/usr/bin/env python

import sys
import re
import string
import operator

#### COMPILE REGULAR EXPRESSIONS ####
# Precompiling the expressions results in dramatic
# performance improvements since the expressions
# will be evaluated millions of times
rgx_auth = re.compile('"author":')
rgx_subreddit = re.compile('"subreddit":')
rgx_score = re.compile('"score":')

rgx_endpoint_slash = re.compile('\",')
rgx_endpoint_bracket = re.compile('\"}')
rgx_endpoint_digit = re.compile('\d{1,}')
rgx_endpoint_break = re.compile('}\n')

def get_author(line,rgx_auth,rgx_endpoint_slash,rgx_endpoint_bracket):
    # Helper function to get the author out of the line
    # This is an unordered line of text, so the position will vary
    
    subreddit_startpoint = rgx_auth.search(line).end() + 1
    
    # In the event that the subreddit is the last element of the line
    # we will have to search for a different pattern: '"}'
    
    if rgx_endpoint_slash.search(line[subreddit_startpoint:]):
        subreddit_endpoint = rgx_endpoint_slash.search(line[subreddit_startpoint:]).end()-2
    else:
        subreddit_endpoint = rgx_endpoint_bracket.search(line[subreddit_startpoint:]).end()-2

    return (line[subreddit_startpoint:subreddit_startpoint+subreddit_endpoint])

def get_subreddit(line,rgx_subreddit,rgx_endpoint_slash,rgx_endpoint_bracket):
    # Helper function to get the subreddit out of the line
    # This is an unordered line of text, so the position will vary
    
    subreddit_startpoint = rgx_subreddit.search(line).end() + 1
    
    # In the event that the subreddit is the last element of the line
    # we will have to search for a different pattern: '"}'
    if rgx_endpoint_slash.search(line[subreddit_startpoint:]):
        subreddit_endpoint = rgx_endpoint_slash.search(line[subreddit_startpoint:]).end()-2
    else:
        subreddit_endpoint = rgx_endpoint_bracket.search(line[subreddit_startpoint:]).end()-2

    return (line[subreddit_startpoint:subreddit_startpoint+subreddit_endpoint])

def get_score(line,rgx_score,rgx_endpoint_digit,rgx_endpoint_break):
    # Helper function to get the score out of the line
    # This is an unordered line of text, so the position will vary
    
    subreddit_startpoint = rgx_score.search(line).end() 
    
    # In the event that the subreddit is the last element of the line
    # we will have to search for a different pattern: '"}'
    # \d{1,}   This finds a digit at least 1 character or longer
    if rgx_endpoint_digit.search(line[subreddit_startpoint:]):
        subreddit_endpoint = rgx_endpoint_digit.search(line[subreddit_startpoint:]).end()
    else:
        subreddit_endpoint = rgx_endpoint_break.search(line[subreddit_startpoint:]).end()

    return (line[subreddit_startpoint:subreddit_startpoint+subreddit_endpoint])

def subreddit_author_score(line,rgx_auth,rgx_endpoint_slash,rgx_endpoint_bracket,
                           rgx_subreddit,rgx_score,rgx_endpoint_digit,rgx_endpoint_break):
    
    # get the author first to determine if subsequent fields are needed
    auth = get_author(line,rgx_auth,rgx_endpoint_slash,rgx_endpoint_bracket).lower()
    
    # ignore comments/lines where the author/comment has been deleted
    # as this has no information we can use
    if auth != '[deleted]':
        sub = get_subreddit(line,rgx_subreddit,rgx_endpoint_slash,rgx_endpoint_bracket).lower()
        score = int(get_score(line,rgx_score,rgx_endpoint_digit,rgx_endpoint_break))
        #print("{0} {1}\t1".format(sub,auth))
        #return "({0},{1},1)".format(sub,auth)
        return (sub,auth,1,score)
    else:
        return ("None","None",1,0)

# Read in each line piped through the command line for mapping
mapped_output = []
for line in sys.stdin:
    sub, auth, count, score = subreddit_author_score(line,rgx_auth,rgx_endpoint_slash,rgx_endpoint_bracket,
                                                     rgx_subreddit,rgx_score,rgx_endpoint_digit,rgx_endpoint_break)
    if sub != 'None' and auth != 'None':
        mapped_output.append((sub, auth, count, score))
        #print ("{0}\t{1}\t{2}\t{3}".format(sub, auth, count, score))

# In place internal sorting by two keys: the subreddit and the author
mapped_output.sort(key = operator.itemgetter(0,1))

for i in mapped_output:
    #print (i)
    print ("{0}\t{1}\t{2}\t{3}".format(i[0], i[1], i[2], i[3]))