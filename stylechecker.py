import inspect

from .autograder_utils import StatusMessage


class StyleChecker:
    """
    A very rudimentary and initial attempt at checking
    a program's style.

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
        self.function_list = [
            o[0] for o in inspect.getmembers(self.module)
            if inspect.isfunction(o[1])
        ]

    def _check_line_lengths(self):
        print("Checking line lengths...".ljust(64), end="")
        ok = True
        long_idxs = []
        for i, line in enumerate(self.module_lines):
            if len(line) > 79:
                long_idxs.append(i)

                ok = False
        if ok:
            print(StatusMessage("All good!", "SUCCESS"))
        else:
            print("\n")
            for idx in long_idxs[:3]:
                print(f"Line {idx} is longer than 80 characters")
                print("")
            if len(long_idxs) > 3:
                print(
                    f"{len(long_idxs) - 3} more lines are longer than 80 characters"
                )
            print("")

    def _check_function_defs(self):
        ok = True
        seen_already = set()

        print("Checking function definitions...".ljust(64), end="")
        for f in self.function_list:
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

    def assert_num_functions(self, min_required):
        """
        Check that *at least* `num` functions
        are present in the module.
        """
        print("Checking number of functions...".ljust(64), end="")
        if len(self.function_list) < min_required:
            print(StatusMessage(
                f"Expected at least {min_required}, only found {len(self.function_list)}", "FAIL"))
        else:
            print(StatusMessage("Okay!", "SUCCESS"))

    def assert_num_doctests(self, func_name, min_required):
        print("Checking number of doctests...".ljust(64), end="")
        docstring = getattr(self.module, func_name).__doc__
        num_doctests = docstring.count(">>>")
        if num_doctests >= min_required:
            print(StatusMessage("Okay!", "SUCCESS"))
        else:
            print(StatusMessage(
                f"Expected at least {min_required}, only found {len(num_doctests)}", "FAIL"))
