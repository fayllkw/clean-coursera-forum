"""
cleaningMain.py:
Clean the discussion forums data of a number of teach-outs; count # of learners of each teach-out.
Cleaning includes
restoring the broken format; removing HTML tags; adding post length information; merging questions and answers;
adding post language information.
Output one "learner_count.csv" for all course.
Output five csv file for each course, which includes
"processed_discussion_answers.csv"; "processed_discussion_questions.csv", "merged_question_and_answer_with_language.csv",
"merged_question_and_answer_with_language_without_instructor.csv","english_only_question_and_answer_without_instructor.csv".
"""

import os
import pandas as pd
import cleanAnswers
import cleanQuestions
import merging
import tagLang

if __name__ == '__main__':
    # settings
    CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
    PARENT_DIR = os.path.dirname(CUR_DIR)
    DATA_DIR = PARENT_DIR + '/data'
    RESULT_DIR = PARENT_DIR + '/processed data'
    SUMMARY_DIR = PARENT_DIR + '/summary/stats'

    # get course directory names
    courses = [f for f in os.listdir(DATA_DIR) if not f.startswith('.')
               # and os.path.isdir(os.path.join(RESULT_DIR, f))     #judge it the name is a directory
               ]
    print(courses)
    learner_count = {}

    # clean course by course
    for course in courses:
        print(course)
        # clean answers and output
        answers = pd.read_csv(DATA_DIR + '/' + course + '/discussion_answers.csv', encoding='ISO-8859-1')
        cleaned_answers = cleanAnswers.clean_answers(answers)
        cleaned_answers.to_csv(RESULT_DIR + "/" + course + "/processed_discussion_answers.csv", index=False,
                                 encoding="ISO-8859-1")
        # clean questions and output
        questions = pd.read_csv(DATA_DIR + '/' + course + '/discussion_questions.csv', encoding='ISO-8859-1')
        cleaned_questions = cleanQuestions.clean_questions(questions)
        cleaned_questions.to_csv(RESULT_DIR + "/" + course + "/processed_discussion_questions.csv", index=False,
                                 encoding="ISO-8859-1")

        # merge them
        merged = merging.merge_questions_and_answers(questions=cleaned_questions, answers=cleaned_answers)

        # count the number of learners
        membership = pd.read_csv(DATA_DIR + '/' + course + '/course_memberships.csv', encoding='ISO-8859-1')
        learner_membership = membership[membership["course_membership_role"].isin(["PRE_ENROLLED_LEARNER", "LEARNER"])]
        temp_learner_count = len(set(learner_membership["umich_user_id"]))
        print("# of total learners in {}: {}".format(course, temp_learner_count))
        learner_count[course] = temp_learner_count

        # add language info and output
        labeled = merged.copy()
        labeled['language'] = tagLang.get_language_label(labeled)
        print('# of total posts: ', len(labeled))
        labeled.to_csv(RESULT_DIR + "/" + course + "/merged_question_and_answer_with_language.csv",
                             index = False, encoding = "ISO-8859-1")
        # remove instructors posts and output
        labeled_no_instructor = merging.remove_instructors(membership=membership, merged=labeled)
        print('# of total posts by learners: ', len(labeled_no_instructor))
        labeled_no_instructor.to_csv(RESULT_DIR + "/" + course + "/merged_question_and_answer_with_language_without_instructor.csv",
                       index=False, encoding="ISO-8859-1")
        # remove empty and non-en posts and output
        english_only_wo_instructor = labeled_no_instructor[labeled_no_instructor["post_content_length"] != 0].copy()
        english_only_wo_instructor = english_only_wo_instructor[english_only_wo_instructor['language'] == 'en']
        print('# of english posts by learners: ', len(english_only_wo_instructor))
        english_only_wo_instructor.to_csv(RESULT_DIR + "/" + course + "/english_only_question_and_answer_without_instructor.csv",
            index=False, encoding="ISO-8859-1")

    # output the learner count to the summary directory
    learner_count = pd.DataFrame(list(learner_count.items()), columns=['course', '# of learners'])
    learner_count.to_csv(SUMMARY_DIR + '/learner_count.csv', index=False)

