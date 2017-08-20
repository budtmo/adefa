import unittest

from appium import webdriver


class SimpleAndroidUITests(unittest.TestCase):

    def setUp(self):
        url = 'http://127.0.0.1:4723/wd/hub'
        desired_caps = {}
        self.driver = webdriver.Remote(url, desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_calculation(self):
        text_fields = self.driver.find_elements_by_class_name('android.widget.EditText')
        text_fields[0].send_keys(4)
        text_fields[1].send_keys(6)

        btn_calculate = self.driver.find_element_by_class_name('android.widget.Button')
        btn_calculate.click()

        self.assertEqual('10', text_fields[2].text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleAndroidUITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
