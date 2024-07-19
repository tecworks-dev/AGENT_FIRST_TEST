
import unittest
import sys
import os
import traceback
import importlib
import asyncio
from termcolor import colored

class DiagnosticReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Add the parent directory to sys.path
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    def run_test(self, test_func):
        try:
            test_func()
        except Exception as e:
            print(colored(f"Test failed: {test_func.__name__}", "red"))
            print(colored(f"Error: {str(e)}", "red"))
            print(colored("Traceback:", "red"))
            traceback.print_exc()
            return False
        return True

    def test_main_py(self):
        print("\nTesting main.py")
        try:
            import main
            self.assertTrue(hasattr(main, 'main'))
            self.assertTrue(callable(main.main))
        except ImportError:
            print(colored("Error: main.py not found or cannot be imported", "red"))
            return False
        return True

    def test_planner_py(self):
        print("\nTesting planner.py")
        try:
            import planner
            self.assertTrue(hasattr(planner, 'plan_project'))
            self.assertTrue(callable(planner.plan_project))
        except ImportError:
            print(colored("Error: planner.py not found or cannot be imported", "red"))
            return False
        return True

    def test_code_generator_py(self):
        print("\nTesting code_generator.py")
        try:
            import code_generator
            self.assertTrue(hasattr(code_generator, 'agent_write_file'))
            self.assertTrue(callable(code_generator.agent_write_file))
        except ImportError:
            print(colored("Error: code_generator.py not found or cannot be imported", "red"))
            return False
        return True

    def test_error_fixer_py(self):
        print("\nTesting error_fixer.py")
        try:
            import error_fixer
            self.assertTrue(hasattr(error_fixer, 'fix_application_files'))
            self.assertTrue(callable(error_fixer.fix_application_files))
        except ImportError:
            print(colored("Error: error_fixer.py not found or cannot be imported", "red"))
            return False
        return True

    def test_feedback_handler_py(self):
        print("\nTesting feedback_handler.py")
        try:
            import feedback_handler
            self.assertTrue(hasattr(feedback_handler, 'update_application_files'))
            self.assertTrue(callable(feedback_handler.update_application_files))
        except ImportError:
            print(colored("Error: feedback_handler.py not found or cannot be imported", "red"))
            return False
        return True

    def test_unittest_creator_py(self):
        print("\nTesting unittest_creator.py")
        try:
            import unittest_creator
            self.assertTrue(hasattr(unittest_creator, 'create_unittests'))
            self.assertTrue(callable(unittest_creator.create_unittests))
            self.assertTrue(hasattr(unittest_creator, 'run_unittests'))
            self.assertTrue(callable(unittest_creator.run_unittests))
        except ImportError:
            print(colored("Error: unittest_creator.py not found or cannot be imported", "red"))
            return False
        return True

    def test_file_utils_py(self):
        print("\nTesting file_utils.py")
        try:
            import file_utils
            self.assertTrue(hasattr(file_utils, 'get_file_contents'))
            self.assertTrue(callable(file_utils.get_file_contents))
            self.assertTrue(hasattr(file_utils, 'save_file_contents'))
            self.assertTrue(callable(file_utils.save_file_contents))
            self.assertTrue(hasattr(file_utils, 'update_backup_folder'))
            self.assertTrue(callable(file_utils.update_backup_folder))
        except ImportError:
            print(colored("Error: file_utils.py not found or cannot be imported", "red"))
            return False
        return True

    def test_api_utils_py(self):
        print("\nTesting api_utils.py")
        try:
            import api_utils
            self.assertTrue(hasattr(api_utils, 'rate_limited_request'))
            self.assertTrue(callable(api_utils.rate_limited_request))
        except ImportError:
            print(colored("Error: api_utils.py not found or cannot be imported", "red"))
            return False
        return True

    def test_constants_py(self):
        print("\nTesting constants.py")
        try:
            import constants
            self.assertTrue(hasattr(constants, 'DEBUG'))
        except ImportError:
            print(colored("Error: constants.py not found or cannot be imported", "red"))
            return False
        return True

def main():
    print(colored("Starting Diagnostic Report", "cyan"))
    suite = unittest.TestLoader().loadTestsFromTestCase(DiagnosticReport)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    if result.wasSuccessful():
        print(colored("\nAll tests passed successfully!", "green"))
    else:
        print(colored("\nSome tests failed. Please check the output above for details.", "yellow"))

    print(colored("\nDiagnostic Report Complete", "cyan"))

if __name__ == "__main__":
    main()
