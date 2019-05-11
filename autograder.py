import doctest
import unittest

from .autograder_utils import StatusMessage, print_header
from .filehandlers import check_syntax_import
from .stylechecker import StyleChecker


class AutoGrader:
    """
    A base AutoGrader Class. Theoretically, this is capable of
    running doctests and style checks on any module, but I imagine
    that in most use cases, it will be subclassed and `_run_additional_tests`
    will be overridden.
    """

    def __init__(self,
                 module_name,
                 has_doctests=True,
                 has_additional_tests=False,
                 has_stylecheck=True,
                 has_additional_stylecheck=False):
        """
        the last 3 allow us to control which kinds of tests
        we run
        """
        print_header("Starting AutoGrader...")
        self.module_name = module_name
        self.module = check_syntax_import(self.module_name)
        self.has_doctests = has_doctests
        self.has_additional_tests = has_additional_tests
        self.has_stylecheck = has_stylecheck
        self.has_additional_stylecheck = has_additional_stylecheck

        self.checker = StyleChecker(self.module)

    def _run_doctests(self):
        print(StatusMessage(
            f"\n\nRunning doctests for {self.module_name}...", "INFO"))
        test_suite = doctest.DocTestSuite(self.module)
        unittest.TextTestRunner(verbosity=0).run(test_suite)

    def _run_additional_tests(self):
        raise NotImplementedError("run_additional_tests not implemented")

    def _run_stylecheck(self):
        print(StatusMessage(
            f"\n\nChecking (very basic) style for {self.module_name}...",
            "INFO"
        )
        )
        print("-"*70)
        self.checker.check_style()

    def _run_additional_stylecheck(self):
        raise NotImplementedError("run_additional_stylecheck not implemented")

    def run_tests(self):
        if self.has_doctests:
            self._run_doctests()
        if self.has_additional_tests:
            self._run_additional_tests()
        if self.has_stylecheck:
            self._run_stylecheck()
        if self.has_additional_stylecheck:
            self._run_additional_stylecheck()
