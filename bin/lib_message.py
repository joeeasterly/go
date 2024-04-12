#!/usr/local/gh/go/.venv/bin/python

def red(input_message):
    """
    Wraps the input message in red color for terminal output.

    Parameters:
    - input_message (str): The message to be colored red.

    Returns:
    - str: The input message wrapped in ANSI codes for red color.

    Sample usage:
    >>> print(red("Warning: ") + "this is an error")
    This will print "Warning: " in red followed by "this is an error" in the default terminal color.
    """
    RED = '\033[91m'
    RESET = '\033[0m'
    return f"{RED}{input_message}{RESET}"

def green(input_message):
    """
    Wraps the input message in green color for terminal output.

    Parameters:
    - input_message (str): The message to be colored green.

    Returns:
    - str: The input message wrapped in ANSI codes for green color.

    Sample usage:
    >>> print(green("Success: ") + "operation completed")
    This will print "Success: " in green followed by "operation completed" in the default terminal color.
    """
    GREEN = '\033[92m'
    RESET = '\033[0m'
    return f"{GREEN}{input_message}{RESET}"

def yellow(input_message):
    """
    Wraps the input message in yellow color for terminal output.

    Parameters:
    - input_message (str): The message to be colored yellow.

    Returns:
    - str: The input message wrapped in ANSI codes for yellow color.

    Sample usage:
    >>> print(yellow("Warning: ") + "low disk space")
    This will print "Warning: " in yellow followed by "low disk space" in the default terminal color.
    """
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    return f"{YELLOW}{input_message}{RESET}"