#!/usr/bin/env python3

import unittest, logging
from aebsDButils.ged2csv import Ged2Genealogy

logging.basicConfig(level=logging.INFO)


TEST_DATA_DIR = 'aebsDButils/test/test_data/'

TEST_GED = TEST_DATA_DIR + 'small_test_tree.ged'
TEST_CSV = TEST_DATA_DIR +'small_test_tree.csv'
TEST_CSV_CORRECT = TEST_DATA_DIR +'correct_results.csv'
TEST_IND = TEST_DATA_DIR +'test_individuals.txt'


class Tests(unittest.TestCase):

    def setUp(self):
        logging.info('Set up tests')
        logging.info('------------')

    def test_write_gen_csv(self):
        logging.info('Write AEBS genealogy to CSV')
        logging.info('------------')
        Ged2Genealogy(TEST_GED, TEST_CSV)

    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

if __name__ == '__main__':
    unittest.main()
