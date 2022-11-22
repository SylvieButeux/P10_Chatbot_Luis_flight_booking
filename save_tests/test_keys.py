import unittest   # The test framework



class Test_key_azure_appinsight(unittest.TestCase):
    def test_OK(self):
        self.assertEqual(DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY, "f3001851-bd7c-4c79-b3f7-fa0cc1c30e55")

    def test_NOK(self):
        self.assertNotEqual(DefaultConfig.APPINSIGHTS_INSTRUMENTATION_KEY, "hhhhh")

class Test_key_app_luis(unittest.TestCase):
    def test_OK(self):
        self.assertEqual(DefaultConfig.LUIS_API_KEY, "ad25e2608a7b496ca39d639f74a0dcd8")

    def test_NOK(self):
        self.assertNotEqual(DefaultConfig.LUIS_API_KEY, "hhhhh")

if __name__ == '__main__':
    unittest.main(module="tests")
    
    
    