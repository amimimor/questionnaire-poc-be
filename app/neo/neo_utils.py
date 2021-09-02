import uuid


def generate_node_id():
    return str(uuid.uuid4())[:8]


def extract_answer(answers_node):
    return {
        "id": answers_node.get('Id'),
        "type": answers_node.get('Type'),
        "displayName": answers_node.get('DisplayName'),
        "defaultValue": answers_node.get('DisplayName'),
        "inputValue": answers_node.get('DisplayName'),
        "example": answers_node.get('example')
    }


def extract_answers(answers_nodes):
    answers = []
    for answer_node in answers_nodes:
        answers.append(extract_answer(answer_node))
    return answers


def extract_answer_ids(answer_list):
    answers_ids = []
    for answer in answer_list:
        answers_ids.append(answer['answerId'])
    return answers_ids


def extract_in_the_first_list(f_lst, s_lst):
    return list(set(f_lst) - set(s_lst))

def check_rule_in_answers(rule_list, answer_list):
    return set(rule_list).issubset(set(answer_list))
