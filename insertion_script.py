import uuid
from neo4j import GraphDatabase

uri = r"neo4j+s://bd62b7e5.databases.neo4j.io:7687"
with open('passwords.txt') as f:
    password = f.readlines()
PASSWORD = password[0]


def generate_node_id():
    return str(uuid.uuid4())[:8]


def create_question_answer_with_1_answer(tx, answer_node, question_node):
    query = ("CREATE (a:Answer:MatanDev $answer_node), (q:Question:MatanDev $question_node), "
             "(q) - [hs:hasAnswer]->(a) "
             "RETURN q, a")
    tx.run(query, answer_node=answer_node, question_node=question_node)


def create_question_answer_with_2_answer(tx, answer_node1, answer_node2, question_node):
    query = ("CREATE (a:Answer:MatanDev $answer_node1), (a2:Answer:MatanDev $answer_node2), "
             "(q:Question:MatanDev $question_node), (q) - [hs:hasAnswer]->(a) , (q)-[hs2:hasAnswer]->(a2)"
             "RETURN q, a")
    tx.run(query, answer_node1=answer_node1, answer_node2=answer_node2, question_node=question_node)


def create_forms(tx, f1, f2, f3):
    query = ("CREATE (f:Form:MatanDev $f1), (f2:Form:MatanDev $f2), (f3:Form:MatanDev $f3)"
             "return f,f2,f3")
    tx.run(query, f1=f1, f2=f2, f3=f3)


def connect_form_with_questions(tx, f_id, q_ids):
    query = ("MATCH (f:Form:MatanDev), (q:Question:MatanDev) "
             "WHERE f.Id = $f_id and q.Id IN $q_ids "
             "CREATE (f)-[hq:hasQuestion]->(q)"
             "RETURN f,q")
    tx.run(query, f_id=f_id, q_ids=q_ids)


def create_rules(tx, r0, r1, r2):
    query = ("Create (r0:Rule:MatanDev $r0),"
             "(r1:Rule:MatanDev $r1),"
             "(r2:Rule:MatanDev $r2) "
             "return r0, r1, r2")
    tx.run(query, r0=r0, r1=r1, r2=r2)


def create_rule_from(tx, f_id, r_ids):
    query = ("MATCH (f:Form:MatanDev), (r:Rule:MatanDev) "
             "WHERE f.Id = $f_id and r.Id IN $r_ids "
             "CREATE (f)-[rf:ruleFrom]->(r) "
             "RETURN f,r")
    tx.run(query, f_id=f_id, r_ids=r_ids)


def create_rule_to(tx, f_id, r_id):
    query = ("MATCH (f:Form:MatanDev), (r:Rule:MatanDev) "
             "WHERE f.Id = $f_id and r.Id = $r_id "
             "CREATE (f)-[rt:ruleTo]->(r) "
             "RETURN f,r")
    tx.run(query, f_id=f_id, r_id=r_id)


def connect_answer_to_rule(tx, r_id, a_ids):
    query = ("MATCH (a:Answer:MatanDev), (r:Rule:MatanDev) "
             "WHERE a.Id IN $a_ids and r.Id = $r_id "
             "CREATE (a)-[aw:answerWith]->(r) "
             "RETURN a,r")
    tx.run(query, r_id=r_id, a_ids=a_ids)


def delete_all(tx):
    query = "Match(n) detach delete n"
    tx.run(query)


