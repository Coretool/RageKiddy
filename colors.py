"""
Author: Coretool
Licence: MIT
Description: This file contains functions to format text for chameleon
"""

class colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def scs(text):
    return colour.GREEN + text + colour.END

def msg(text):
    return colour.BLUE + text + colour.END

def wrn(text):
    return colour.YELLOW + text + colour.END

def err(text):
    return colour.RED + text + colour.END

def pan(text):
    return colour.RED + '[PANIC] ' + text + colour.END

def fat(text):
    return colour.BOLD + colour.RED + '[FATAL] ' + text + colour.END

def mrk(text):
    return colour.UNDERLINE + text + colour.END

def debug(s):
    if LOG_LEVEL == 5:
        print(s)


def info(s):
    if LOG_LEVEL >= 4:
        print(msg(s))


def warn(s):
    if LOG_LEVEL >= 3:
        print(wrn(s))


def error(s):
    if LOG_LEVEL >= 2:
        print(err(s))


def fatal(s):
    if LOG_LEVEL >= 1:
        print(fat(s))



