from app.neo.neo_transaction import *
from neo4j import GraphDatabase

uri = r"neo4j+s://bd62b7e5.databases.neo4j.io:7687"

with open('passwords.txt') as f:
    password = f.readlines()
PASSWORD = password[0]


def get_questions_for_questionnaire():
    driver = GraphDatabase.driver(uri, auth=('neo4j', PASSWORD))
    with driver.session() as session:
        f_id = session.read_transaction(get_forms_id_from_neo)
        questions = session.read_transaction(get_questions_from_neo, f_id)
    driver.close()
    return questions


def get_questions_for_update_questionnaire(questions_ids):
    driver = GraphDatabase.driver(uri, auth=('neo4j',PASSWORD))
    with driver.session() as session:
        questions = session.read_transaction(get_questions_by_ids, questions_ids)
    driver.close()
    return questions


def write_new_respondent(company_name, policy_request_id):
    driver = GraphDatabase.driver(uri, auth=('neo4j', PASSWORD))
    with driver.session() as session:
        respondent_id = session.write_transaction(create_new_respondent, company_name, policy_request_id)
    driver.close()
    return respondent_id


def write_new_answer_for_respondent(question_to_submit):
    driver = GraphDatabase.driver(uri, auth=('neo4j', PASSWORD))
    with driver.session() as session:
        session.write_transaction(update_respondent_answer, question_to_submit['questionnaireId'],
                                  question_to_submit['question_to_submit'])
    driver.close()


def check_rules_for_new_questions(respondent_id):
    driver = GraphDatabase.driver(uri, auth=('neo4j', PASSWORD))
    with driver.session() as session:
        rules = session.read_transaction(get_all_rules)
        answers_list = session.read_transaction(get_all_respondent_answers, respondent_id)
        rule_base = session.read_transaction(get_base_rule)
        rules[rule_base] = []
        rule_to_display = []
        for rule in rules:
            if check_rule_in_answers(rules[rule], answers_list):
                rule_to_display.append(rule)
        all_question_to_show = session.read_transaction(get_question_to_show, rule_to_display)
    driver.close()
    return all_question_to_show