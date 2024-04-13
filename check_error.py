from typing import Callable
import operator

# operator.gt/lt/eq
def check_key(usr_value: dict, key: str, potential, relation: Callable) -> bool: 
    # pass
    if key in usr_value.keys():
        return relation(usr_value[key], potential)
    
    return False

def blank_page_error(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "isBlank", "True", operator.eq)

def repeat_click_error(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "repeatClick", "True", operator.eq)
    
def poor_page_loading_problem(usr_value: dict) -> bool:
    # pass
    condition = check_key(usr_value, "isRefresh", "True", operator.eq)
    condition |= check_key(usr_value, "pageLoad", 5000, operator.gt)
    condition |= check_key(usr_value, "loadingPerformance", "Good", operator.ne)    
    return condition

def poor_first_interaction_problem(usr_value: dict) -> bool:
    # pass
    condition = check_key(usr_value, "firstInteractionPerformance", "Good", operator.ne)
    condition |= check_key(usr_value, "firstInputDelay", 500, operator.gt)
    return condition

def poor_network_problem(usr_value: dict) -> bool:
    # pass
    condition = check_key(usr_value, "timeSincePageLoad", 50000, operator.gt)
    condition |= check_key(usr_value, "slowNetwork", "True", operator.eq)

def lack_of_engaging_content(usr_value: dict) -> bool:
    #pass
    return check_key(usr_value, "stayTime", 5000, operator.lt) 

def console_error(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "consoleErrors", 0, operator.gt)
  
def console_warning(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "consoleWarnings", 0, operator.gt)
  
def page_text_error(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "errorText", "", operator.gt)
  
def page_loading_error(usr_value: dict) -> bool:
    # pass  
    return check_key(usr_value, "isError", "True", operator.eq)

def high_click_latency_problem(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "feedbackInterval", 500, operator.gt) 

def high_rendering_latency_problem(usr_value: dict) -> bool:
    # pass
    return check_key(usr_value, "largestContentfulPaint", 2500, operator.gt) 
# def error_in_loading_pages(usr_value: dict) -> bool:
    # pass

all_function: list[Callable] = [blank_page_error, 
                                repeat_click_error, 
                                poor_page_loading_problem,
                                poor_first_interaction_problem, 
                                poor_network_problem, 
                                lack_of_engaging_content, 
                                console_error,
                                console_warning,
                                page_text_error,
                                page_loading_error, 
                                high_click_latency_problem, 
                                high_rendering_latency_problem]

def check_all_error(usr_value: dict) -> list[str]:
    # __name__属性直接获得函数的名字
    issues = []
    global all_function
    for func in all_function:
        if func(usr_value):
            issues.append(func.__name__)

    return issues
    # pass