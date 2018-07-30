"""
merging.py:
get rid of unnecessary columns; merge answers and questions;
also get a version of merged dataframe without instructor posts.
Here's also a function could be used to remove unwanted sessions.
"""

import pandas as pd
import os
from dateutil.parser import parse
import datetime as dt

def merge_questions_and_answers(questions, answers):
    """
    Merge and only keep useful columns.
    :param questions: the questions dataframe in neat format.
    :param answers: the answers dataframe in neat format.
    :return: a dataframe including both questions and answers.
    """
    # remove unused columns in questions
    questions.drop(["discussion_question_context_type", "course_id", "course_module_id", "course_item_id",
                    "discussion_forum_id", "country_cd", "group_id", "discussion_question_updated_ts"],
                   axis=1, inplace=True)
    # add a column, reorder and rename the columns in questions
    questions = questions.reindex(columns=["discussion_answer_id", "discussion_question_id",
                                           "discussion_answer_parent_discussion_answer_id", "umich_user_id",
                                           "discussion_question_title", "discussion_question_details",
                                           "discussion_question_created_ts", "question_details_length"])
    questions.columns = ["discussion_answer_id", "discussion_question_id", "discussion_answer_parent_discussion_answer_id",
                         "umich_user_id", "discussion_question_title", "post_content", "post_created_ts",
                         "post_content_length"]
    # repeat the similar steps for answers
    answers.drop(["course_id", "discussion_answer_updated_ts"], axis=1, inplace=True)
    answers = answers.reindex(columns=["discussion_answer_id", "discussion_question_id",
                                       "discussion_answer_parent_discussion_answer_id", "umich_user_id",
                                       "discussion_question_title", "discussion_answer_content",
                                       "discussion_answer_created_ts", "answer_content_length"])
    answers.columns = ["discussion_answer_id", "discussion_question_id", "discussion_answer_parent_discussion_answer_id",
                       "umich_user_id", "discussion_question_title", "post_content", "post_created_ts",
                       "post_content_length"]
    # add these two dataframes together
    frames = [questions, answers]
    merged = pd.concat(frames)
    return merged

def remove_instructors(membership, merged):
    """
    Remove posts by instructors (mentors, teaching_staff ...).
    :param membership: the membership dataframe.
    :param merged: the merged questiosn and answers.
    :return:
    """
    LEARNERS = ["NOT_ENROLLED", "PRE_ENROLLED_LEARNER", "BROWSER", "LEARNER"]
    learners = membership[membership["course_membership_role"].isin(LEARNERS)]
    merged_no_instructor = merged[merged["umich_user_id"].isin(learners["umich_user_id"])]
    return merged_no_instructor

def remove_other_senssion_learners(membership, begin, end):
    """
    Try to remove leanres of uninterested sessions by filtering by registering timestamp.
    (May not be fully correct, as there're some pre_enrolled cases).
    :param membership: the membership dataframe.
    :param begin: timestamp indicating the beginning of the interested period (inclusive).
    :param end: timestamp indicating the end of the interested period (inclusive).
    :return a filtered membership dataframe.
    """
    filtered_membership = membership[(membership['course_membership_ts']<=end)
                                     & (membership['course_membership_ts']>=begin)
    ]
    print("# of total learners in the first run: ",
          sum(filtered_membership["course_membership_role"].isin([ "PRE_ENROLLED_LEARNER",  "LEARNER"])))
    return filtered_membership

if __name__ == '__main__':
    # setting
    ARVR = 'ARVR'
    Civil = 'Civil'
    Fake = 'Fake'
    Privacy = 'Privacy'
    COURSE = Privacy
    DATA_DIR = "processed data/" + COURSE
    ANSWER = "processed_discussion_answers.csv"
    QUESTION = "processed_discussion_questions.csv"
    MEMBERSHIP = COURSE + "/course_memberships.csv"
    CUR_DIR = os.path.split(os.path.realpath(__file__))[0]

    # read in questions
    questions = pd.read_csv(CUR_DIR + "/" + DATA_DIR + "/" + QUESTION, encoding="ISO-8859-1")
    # read in answers
    answers = pd.read_csv(CUR_DIR + "/" + DATA_DIR + "/" + ANSWER, encoding="ISO-8859-1")
    # merge them
    merged = merge_questions_and_answers(questions, answers)
    # output
    merged.to_csv(CUR_DIR + "/" + DATA_DIR + "/merged_question_and_answer.csv", index=False, encoding = "ISO-8859-1")

    # read in memberships
    membership = pd.read_csv(CUR_DIR + "/" + MEMBERSHIP, encoding = "ISO-8859-1")
    # count number of learners
    print("# of total learners in {}: {}".
          format(COURSE, sum(membership["course_membership_role"].isin([ "PRE_ENROLLED_LEARNER",  "LEARNER"]))))
    # remove instructor posts
    merged_no_instructor = remove_instructors(membership, merged)
    print('# of posts by learner: ', len(merged_no_instructor))
    # output without instructor
    merged_no_instructor.to_csv(CUR_DIR + "/" + DATA_DIR + "/merged_question_and_answer_without_instructor.csv", index=False,
                  encoding="ISO-8859-1")

    # # remove learners in certain time period
    # membership['course_membership_ts'] = membership['course_membership_ts'].apply(parse)
    # begin_date = membership['course_membership_ts'].min()
    # end_date = dt.datetime(2018,1,1)
    # membership_filtered = remove_other_senssion_learners(membership,begin_date,end_date)

