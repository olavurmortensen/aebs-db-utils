#!/usr/bin/env python3

import unittest, logging
from aebsDButils.ged2csv import Ged2Genealogy, GetBirthYear, GetEncryptedID
from aebsDButils.utils import encrypt, check_pid
from aebsDButils.read_csv import read_csv

logging.basicConfig(level=logging.INFO)


TEST_DATA_DIR = 'aebsDButils/test/test_data/'

# Test GED file to read from.
TEST_GED = TEST_DATA_DIR + 'test_ged.ged'

# Expected results.
EXPECTED_GEN = TEST_DATA_DIR + 'expected_gen.csv'
EXPECTED_BY = TEST_DATA_DIR + 'expected_by.csv'
EXPECTED_BP = TEST_DATA_DIR + 'expected_bp.csv'

# Actual results.
ACTUAL_GEN = TEST_DATA_DIR + 'actual_gen.csv'
ACTUAL_BY = TEST_DATA_DIR + 'actual_by.csv'
ACTUAL_BP = TEST_DATA_DIR + 'actual_bp.csv'
ACTUAL_HASHID = TEST_DATA_DIR + 'actual_hash_id.csv'

class TestGen(unittest.TestCase):

    def setUp(self):
        logging.info('Setup genealogy tests')
        logging.info('------------')

    def test_write_gen_csv(self):
        logging.info('Read genealogy from GED and write to CSV')
        logging.info('------------')

        # Read the GED file and write genealogy to CSV.
        Ged2Genealogy(TEST_GED, ACTUAL_GEN)

        # Read the CSV that was just created.
        actual_data = read_csv(ACTUAL_GEN)

        # Read the "correct" data.
        expected_data = read_csv(EXPECTED_GEN)

        self.assertTrue(len(actual_data) == len(expected_data), 'Expected %d rows in genealogy but got %d.' %(len(expected_data), len(actual_data)))

        # Sort both lists by the individual ID (first element of tuple), so
        # that they can be compared directly.
        actual_data = sorted(actual_data, key=lambda x: x[0])
        expected_data = sorted(expected_data, key=lambda x: x[0])

        # Individual IDs.
        ind_actual = [d[0] for d in actual_data]

        # Make sure the IDs are unique.
        self.assertTrue(len(ind_actual) == len(set(ind_actual)), 'Individual IDs are not unique.')

        # Correct individual IDs.
        ind_expected = [d[0] for d in expected_data]

        # Make sure the indivual IDs match the expected.
        diff = set(ind_actual).symmetric_difference(ind_expected)
        self.assertTrue(len(diff) == 0, 'The indivual IDs do not match the expected.')

        # Make sure all the data in the records match the expected.
        for i in range(len(actual_data)):
            rec_actual = actual_data[i]
            rec_expected = expected_data[i]

            self.assertEqual(actual_data[i], expected_data[i], 'Data in record for individual ID %s does not match the expected.' % actual_data[i][0])

    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

class TestGetBirthYear(unittest.TestCase):

    def setUp(self):
        logging.info('Setup birth year tests')
        logging.info('------------')

    def test_write_by_csv(self):
        # FIXME: a lot of redundant code here. How to generalize?

        logging.info('Read birth year from GED and write to CSV')
        logging.info('------------')

        # Read the GED file and write genealogy to CSV.
        GetBirthYear(TEST_GED, ACTUAL_BY)

        # Read the CSV that was just created.
        actual_data = read_csv(ACTUAL_BY)

        # Read the "correct" data.
        expected_data = read_csv(EXPECTED_BY)

        self.assertTrue(len(actual_data) == len(expected_data), 'Expected %d rows in genealogy but got %d.' %(len(expected_data), len(actual_data)))

        # Sort both lists by the individual ID (first element of tuple), so
        # that they can be compared directly.
        actual_data = sorted(actual_data, key=lambda x: x[0])
        expected_data = sorted(expected_data, key=lambda x: x[0])

        # Individual IDs.
        ind_actual = [d[0] for d in actual_data]

        # Make sure the IDs are unique.
        self.assertTrue(len(ind_actual) == len(set(ind_actual)), 'Individual IDs are not unique.')

        # Correct individual IDs.
        ind_expected = [d[0] for d in expected_data]

        # Make sure the indivual IDs match the expected.
        diff = set(ind_actual).symmetric_difference(ind_expected)
        self.assertTrue(len(diff) == 0, 'The indivual IDs do not match the expected.')

        # Make sure all the data in the records match the expected.
        for i in range(len(actual_data)):
            rec_actual = actual_data[i]
            rec_expected = expected_data[i]

            self.assertEqual(actual_data[i], expected_data[i], 'Data in record for individual ID %s does not match the expected.' % actual_data[i][0])

    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

class TestGetHashID(unittest.TestCase):

    def setUp(self):
        logging.info('Setup hash ID tests')
        logging.info('------------')

    def test_write_hashid_csv(self):
        logging.info('Read REFN from GED, encrypt it, and write to CSV')
        logging.info('------------')

        # Read the GED file and write genealogy to CSV.
        gedreader = GetEncryptedID(TEST_GED, ACTUAL_HASHID)

        # Read the CSV that was just created.
        actual_data = read_csv(ACTUAL_HASHID)

        logging.info('Test reformatting REFN and encrypting it')
        logging.info('------------')

        # All these REFN are equivalent.
        refn_list = ['19000101123', '19000101-123', '19000101 123']

        # Reformat all REFN.
        pid_list = [gedreader.reformat_refn(refn) for refn in refn_list]

        # Check PID formatting.
        for pid in pid_list:
            check_pid(pid)

        # If reformatting of a REFN is not possible, None is returned. This shouldn't happen here.
        self.assertTrue(None not in pid_list, 'Reformatting of one or more REFN failed.')

        # Encrypt the PIDs.
        encrypted_pid = [encrypt(refn) for refn in pid_list]

        # Since all REFN are equivalent, there should only be one unique hash ID.
        self.assertTrue(len(set(encrypted_pid)) == 1, 'Encrypting of one or more REFN failed.')


    def tearDown(self):
        logging.info('------------')
        logging.info('Teardown')

if __name__ == '__main__':
    unittest.main()
