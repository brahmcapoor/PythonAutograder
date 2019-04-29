import inspect

from autograder_utils import StatusMessage


class StyleChecker:
    """
    A very rudimentary and initial attempt at checking
    a program's style.

    #TODO limit verbosity of line checks
    #TODO check variable name lengths
    #TODO some measure of decomposition
    #TODO check recursion

    Those last two might require a janky parser,
    or finally learning how the ast module works D:
    """

    def __init__(self, module):
        self.module = module
        self.module_src = inspect.getsource(module)
        self.module_lines = self.module_src.split("\n")

    def _check_line_lengths(self):
        print("Checking line lengths...".ljust(64), end="")
        ok = True
        for i, line in enumerate(self.module_lines):
            if len(line) > 79:
                print("")
                print(f"Line {i} is greater than 80 characters")
                ok = False
        if ok:
            print(StatusMessage("All good!", "SUCCESS"))
        else:
            print("")

    def _check_function_defs(self):
        function_list = [
            o[0] for o in inspect.getmembers(self.module)
            if inspect.isfunction(o[1])
        ]
        ok = True
        seen_already = set()

        print("Checking function definitions...".ljust(64), end="")
        for f in function_list:
            if f in seen_already:
                print(f"Multiple functions called {f}")
                ok = False
            seen_already.add(f)
            if len(f) < 5 and f != "main":
                print("")
                print(
                    f"function {f} has a pretty short name, make sure it's ok"
                )
                ok = False

        if ok:
            print(StatusMessage("All good!", "SUCCESS"))

    def _check_variables(self):
        pass

    def check_style(self):
        self._check_line_lengths()
        self._check_function_defs()
