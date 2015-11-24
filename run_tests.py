# -*- coding: utf-8 -*-

import sys
import unittest

from test.search.tests import *

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(PositiveTests),
        unittest.makeSuite(NegativeTests),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())