# -*- coding: utf-8 -*-

import unittest
import sys
import unittest
from test.tests import PositiveTests


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(PositiveTests),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())