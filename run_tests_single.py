# -*- coding: utf-8 -*-

import sys
import unittest

from test.search.tests import *

if __name__ == '__main__':
    suite = unittest.TestSuite(
        map(PositiveTests, ['test_check_number_of_answers'])
    )
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())