def quest1():
    answer_node = {'Id': generate_node_id(),
                   'Type': 'FreeText',
                   'DisplayName': 'Applicant\'s Name',
                   'DefaultValue': None,
                   'InputValue': None,
                   'example': None
                   }
    question_node = {'Id': generate_node_id(),
                     'Name': 'Applicant\'s Name',
                     'BaseQuestion': 'Applicant\'s Name (First Named Insured)',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node, question_node


def quest2():
    answer_node = {'Id': generate_node_id(),
                   'Type': 'FreeText',
                   'DisplayName': 'Other Named Insured\'s or DBAs',
                   'DefaultValue': None,
                   'InputValue': None,
                   'example': None
                   }

    question_node = {'Id': generate_node_id(),
                     'Name': 'Other Named Insured\'s or DBAs',
                     'BaseQuestion': 'Other Named Insured\'s or DBAs',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 0
                     }
    return answer_node, question_node


def quest3():
    answer_node = {'Id': generate_node_id(),
                   'Type': 'FreeText',
                   'DisplayName': 'Applicant\'s Primary Address',
                   'DefaultValue': None,
                   'InputValue': None,
                   'example': None
                   }
    question_node = {'Id': generate_node_id(),
                     'Name': 'Primary Address',
                     'BaseQuestion': 'Applicant\'s Primary Address',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node, question_node


def quest4():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'CurrencySelection',
                    'DisplayName': 'More than 3 Million',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': '1,000,000'
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'CurrencySelection',
                    'DisplayName': 'Less than 3 Million',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': '1,000,000'
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'Revenue',
                     'BaseQuestion': 'Applicant\'s annual revenue for the most recently completed fiscal year (or annual projection for a startup)',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, question_node


def quest5():
    answer_node = {'Id': generate_node_id(),
                   'Type': 'FreeText',
                   'DisplayName': 'Applicant\'s website/domain',
                   'DefaultValue': None,
                   'InputValue': None,
                   'example': None
                   }
    question_node = {'Id': generate_node_id(),
                     'Name': 'Website',
                     'BaseQuestion': 'Applicant\'s website/domain',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 0
                     }
    return answer_node, question_node


def quest6():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Yes',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'No',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'applicant been in business',
                     'BaseQuestion': 'Has the applicant been in business for at least three years?',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, question_node


def quest7():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Yes',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'No',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'single client represent more than 50% of the total revenue',
                     'BaseQuestion': 'Does the applicant or its principals have three or more years of experience in the services for which they are seeking coverage?',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, question_node


def quest8():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Yes',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'No',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'single client represent more than 50% of the total revenue',
                     'BaseQuestion': 'Does any single client represent more than 50% of the total revenue?',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, question_node


def quest9():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Yes',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'No',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'applicant use written contracts',
                     'BaseQuestion': 'Does the applicant use written contracts or agreements with customers for the provision of services?',
                     'ExpectMaxLen': 1,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, question_node


def quest10():
    answer_node1 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Service1',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node2 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Service2',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node3 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Service3',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    answer_node4 = {'Id': generate_node_id(),
                    'Type': 'SelectionAnswer',
                    'DisplayName': 'Service4',
                    'DefaultValue': None,
                    'InputValue': None,
                    'example': None
                    }
    question_node = {'Id': generate_node_id(),
                     'Name': 'applicant use written contracts',
                     'BaseQuestion': 'Please select the services for which coverage is being sought:',
                     'ExpectMaxLen': 4,
                     'ExpectMinLen': 1
                     }
    return answer_node1, answer_node2, answer_node3, answer_node4, question_node


def generate_forms():
    f1 = {
        'Id': generate_node_id(),
        'Name': 'Opeining Form',
    }
    f2 = {
        'Id': generate_node_id(),
        'Name': 'More Than 3 Million Revenue Form',
    }
    f3 = {
        'Id': generate_node_id(),
        'Name': 'Ending Form',
    }
    return f1, f2, f3


def generate_rules():
    r0 = {
        'Id': generate_node_id(),
        'Name': 'Base'
    }
    r1 = {
        'Id': generate_node_id(),
        'Name': 'RuleForMoreThan3Million'
    }
    r2 = {
        'Id': generate_node_id(),
        'Name': 'Default'
    }
    return r0, r1, r2


def get_ids_list(obs):
    ids = []
    for ob in obs:
        ids.append(ob['Id'])
    return ids


def write_all():
    driver = GraphDatabase.driver(uri, auth=('neo4j', PASSWORD))
    with driver.session() as session:
        session.write_transaction(delete_all)
        a1, q1 = quest1()
        session.write_transaction(create_question_answer_with_1_answer, a1, q1)

        a2, q2 = quest2()
        session.write_transaction(create_question_answer_with_1_answer, a2, q2)

        a3, q3 = quest3()
        session.write_transaction(create_question_answer_with_1_answer, a3, q3)

        a4a, a4b, q4 = quest4()
        session.write_transaction(create_question_answer_with_2_answer, a4a, a4b, q4)

        a5, q5 = quest5()
        session.write_transaction(create_question_answer_with_1_answer, a5, q5)

        a6a, a6b, q6 = quest6()
        session.write_transaction(create_question_answer_with_2_answer, a6a, a6b, q6)

        a7a, a7b, q7 = quest7()
        session.write_transaction(create_question_answer_with_2_answer, a7a, a7b, q7)

        a8a, a8b, q8 = quest8()
        session.write_transaction(create_question_answer_with_2_answer, a8a, a8b, q8)

        a9a, a9b, q9 = quest9()
        session.write_transaction(create_question_answer_with_2_answer, a9a, a9b, q9)

        a10a, a10b, a10c, a10d, q10 = quest10()
        session.write_transaction(create_question_answer_with_2_answer, a10a, a10b, q10)

        f1, f2, f3 = generate_forms()
        session.write_transaction(create_forms, f1, f2, f3)

        session.write_transaction(connect_form_with_questions, f1['Id'], get_ids_list([q1, q2, q3, q4, q5]))
        session.write_transaction(connect_form_with_questions, f2['Id'], get_ids_list([q6, q7, q8, q9]))
        session.write_transaction(connect_form_with_questions, f3['Id'], get_ids_list([q10]))

        r0, r1, r2 = generate_rules()
        session.write_transaction(create_rules, r0, r1, r2)
        session.write_transaction(create_rule_from, f1['Id'], get_ids_list([r1, r2]))
        session.write_transaction(create_rule_to, f1['Id'], r0['Id'])
        session.write_transaction(create_rule_to, f2['Id'], r1['Id'])
        session.write_transaction(create_rule_to, f3['Id'], r2['Id'])
        session.write_transaction(connect_answer_to_rule, r1['Id'], get_ids_list([a1, a3, a4a]))
        session.write_transaction(connect_answer_to_rule, r2['Id'], get_ids_list([a1, a3]))

    driver.close()


write_all()
