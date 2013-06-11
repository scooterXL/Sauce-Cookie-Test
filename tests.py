from selenium.webdriver import Remote
import unittest
import os

# HTTP/1.0 200 OK
# Content-Type: text/html; charset=utf-8
# Content-Length: 153
# Set-Cookie: ccc0=stuff; Path=/
# Set-Cookie: ccc1=stuff; Path=/
# Set-Cookie: ccc2=stuff; Path=/
# Server: Werkzeug/0.8.1 Python/2.7.2
# Date: Fri, 18 Nov 2011 14:55:12 GMT
#
#
#         <html>
#             <head><title>Cookie Test</title></head>
#             <body>Dropped cookies under name <em>ccc</em></body>
#         </html>
#


class CookieTest(object):

    def test_cookies(self):
        for N in range(1, 4):
            browser = self.browser
            browser.get("http://127.0.0.1:5000/test/%s" % N)
            cookies = browser.get_cookies()
            for n in range(N):
                assert 'test%s' % n in [f['name'] for f in cookies], "Fail: test%s not in %s" % (n, cookies)


class Sauce(unittest.TestCase, CookieTest):

    def setUp(self):
        caps = {"platform": "Windows 2003",
                "browserName": "firefox",
                "version": "21",
                "name": "Multiple Cookie Bug Test."}
        self.browser = Remote('http://%(SAUCE_USER)s:%(SAUCE_KEY)s@127.0.0.1:4445/wd/hub' % os.environ,
                              desired_capabilities=caps)

    def tearDown(self):
        self.browser.quit()


class Localhost(unittest.TestCase, CookieTest):

    def setUp(self):
        caps = {"browserName": "chrome",
                "name": "Multiple Cookie Bug Test."}
        self.browser = Remote('http://127.0.0.1:4444/wd/hub',
                                    desired_capabilities=caps)

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
