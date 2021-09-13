from app.neo.neo_utils import *


def create_new_respondent(tx, company_name, policy_request_id):
    query = "CREATE(r:Respondent:MatanDev $node) return r"
    node = {
        'id': generate_node_id(),
        'comapnyName': company_name,
        'policyRequestId': policy_request_id
    }
    result = tx.run(query, node=node)
    record = result.single()
    return record[0].get("id")


def get_questions_from_neo(tx, form_id):
    q = "MATCH (f:Form:MatanDev {Id:$form_id})-[:hasQuestion]-(q:Question:MatanDev)-[:hasAnswer]-(a:Answer:MatanDev) return q, collect(a) as optionalAnswers"
    result = tx.run(q, form_id=form_id)
    questions = []
    for record in result:
        question = {
            'id': record[0].get('Id'),
            'name': record[0].get('Name'),
            'question': record[0].get('BaseQuestion'),
            'subQuestion': None,
            'expectMinLen': record[0].get('ExpectMinLen'),
            'expectMaxLen': record[0].get('ExpectMaxLen'),
            'optionalAnswerList': extract_answers(record[1])
        }
        questions.append(question)

    return questions


def get_forms_id_from_neo(tx):
    q = "Match(f:Form:MatanDev {Name:'Opeining Form'}) return f "
    result = tx.run(q)
    record = result.single()
    return record[0].get("Id")


def add_answer_of_respondent(tx, respondent_id, question_id, answer_ids):
    if answer_ids:
        query_to_insert = ('Match(r:Respondent:MatanDev ),(q:Question:MatanDev ),(a:Answer:MatanDev ) '
                           'where r.id=$respondent_id and q.Id=$question_id and a.Id IN $answer_ids '
                           'MERGE (r)-[rw:respondedWith]->(a) '
                           'MERGE (r)-[rt:respondedTo]->(q) '
                           'RETURN r,q,a')
        tx.run(query_to_insert, respondent_id=respondent_id, question_id=question_id,
               answer_ids=answer_ids)


def delete_answer_of_respondent(tx, respondent_id, answer_ids):
    if answer_ids:
        query_to_delete = ('MATCH (r:Respondent:MatanDev)-[rw:respondedWith]->(a:Answer:MatanDev) '
                           'WHERE r.id=$respondent_id and a.Id IN $answer_ids '
                           'Delete rw')
        tx.run(query_to_delete, respondent_id=respondent_id, answer_ids=answer_ids)


def update_respondent_answer(tx, respondent_id, question):
    # check if I answer the question
    # if No -> add new answer to question
    # if Yes ->
    # get all answers for this question from respondent
    # 1. if they not exacly like new - remove the unnececry
    # 2. don't do anything

    question_id = question['questionId']
    answer_ids = extract_answer_ids(question['answersList'])
    query_to_check_question = ('MATCH (r:Respondent:MatanDev)-[:respondedTo]->(q:Question:MatanDev) '
                               'WHERE r.id=$respondent_id and q.Id=$question_id '
                               'RETURN count(q.Id) as isQuestionConnect')
    response = tx.run(query_to_check_question, respondent_id=respondent_id, question_id=question_id)
    is_question_connect = 0
    for record in response:
        is_question_connect = record.get('isQuestionConnect')

    if is_question_connect:
        query_to_check_latest_respondent_answers = (
            'MATCH (r:Respondent)-[:respondedWith]->(a:Answer), (q:Question)-[:hasAnswer]->(a:Answer) '
            'WHERE r.id=$respondent_id and q.Id=$question_id '
            'return a.Id as answerId')
        response = tx.run(query_to_check_latest_respondent_answers, respondent_id=respondent_id,
                          question_id=question_id)
        list_of_latest_answers = []
        for record in response:
            list_of_latest_answers.append(record.get('answerId'))

        answer_to_remove = extract_in_the_first_list(list_of_latest_answers, answer_ids)
        answer_to_add = extract_in_the_first_list(answer_ids, list_of_latest_answers)
    else:
        answer_to_remove = []
        answer_to_add = answer_ids
    add_answer_of_respondent(tx, respondent_id, question_id, answer_to_add)
    delete_answer_of_respondent(tx, respondent_id, answer_to_remove)


def get_all_rules(tx):
    query = ('Match (r:Rule)-[aw:answerWith]-(a:Answer) return r.Id as ruleId, collect(a.Id) as answersId')
    response = tx.run(query)
    rules = {}
    for record in response:
        rules[record.get('ruleId')] = record.get('answersId')
    return rules


def get_all_respondent_answers(tx, respondent_id):
    query = ('Match (r:Respondent)-[rw:respondedWith]-(a:Answer) WHERE r.id=$respondent_id '
             'return collect(a.Id) as respondent_answers')
    response = tx.run(query, respondent_id=respondent_id)
    for record in response:
        return record.get('respondent_answers')


def get_question_to_show(tx, rules_ids):
    query = ('Match (r:Rule)-[:ruleTo]-(f:Form)-[:hasQuestion]-(q:Question) '
             'where r.Id in $rules_ids '
             'return collect(q.Id) as allQuestionToShow')
    response = tx.run(query, rules_ids=rules_ids)
    for record in response:
        return record.get('allQuestionToShow')


def get_base_rule(tx):
    query = ('Match  (r:Rule {Name:\'Base\'}) return r.Id as ruleId')
    response = tx.run(query)
    for record in response:
        return record.get('ruleId')


def get_questions_by_ids(tx, questions_ids):
    query = ('MATCH (q:Question:MatanDev)-[:hasAnswer]-(a:Answer:MatanDev) where q.Id in $questions_ids '
             'return q, collect(a) as optionalAnswers')
    response = tx.run(query, questions_ids=questions_ids)
    questions = []
    for record in response:
        question = {
            'id': record[0].get('Id'),
            'name': record[0].get('Name'),
            'question': record[0].get('BaseQuestion'),
            'subQuestion': None,
            'expectMinLen': record[0].get('ExpectMinLen'),
            'expectMaxLen': record[0].get('ExpectMaxLen'),
            'optionalAnswerList': extract_answers(record[1])
        }
        questions.append(question)

    return questions