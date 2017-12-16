import unittest

import webapp


class WebappTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to webapp', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
