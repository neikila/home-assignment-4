# -*- coding: utf-8 -*-

import sys
import unittest

from test.search.tests import PositiveTests, NegativeTests

if __name__ == '__main__':
    suite = unittest.TestSuite(
        map(PositiveTests, ['test_accurate_search_by_text'])
    )
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())