## cleanTeachOuts
A mini project for cleaning the Coursera discussion forums data. It mainly:

* restores the broken csv format caused by commas in the texts
* removes HTML tags
* adds post length information
* merges questions and answers
* adds post language information

Data are not included, but here're descriptions of some important attributes in data files.

#### discussion_questions.csv
* discussion_question_id:	The id of the question in the discussion forum.
* user_id:	Encrypted Coursera user id.
* discussion_question_title:	The title of the question.
* discussion_question_details:	The content of the question
* discussion_question_created_ts:	The timestamp of when the discussion question was created.

#### discussion_answers.csv
* discussion_answer_id: The id of the answer in the discussion forum.
* user_id:	Encrypted Coursera user id.
* discussion_answer_content: Content of the answer
* discussion_question_id:	The id of a question in the discussion forum.
* discussion_answer_parent_discussion_answer_id:	Parent answer if this is a nested reply (we cap nesting at 1 level)
* discussion_answer_created_ts:	The timestamp of when the discussion answer was created.

#### course_memberships.csv
* user_id:	Encrypted Coursera user id.
* course_membership_role:	A user can have one of multiple roles in a course, set either by their affiliation to the course, or their activity. Currently the options include: not_enrolled, pre_enrolled_learner, browser, learner, mentor, teaching_staff, instructor, university_admin.
* course_membership_ts:	The timestamp for when a user became affiliated with the course in that particular membership role.



The script cleaningMain.py is used when processing data of serveral courses. One of the other python scripts can also be used individually if only intermediate results are needed. Check each file to see its effects.
