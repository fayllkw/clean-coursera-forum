"""
removing non-en.py:
Use langid to add language information for each post; remove empty and non-en posts.
(not absolutely accurate, especially for short or mixed posts)
Show posts count information.
Output three csv files:
all posts with language label; posts without instructors with language label;
english and non-empty posts without instructors.
"""

import pandas as pd
import os
import langid

def detect_language(string, word_count):
    """
    customized language detection (based on langid)
    langid got difficulty in classifying short posts,
    such as "Hi Laurensia. Welcome!", "Hello guys", “no questions”.
    Since the linguistic context of the forum is generally English,
    I just classify all posts shorter than 7 words as English.
    The number 7 is decided by observation, which should be decided
    more scientifically if generalization is needed.
    """
    if word_count < 7: return 'en'
    else: return langid.classify(string)[0]

def get_language_label(merged):
    return merged.apply(lambda row: detect_language(row['post_content'], row['post_content_length']), axis=1)

if __name__ == '__main__':
    # settings
    ARVR = 'ARVR'
    Civil = 'Civil'
    Fake = 'Fake'
    Privacy = 'Privacy'
    COURSE = Privacy
    DATA_DIR = "processed data/" + COURSE
    FILE = "merged_question_and_answer.csv"
    FILE_WO_INSTRUCTOR = "merged_question_and_answer_without_instructor.csv"
    CUR_DIR = os.path.split(os.path.realpath(__file__))[0]

    # read in the merged file
    merged = pd.read_csv(CUR_DIR + "/" + DATA_DIR + "/" + FILE, encoding ="ISO-8859-1")
    merged_wo_instructor = pd.read_csv(CUR_DIR + "/" + DATA_DIR + "/" + FILE_WO_INSTRUCTOR, encoding ="ISO-8859-1")
    merged_wo_instructor = merged_wo_instructor[["discussion_answer_id", "discussion_question_id"]]

    # add language column
    merged['language'] = get_language_label(merged)
    print('# of total posts: ', len(merged))
    # output the full dataframe with language info
    merged.to_csv(CUR_DIR + "/" + DATA_DIR + "/" + "merged_question_and_answer_with_language.csv", index = False, encoding = "ISO-8859-1")

    # output the previous dataframe except for instructor posts
    labeled_no_instructor = merged.merge(merged_wo_instructor, how='right')
    print('# of total posts by learners: ', len(labeled_no_instructor))
    labeled_no_instructor.to_csv(CUR_DIR + "/" + DATA_DIR + "/" + "merged_question_and_answer_with_language_without_instructor.csv",
                   index = False, encoding = "ISO-8859-1")

    #cget rid of empty answers
    merged = merged[merged["post_content_length"] != 0]
    # get all the posts (no instructor) in english and output
    english_only = merged[merged['language'] == 'en']
    english_only_wo_instructor = english_only.merge(merged_wo_instructor, on=["discussion_answer_id", "discussion_question_id"])
    print('# of english posts: ', len(english_only))
    print('# of english posts by learners: ', len(english_only_wo_instructor))
    english_only_wo_instructor.to_csv(CUR_DIR + "/" + DATA_DIR + "/" + "english_only_question_and_answer_without_instructor.csv",
                        index = False, encoding = "ISO-8859-1")












