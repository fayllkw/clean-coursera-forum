"""
cleaning answers.py: cleans "discussion_answer.csv", and outputs "processed_discussion_answers.csv".
It restores the broken format; removes HTML tags in answer contents; adds column "answer_content_length".
"""

import numpy as np
import pandas as pd
import os

def modifyRow(df, prev, totalColumns, restColumns):
    """
    Change the row(s) into correct format, and delete the very last column.
    :param df: a data frame containing discussion forum records (either answers or questions)
    :param prev: a list of index of those rows have already been modified
    :param totalColumns: the proper number of the columns
    :param restColumns: the number of columns after the post content column
    :return: index of rows modified (including also those have been modified previously)
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
            temp_str = df.iloc[target_row_number, 3]
            for j in range(4, df.shape[1] - restColumns):
                temp_str += ' ' + str(df.iloc[target_row_number, j])
            df.iloc[target_row_number, 3] = temp_str
            # put other columns in to the correct places
            for j in range(4, totalColumns):
                df.iloc[target_row_number, j] = df.iloc[target_row_number, df.shape[1] - totalColumns + j]
    df.drop(df.columns[-1], axis = 1, inplace = True)
    return target_row_numbers

def clean_answers(df):
    """
    Clean the dataframe of answers. Remove HTML tags in posts. Add a column indicating the post length.
    :param df: a dataframe directly got from the discussion_answers.csv file
    :return: the discussion answers in a neat format
    """
    NUMBER_OF_COLUMNS = 8
    NUMBER_OF_REST_COLUMNS = 4
    # Use a loop to modify the whole data frame
    prev = np.array([])
    while (df.shape[1] > NUMBER_OF_COLUMNS):
        prev = np.unique(np.concatenate([prev, modifyRow(df, prev, NUMBER_OF_COLUMNS, NUMBER_OF_REST_COLUMNS)]))
    # remove HTML tags
    df["discussion_answer_content"] = df["discussion_answer_content"].str.replace(r'<[\w\s\\/=\-?:."]*>', ' ')
    df["discussion_answer_content"] = df["discussion_answer_content"].str.replace(r'\\\\n', '')
    # change strings with only spaces to empty
    df["discussion_answer_content"] = df["discussion_answer_content"].apply(
        lambda string: '' if string.isspace() else string)
    # add post length of each answer
    df["answer_content_length"] = df["discussion_answer_content"].apply(lambda s: len(s.split()))
    return df

if __name__ == '__main__':
    # setting
    ARVR = 'ARVR'
    Civil = 'Civil'
    Fake = 'Fake'
    Privacy = 'Privacy'
    COURSE = Privacy
    PROCESSED_DIR = "processed data"
    TARGET_FILE = "discussion_answers.csv"
    CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
    # import data
    answers = pd.read_csv(CUR_DIR + "/" + COURSE + "/" + TARGET_FILE, encoding="ISO-8859-1")
    # clean it
    answers = clean_answers(answers)
    # output the cleaned data
    answers.to_csv(CUR_DIR + "/" + PROCESSED_DIR + "/" + COURSE + "/processed_" + TARGET_FILE, index = False, encoding ="ISO-8859-1")

