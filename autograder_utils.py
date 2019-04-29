"""
Miscellaneous autograding utilities. This will likely
be decomposed into more descriptive modules later
once I have a better sense of what that decomposition
will like
"""
import platform
import itertools


class StatusMessage():
    """
    Allows for colored output in the terminal
    """

    colors = {
        # ansi escape sequences, shamelessly stolen from stack overflow
        "HEADER": '\033[95m',
        "OKBLUE": '\033[94m',
        "SUCCESS": '\033[92m',
        "INFO": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m',
        "UNDERLINE": '\033[4m'
    }

    def __init__(self, message, message_type):
        self.message = message
        self.type = message_type

    def __str__(self):
        if platform.system() == 'Windows': # Windows is the worst
            return self.message
        return self.colors[self.type] + self.message + self.colors["ENDC"]


class TestFailHandlers():
    """
    Various static methods used as handlers for mismatched
    student and solution output. Each function takes in
    student and solution output as parameters, as well
    as any additional keyword arguments
    """
    @staticmethod
    def base_fail_handler(student_out, soln_out):
        """
        Default test fail handler
        """
        print(f"Student output:  {student_out}")
        print(f"Expected output: {soln_out}")

    @staticmethod
    def show_diff(student_out, soln_out, num_diffs_to_show=3):
        """
        Test fail handler for dealing with multiline
        text output
        """
        s1 = student_out.split("\n")
        s2 = soln_out.split("\n")

        print(StatusMessage(
            f"First {num_diffs_to_show} differences:", "OKBLUE")
        )
        for i, (student_line, soln_line) in enumerate(itertools.zip_longest(s1, s2)):
            # we use itertools.zip_longest in case some output is longer than the others
            if i > num_diffs_to_show:
                # don't overwhelm console
                print("And more...")
                break
            if student_line != soln_line:
                print(StatusMessage(f"Line {i}", "UNDERLINE"))
                print(f"Student output:  {student_line}")
                print(f"Expected output: {soln_line}")
        print("")


def print_header(text):
    print("")
    space_before = (80 - len(text)) // 2
    space_after = 80 - len(text) - space_before
    print(StatusMessage(
        f"{space_before * ' '}{text.upper()}{space_after * ' '}", "BOLD"))
