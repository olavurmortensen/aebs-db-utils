#!/usr/bin/env python3

import unittest, logging

logging.basicConfig(level=logging.INFO)


TEST_DATA_DIR = 'aebsDButils/test/test_data/'

TEST_GED = TEST_DATA_DIR + 'small_test_tree.ged'
TEST_CSV = TEST_DATA_DIR +'correct_results.csv'
TEST_IND = TEST_DATA_DIR +'test_individuals.txt'

class Tests(unittest.TestCase):

    def setUp(self):
        logging.info('Set up tests')
        logging.info('------------')

    def test1(self):
        logging.info('Test 1')
        logging.info('------------')

    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

if __name__ == '__main__':
    unittest.main()
