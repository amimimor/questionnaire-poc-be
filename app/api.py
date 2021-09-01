def create_questionnaire(*args, **kwargs):
    print(kwargs)

    return {
               "questionnaireId": "FERRARI1"
           }, 200


def get_questionnaire(*args, **kwargs):
    print(kwargs)
    return {
               "questions": [
                   {
                       "expectMaxLen": 1,
                       "expectMinLen": 1,
                       "id": "488ENZO1",
                       "name": "Revenue",
                       "optionalAnswerList": [
                           {
                               "defaultValue": "Construction",
                               "displayName": "Construction",
                               "example": None,
                               "id": "296GTB4",
                               "inputValue": "Construction",
                               "type": "FreeText"
                           }
                       ],
                       "question": "enter company revenue",
                       "subQuestion": "please enter it only on dollars"
                   }
               ],
               "questionsStatus": {
                   "ENZO1F50": "GTS488SE"
               }
           }, 200


def submit_questionnaire(*args, **kwargs):
    print(kwargs)
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
    print(kwargs)
    return [
               {
                   "expectMaxLen": 1,
                   "expectMinLen": 1,
                   "id": "488ENZO1",
                   "name": "Revenue",
                   "optionalAnswerList": [
                       {
                           "defaultValue": "Construction",
                           "displayName": "Construction",
                           "example": None,
                           "id": "296GTB4",
                           "inputValue": "Construction",
                           "type": "FreeText"
                       }
                   ],
                   "question": "enter company revenue",
                   "subQuestion": "please enter it only on dollars"
               }
           ], 200
