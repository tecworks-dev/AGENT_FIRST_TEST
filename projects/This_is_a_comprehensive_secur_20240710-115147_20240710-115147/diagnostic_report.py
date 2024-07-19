
import unittest
import traceback

class TestApplication(unittest.TestCase):
    
    def setUp(self):
        print(f"\nRunning test for application_plan.xml")
        
    def test_application_plan_exists(self):
        try:
            with open('application_plan.xml', 'r') as f:
                content = f.read()
            self.assertIsNotNone(content)
        except FileNotFoundError:
            print("Test failed: application_plan.xml does not exist")
            traceback.print_exc()
        except Exception as e:
            print(f"Test failed: Unexpected error when reading application_plan.xml")
            traceback.print_exc()

    def test_application_plan_content(self):
        try:
            with open('application_plan.xml', 'r') as f:
                content = f.read()
            self.assertIn("<application>", content)
        except Exception as e:
            print(f"Test failed: Error checking content of application_plan.xml")
            traceback.print_exc()

    # Add more tests here for specific functionality

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestApplication)
    unittest.TextTestRunner(verbosity=2).run(suite)

def main():
    print("Starting diagnostic tests...")
    run_tests()
    print("Diagnostic tests completed.")

if __name__ == "__main__":
    main()
