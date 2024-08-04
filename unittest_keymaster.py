# -*- coding: utf-8 -*-

import unittest
import HtmlTestRunner
from TestUnit.mock_press import TestKeyLogger

def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestKeyLogger))

    runner = HtmlTestRunner.HTMLTestRunner(
        output='test_reports',
        report_name="KeyLogger_DetailedTestReport",
        combine_reports=True,
        report_title="KeyLogger Detailed Test Report",
        template='./test_reports/template.html'
    )
    runner.run(test_suite)

if __name__ == '__main__':
    run_tests()