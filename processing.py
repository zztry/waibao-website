from typing import Iterator
import check_error

def read_dict(data: dict) -> Iterator[dict]:
    for single_usr in data['data']:
        usr_interact = single_usr["interactionAttr"]
        usr_page = single_usr["pageAttr"]
        usr_performance = single_usr["performanceAttr"]
        usr_analysis = {}

        for key in usr_interact.keys():
            usr_analysis[key] = usr_interact[key]["value"]
        for key in usr_page.keys():
            usr_analysis[key] = usr_page[key]["value"]
        for key in usr_performance.keys():
            usr_analysis[key] = usr_performance[key]["value"]
        
        usr_analysis["event"] = single_usr["eventName"]
        usr_analysis["ID"] = single_usr["userId"]

        yield usr_analysis

def check_issuetype(usr_value: dict) -> tuple[int, str, list[str]]:
    event: str = usr_value["event"].lower()
    id: int = usr_value["ID"]
    # error_count: int = usr_value["errorCount"]
    return (id, event, check_error.check_all_error(usr_value))
    # pass

def issue_process(issue: tuple[int, str, list[str]]) -> None:
    # print("User {} encountered {} errors in total")
    for iss in issue[2]:
        article = "a"
        if iss[0] in {'a', 'e', 'i', 'o', 'u'}:
            # 冠词
            article += "n"

        print("User {} potentially encountered {} {} while performing {} event.".format(issue[0], article, iss.replace('_', ' '), issue[1]))
    # pass

def analyze_file(data: dict):
    test_file = read_dict(data)
    # attr = {"in": set(), "pa": set(), "pe": set()}
    for usr_value in test_file:
        # for key in usr_value.keys():
            # attr[key] |= usr_value[key]
        issue = check_issuetype(usr_value)
        issue_process(issue)