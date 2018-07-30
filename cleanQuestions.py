"""
cleaning questions.py: cleans "discussion_questions.csv", and outputs "processed_discussion_questions.csv".
It restores the broken format; removes HTML tags in answer contents; adds column "question_details_length".
"""

import numpy as np
import pandas as pd
import os

def modifyRow(df, prev, totalColumns, restColumns):
    """
    The exactly same function in "cleaning answers.py".
    """
    # find the row(s) with non-NAN values in the last column
    mask = df.iloc[:,-1].notnull()
    target_row_numbers = np.where(mask == True)[0]
    if np.any(mask):
        for i in range(target_row_numbers.size):
            target_row_number = target_row_numbers[i]
            # see if this row has already been modified
            if target_row_number in prev:
                continue
            # concatenate the question details and put it in the right place
            temp_str = df.iloc[target_row_number,3]
            for j in range(4, df.shape[1]-restColumns):
                temp_str += ' ' + df.iloc[target_row_number, j]
            df.iloc[target_row_number,3] = temp_str
            # put other columns in to the right places
            for j in range(4, totalColumns):
                df.iloc[target_row_number,j] = df.iloc[target_row_number, df.shape[1]-totalColumns+j]
    df.drop(df.columns[-1], axis = 1, inplace = True)
    return target_row_numbers

def clean_questions(df):
    """
    Clean the dataframe of questions. Remove HTML tags in posts. Add a column indicating the post length.
    Almost the same as clean_answers in "cleaning answers.py", except for the column names in the dataframe.
    :param df: a dataframe directly got from the "discussion_questions.csv" file
    :return: the discussion questions in a neat format
    """
    NUMBER_OF_COLUMNS = 13
    NUMBER_OF_REST_COLUMNS = 9
    # Use a loop to modify the whole data frame
    prev = np.array([])
    while (df.shape[1] > NUMBER_OF_COLUMNS):
        prev = np.unique(np.concatenate([prev, modifyRow(df, prev, NUMBER_OF_COLUMNS, NUMBER_OF_REST_COLUMNS)]))
    # remove HTML tags
    df["discussion_question_details"] = df["discussion_question_details"].str.replace(r'<[\w\s\\/=\-?:."]*>', ' ')
    df["discussion_question_details"] = df["discussion_question_details"].str.replace(r'\\\\n', '')
    # let strings only left spaces become empty
    df["discussion_question_details"] = df["discussion_question_details"].apply(
        lambda string: '' if string.isspace() else string)
    # add post length of each answer
    df["question_details_length"] = df["discussion_question_details"].apply(lambda s: len(s.split()))
    return df

if __name__ == '__main__':
    # settings
    ARVR = 'ARVR'
    Civil = 'Civil'
    Fake = 'Fake'
    Privacy = 'Privacy'
    COURSE = Privacy
    PROCESSED_DIR = "processed data"
    MEMBERSHIP = "course_memberships.csv"
    TARGET_FILE = "discussion_questions.csv"
    CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
    # import data
    questions = pd.read_csv(CUR_DIR + "/" + COURSE + "/" + TARGET_FILE, encoding="ISO-8859-1")
    # clean it
    questions = clean_questions(questions)
    # output the cleaned data
    questions.to_csv(CUR_DIR + "/" + PROCESSED_DIR + "/" + COURSE + "/processed_" + TARGET_FILE, index = False, encoding ="ISO-8859-1")