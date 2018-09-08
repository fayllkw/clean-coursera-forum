"""
sorting.py: sort the merged answer and question by certain order.
Ordering requirement:
put things in a thread together; put nested answers under the parent answer;
order the threads by time; order posts in each thread by time.
Also, remove posts by instructors (mentor, teaching_staff ...) after sorting.
"""

import numpy as np
import pandas as pd
import os

MEMBERSHIP_LOCATION = "AR-VR-Teach-Out-Discussion/course_memberships.csv"
DATA_DIR = "processed data"
FILE = "merged_question_and_answer.csv"
CUR_DIR = os.path.split(os.path.realpath(__file__))[0]

# read in the merged file
dat = pd.read_csv(CUR_DIR + "/" + DATA_DIR + "/" + FILE, encoding = "ISO-8859-1")

# print(len(dat))

# add ranking for questions according to the timestamp
questions = dat[dat.isna()['discussion_answer_id']].copy()
questions['rank'] = questions['post_created_ts'].rank(ascending = True)
questions = questions[["discussion_question_id", "rank"]]

# print(len(questions))
# print(questions)

# apply this rank to the whole dataframe
# (so that the posts could be ordered by the question created time by question group)
dat = dat.merge(questions)

# print(len(dat))

# find the parents of those nested questions
nested = set(dat["discussion_answer_parent_discussion_answer_id"])
nested.remove(np.nan)
nested.remove("i0NE8jExEeis-Q7qXMzcHg") # this seems to be a bad record
# add the ids of themselves for those parents questinos in parent column, so that we can sort
for aid in nested:
    mask = (dat["discussion_answer_id"]==aid)
    row_index = np.where(mask == True)[0][0]
    dat.loc[row_index, "discussion_answer_parent_discussion_answer_id"] = aid

# sort
# first put the same thread together(also nested questiosn together)
# and then sort by time (first by questions created time, and then within each thread, by answer created time)
dat = dat.sort_values(['rank','discussion_question_id','discussion_answer_parent_discussion_answer_id','post_created_ts'],
                      na_position="first")
dat = dat.reset_index(drop = True)

print(len(dat))

# remove the ids of themselves for those parents questinos in parent column
for aid in nested:
    mask = (dat["discussion_answer_id"]==aid)
    row_index = np.where(mask == True)[0][0]
    dat.loc[row_index, "discussion_answer_parent_discussion_answer_id"] = np.nan

# remove the rank column
dat.drop("rank", axis = 1, inplace = True)

# print(len(dat))

# remove posts by instructors (mentor, teaching_staff ...)
membership = pd.read_csv(CUR_DIR + "/" + MEMBERSHIP_LOCATION, encoding = "ISO-8859-1")
LEARNERS = ["NOT_ENROLLED", "PRE_ENROLLED_LEARNER", "BROWSER", "LEARNER"]
learners = membership[membership["course_membership_role"].isin(LEARNERS)]
dat = dat[dat["umich_user_id"].isin(learners["umich_user_id"])]

# print(len(dat))

# output
dat.to_csv(CUR_DIR + "/" + DATA_DIR + "/" + "ordered_question_and_answer.csv",  index = False, encoding = "ISO-8859-1")