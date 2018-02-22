#!/usr/bin/env python

import sys
import re
import string
import operator

current_info = None
current_count = 0
current_score = 0
info = None
score = None

# Read in each line piped through the command line for mapping
for line in sys.stdin:
    # parse the input we got from Map_SubAuthScore.py
    line = line.strip()
    sub, auth, count, score = line.split('\t')
    count = int(count)
    score = int(score)
    info = str(sub) + ' ' + str(auth)

    if current_info == info:
        current_count += count
        current_score += score
    else:
        if current_info:
            print ("{0}\t{1}\t{2}".format(current_info, current_count, current_score))
        current_info = info
        current_count = count
        current_score = score

# Print the last tuple if the last line should be grouped with the one before it
if current_info == info:
    print ("{0}\t{1}\t{2}".format(current_info, current_count, current_score))