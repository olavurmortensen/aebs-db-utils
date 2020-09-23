#!/usr/bin/env python3

import unittest, logging
from aebsDButils.ged2csv import Ged2Genealogy
from aebsDButils.read_csv import read_csv

logging.basicConfig(level=logging.INFO)


TEST_DATA_DIR = 'aebsDButils/test/test_data/'

TEST_GED = TEST_DATA_DIR + 'small_test_tree.ged'
TEST_CSV = TEST_DATA_DIR +'small_test_tree.csv'
TEST_CSV_CORRECT = TEST_DATA_DIR +'gen_correct.csv'
TEST_IND = TEST_DATA_DIR +'test_individuals.txt'


class Tests(unittest.TestCase):

    def setUp(self):
        logging.info('Set up tests')
        logging.info('------------')

    def test_write_gen_csv(self):
        logging.info('Write AEBS genealogy to CSV')
        logging.info('------------')

        # Read the GED file and write genealogy to CSV.
        Ged2Genealogy(TEST_GED, TEST_CSV)

        # Read the CSV that was just created.
        data = read_csv(TEST_CSV)

        # Read the "correct" data.
        correct_data = read_csv(TEST_CSV_CORRECT)

        self.assertTrue(len(data) == len(correct_data), 'Expected %d rows in genealogy but got %d.' %(len(correct_data), len(data)))

        # Sort both lists by the individual ID (first element of tuple), so
        # that they can be compared directly.
        data = sorted(data, key=lambda x: x[0])
        correct_data = sorted(correct_data, key=lambda x: x[0])

        # Individual IDs.
        ind = [d[0] for d in data]

        # Make sure the IDs are unique.
        self.assertTrue(len(ind) == len(set(ind)), 'Individual IDs are not unique.')

        # Correct individual IDs.
        ind_correct = [d[0] for d in correct_data]

        # Make sure the indivual IDs match the expected.
        diff = set(ind).symmetric_difference(ind_correct)
        self.assertTrue(len(diff) == 0, 'The indivual IDs do not match the expected.')

        # Make sure all the data in the records match the expected.
        for i in range(len(data)):
            rec = data[i]
            rec_correct = correct_data[i]

            self.assertEqual(data[i], correct_data[i], 'Data in record for individual ID %s does not match the expected.' % data[i][0])

    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

if __name__ == '__main__':
    unittest.main()
