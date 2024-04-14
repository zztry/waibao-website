import json
from typing import Iterator
import check_error

##new
from flask import Flask, request


def read_dict(data: dict) -> Iterator[dict]:
    
    for single_usr in data['data']:
        usr_interact = single_usr["interactionAttr"]
        usr_page = single_usr["pageAttr"]
        usr_performance = single_usr["performanceAttr"]
        usr_analysis = {}
        # get_attr = {"in": set(), "pa": set(), "pe": set()}
        for key in usr_interact.keys():
            # get_attr["in"] |= {(key, type(usr_interact[key]["value"]))}
            usr_analysis[key] = usr_interact[key]["value"]
        for key in usr_page.keys():
            # get_attr["pa"] |= {(key, type(usr_page[key]["value"]))}
            usr_analysis[key] = usr_page[key]["value"]
        for key in usr_performance.keys():
            # get_attr["pe"] |= {(key, type(usr_performance[key]["value"]))}
            usr_analysis[key] = usr_performance[key]["value"]
        
        usr_analysis["event"] = single_usr["eventName"]
        usr_analysis["ID"] = single_usr["userId"]
        #1
        usr_analysis["url"] = single_usr["pageAttr"]["url"]["value"]
        # yield get_attr
        yield usr_analysis



def check_issuetype(usr_value: dict) -> tuple[int, str,str, list[str],float]:
    event: str = usr_value["event"].lower()
    id: int = usr_value["ID"]
    url: str = usr_value["url"]
    # error_count: int = usr_value["errorCount"]
    errors, eval_score = check_error.check_all_error(usr_value)
    print("Usr {} experience {}%".format(id, eval_score))
    return (id, event, url, errors,eval_score)
    # pass

#issue 3
def issue_process(issue: tuple[int, str, str,list[str]]) -> None:
    # print("User {} encountered {} errors in total")
    for iss in issue[3]:
        article = "a"
        if iss[0] in {'a', 'e', 'i', 'o', 'u'}:
            # 冠词
            article += "n"

        print("User {} potentially encountered {} {} while performing {} event.".format(issue[0], article, iss.replace('_', ' '), issue[1]))
    # pass

#4
def analyze_file(data: dict) -> list[tuple[int, str, str, list[str]]]:
    test_file = read_dict(data)
    issues = []
    # attr = {"in": set(), "pa": set(), "pe": set()}
    for usr_value in test_file:         
        # for key in usr_value.keys():
            # attr[key] |= usr_value[key]
        issue = check_issuetype(usr_value)
        #issue_process(issue)
        issues.append(issue)
    return issues





