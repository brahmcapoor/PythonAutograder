import sys
from autograder_utils import StatusMessage


def check_syntax_import(module_name):
    """
    Imports and returns the specified module, if its
    syntax is valid. Otherwise, prints an error and exits
    the program.
    """
    print(StatusMessage(
        f"\n\nChecking syntax in {module_name}... ", "INFO"), end="")
    try:
        module = __import__(module_name)
        print(StatusMessage("Syntax is ok!", "SUCCESS"))
        return module
    except SyntaxError as error:
        print(
            StatusMessage(f"\nSyntax Error in {error.filename}, line {error.lineno}:", "FAIL"))
        print("")
        print(error.text)
        print(f"{' '*error.offset}^")
        sys.exit(1)
