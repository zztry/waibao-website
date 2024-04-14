from typing import Callable
import operator

# operator.gt/lt/eq
def check_key(usr_value: dict, key: str, potential, relation: Callable) -> tuple[bool, int]: 
    # pass
    if key in usr_value.keys():
        return relation(usr_value[key], potential)
    
    return False

def blank_page_error(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "isBlank", "True", operator.eq), 36

def repeat_click_error(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "repeatClick", "True", operator.eq), 25
    
def page_loading_problem(usr_value: dict) -> tuple[bool, int]:
    # pass
    condition = check_key(usr_value, "isRefresh", "True", operator.eq)
    condition |= check_key(usr_value, "pageLoad", 5000, operator.gt)
    condition |= check_key(usr_value, "loadingPerformance", "Good", operator.ne)    
    return condition, 16

def unpleasant_first_interaction_problem(usr_value: dict) -> tuple[bool, int]:
    # pass
    condition = check_key(usr_value, "firstInteractionPerformance", "Good", operator.ne)
    condition |= check_key(usr_value, "firstInputDelay", 500, operator.gt)
    return condition, 16

def network_latency_problem(usr_value: dict) -> tuple[bool, int]:
    # pass
    condition = check_key(usr_value, "timeSincePageLoad", 50000, operator.gt)
    condition |= check_key(usr_value, "slowNetwork", "True", operator.eq)
    return condition, 9

def lack_of_engaging_content(usr_value: dict) -> tuple[bool, int]:
    #pass
    return check_key(usr_value, "stayTime", 5000, operator.lt), 9

def console_error(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "consoleErrors", 0, operator.gt), 36
  
def console_warning(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "consoleWarnings", 0, operator.gt), 16
  
def page_text_error(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "errorText", "", operator.gt), 25
  
def page_loading_error(usr_value: dict) -> tuple[bool, int]:
    # pass  
    return check_key(usr_value, "isError", "True", operator.eq), 36

def high_click_latency_problem(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "feedbackInterval", 500, operator.gt), 9 

def high_rendering_latency_problem(usr_value: dict) -> tuple[bool, int]:
    # pass
    return check_key(usr_value, "largestContentfulPaint", 2500, operator.gt), 9 
# def error_in_loading_pages(usr_value: dict) -> tuple[bool, int]:
    # pass

all_function: list[Callable] = [blank_page_error, 
                                repeat_click_error, 
                                page_loading_problem,
                                unpleasant_first_interaction_problem, 
                                network_latency_problem, 
                                lack_of_engaging_content, 
                                console_error,
                                console_warning,
                                page_text_error,
                                page_loading_error, 
                                high_click_latency_problem, 
                                high_rendering_latency_problem]

def check_all_error(usr_value: dict) -> tuple[list[str], float]:
    # __name__属性直接获得函数的名字
    score = 0
    issues = []
    global all_function
    for func in all_function:
        flag, errorvalue = func(usr_value)
        if flag:
            issues.append(func.__name__)
            score += errorvalue

    if score < 49:
        x = (49 - score) / 10 + 0.5
    elif score < 100:
        x = 0.5 - (score - 50) / 100
    else:
        x = 0.01

    evaluate = 1 - 1 / (1 + x ** 2)
    return issues, evaluate * 100
    # pass