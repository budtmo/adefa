import unittest

from time import sleep

from appium import webdriver


class MSiteChromeAndroidUITests(unittest.TestCase):

    def setUp(self):
        desired_caps = {}
        self.driver = webdriver.Remote(
            'http://127.0.0.1:4723/wd/hub', desired_caps)

    def test_open_url(self):
        self.driver.get('http://google.com')

        search = self.driver.find_element_by_name('q')
        search.send_keys('butomo1989 docker-android')
        search.submit()
        sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MSiteChromeAndroidUITests)
    unittest.TextTestRunner(verbosity=2).run(suite)
