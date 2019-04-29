"""
A collection of test runner objects intended to
facilitate checking student output against the
solution on a variety of inputs.

# TODO make an arglist class?
"""

import io
import contextlib
import traceback

from .autograder_utils import StatusMessage, TestFailHandlers


class FunctionTestRunner():
    """
    A 'base' function test runner.
    """

    def __init__(self, student_fn, soln_fn):
        self.student_fn = student_fn
        self.soln_fn = soln_fn
        self.arglist = []
        self.current_test = 0

    def add_args(self, args=[], kwargs={}):
        self.arglist.append((args, kwargs))

    def add_arglist(self, arglist):
        self.arglist.extend(arglist)

    def run_tests(self, fail_handler=TestFailHandlers.base_fail_handler):
        """
        `fail_handler` must be callable and will take the student output
        and the solution output in that order as positional arguments.
        """
        fn_name = self.student_fn.__name__
        print(StatusMessage(f"\n\nTesting {fn_name}...", "INFO"))
        print("-" * 70)
        for i, (args, kwargs) in enumerate(self.arglist):
            param_str = FunctionTestRunner._make_param_str(args, kwargs)
            print(f"Testing {fn_name}({param_str})...".ljust(64), end="")

            try:
                student_out, soln_out = self._get_outputs(i)
                if (student_out == soln_out):
                    print(StatusMessage("Test passed!", "SUCCESS"))
                else:
                    print(StatusMessage("Test failed!", "FAIL"))
                    if fail_handler:
                        fail_handler(student_out, soln_out)
            except Exception as error:
                # rip
                print(StatusMessage(f"Test Crashed: {error}", "FAIL"))
                print(traceback.format_exc())

    def _get_outputs(self, i):
        args, kwargs = self.arglist[i]
        return self.student_fn(*args, **kwargs), self.soln_fn(*args, **kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_test == len(self.arglist):
            raise StopIteration
        student_output, soln_output = self._get_outputs(self.current_test)
        ret = self.arglist[self.current_test], student_output, soln_output
        self.current_test += 1
        return ret

    @staticmethod
    def _make_param_str(args, kwargs):
        args_str_list = [repr(a) for a in args]
        kwargs_str_list = [f"{repr(k)}={repr(v)}" for k, v in kwargs.items()]
        params_str_list = args_str_list + kwargs_str_list
        return ", ".join(params_str_list)


class CapturedFunctionTestRunner(FunctionTestRunner):
    """
    Like a function test runner, but for functions
    that output to the console. We redirect stdout
    to a string, and compare said strings. God bless
    contextlib.
    """

    class CapturedFunction:
        """
        A wrapper around an arbitrary function
        that redirects stdout to a string and returns it.
        Also is callable to make the client syntax a little
        cleaner.
        """

        def __init__(self, fn, args=[], kwargs={}):
            self.fn = fn
            self.args = args
            self.kwargs = kwargs

        def get_output(self):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                self.fn(*self.args, **self.kwargs)
            return f.getvalue()

        def __call__(self):
            return self.get_output()

    def _get_outputs(self, i):
        student_output = CapturedFunctionTestRunner.CapturedFunction(
            self.student_fn, *self.arglist[i]).get_output()
        soln_output = CapturedFunctionTestRunner.CapturedFunction(
            self.soln_fn, *self.arglist[i]).get_output()
        return student_output, soln_output
