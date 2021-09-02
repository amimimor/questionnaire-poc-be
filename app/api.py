from app.neo.neo_api import write_new_respondent, get_questions_for_questionnaire, write_new_answer_for_respondent, \
    check_rules_for_new_questions, get_questions_for_update_questionnaire


def create_questionnaire(*args, **kwargs):
    company_name = kwargs['body']['companyName']
    policy_request_id = kwargs['body']['policyRequestId']
    rid = write_new_respondent(company_name, policy_request_id)
    return {
               "questionnaireId": rid
           }, 200


def get_questionnaire(*args, **kwargs):
    return {
        'questions': get_questions_for_questionnaire(),
        'questionStatus': {}
    }


def submit_questionnaire(*args, **kwargs):

    return [
               {
                   "answersList": [
                       {
                           "answerId": "458F40GT",
                           "inputValue": "3,000,000",
                           "type": "FreeText"
                       }
                   ],
                   "questionId": "360MODNA"
               }
           ], 200


def post_question_from_Questionnaire(*args, **kwargs):
    write_new_answer_for_respondent(kwargs)
    questions = check_rules_for_new_questions(kwargs['questionnaireId'])
    return get_questions_for_update_questionnaire(questions)
