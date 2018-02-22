# RelatedSubreddits #
Find which subreddits are related by user comments

# Preliminaries #
This project is the result of class work done for my masters degree in analytics. 
The focus was to create a project to utilize map/reduce methodologies to work with Hadoop streaming.
The mapper and reducer are designed to read the data via the command line as if it were streaming. 
Through the command line, i wrote the data to another file that is then analyzed in the Relational Subreddits notebook.

# Purpose #
Map which subreddits users comment on, their associated comment scores (positive or negative), and understand how individual subreddits are related to each other based on user actions. 

# Data #
Data was obtained using Google Big Query for all public comments made on Reddit in April, 2017 and can be obtained here:
https://bigquery.cloud.google.com/table/fh-bigquery:reddit_comments.2017_04

The zipped file is ~7.5 Gb and extracts to ~41Gb. There are roughly 77.5 million comments in the dataset.
Each line is a text representation of a python dictionary where each entry relates to a single comment made by a user. The keys are undordered but each entry contains the following fields:

subreddit: string
edited: boolean
controversiality: int
can_gild: boolean
author_flair_css_class: string
subreddit_id: string
parent_id: string
body: string
score: int
author: string
gilded: int
retrieved_on: int
link_id: string
stickied: boolean
id: string
created_utc: int
author_flair_text: string
distinguished: string
