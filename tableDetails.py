
# ---------------------------------------------TABLES------------------------------------------------


class Tables():

    tables = {}

    tables['users'] = "(username, email, class_id)"

    tables['dailyexam'] = "(name, teacher_id, class_id, question_ids)"

    tables['question'] = "(exam_id, question, choice_ids, correct_choice_id)"

    tables['choice'] = "(question_id, choice, value)"

    tables['teacher'] = "(name, phone, email, subject_ids, class_ids, mentor, password)"
