#!/usr/bin/env python
'''
'''

from ged4py import GedcomReader
from aebsDButils.utils import encrypt, check_pid, format_date_year
import sys, re, logging, hashlib

logging.basicConfig(level=logging.INFO)


class Ged2Csv(object):
    def __init__(self, ged_path, csv_path):
         self.ged_path = ged_path
         self.csv_path = csv_path
         self.data = []

         logging.info('Reading from GED file: ' + ged_path)
         logging.info('Writing to CSV file: ' + csv_path)

    def format_rin(self, rin):
        '''
        Extract RIN from GEDCOM individual ID. For example, if the ID in the GEDCOM
        file is "@I123@", we get the ID "123".
        '''
        return rin[2:-1]

    def write_csv(self, header=None):
        '''
        Write records in `self.data` to CSV. `self.data` must be a list of tuples of the same length,
        and the tuples must contain string elements.
        '''

        sep = ','

        # Various checks for the data to write.
        assert len(self.data) > 0, 'Error: no data to write.'
        assert isinstance(self.data, list), 'Error: "data" must be a list of tuples.'

        len_record0 = len(self.data[0])

        logging.info('Writing CSV with %d columns and %d rows.' % (len_record0, len(self.data)))

        for i, record in enumerate(self.data):
            assert isinstance(record, tuple), 'Error: "data" must be a list of tuples.'
            assert len(record) == len_record0, 'Error: record %d in data has length %d.' % len(record)

        if header is not None:
            assert sep in header, 'Error: field separator "%s" is not in header "%s".' % (sep, header)
            assert len(header.split(',')) == len_record0, 'Error: header and records do not have the same number of columns.'

            logging.info('Writing file with columns: ' + header)

        with open(self.csv_path, 'w') as fid:
            if header is not None:
                # Write header to file.
                fid.write(header + '\n')
            for record in self.data:
                line = sep.join(record)
                fid.write(line + '\n')

class Ged2Genealogy(Ged2Csv):
    def __init__(self, ged_path, csv_path):
         # Call super-class constructor to initalize genealogy.
         super(Ged2Genealogy, self).__init__(ged_path, csv_path)

         self.ged_reader()

         header = 'ind,father,mother,sex'

         self.write_csv(header)


    def ged_reader(self):
        count_none_rin = 0

        # Initialize GED parser.
        with GedcomReader(self.ged_path, encoding='utf-8') as parser:
            # iterate over all INDI records
            for i, record in enumerate(parser.records0('INDI')):
                # Get individual RIN ID.
                ind_ref = self.format_rin(record.xref_id)

                # Get the RIN ID of the individuals parents.
                # If the parent does not exist, set to 0.

                # Get father ID.
                fa = record.father
                fa_ref = '0'
                if not fa is None:
                    if fa.xref_id is not None:
                        fa_ref = self.format_rin(fa.xref_id)

                # Get mother ID.
                mo = record.mother
                mo_ref = '0'
                if not mo is None:
                    if mo.xref_id is not None:
                        mo_ref = self.format_rin(mo.xref_id)

                # Get information about individual in a dictionary.
                ind_records = {r.tag: r for r in record.sub_records}

                sex = ind_records['SEX'].value

                # Append a tuple to the data list.
                record = (ind_ref, fa_ref, mo_ref, sex)
                self.data.append(record)


class GetBirthYear(Ged2Csv):
    def __init__(self, ged_path, csv_path):
         # Call super-class constructor to initalize genealogy.
         super(GetBirthYear, self).__init__(ged_path, csv_path)

         self.ged_reader()

         header = 'ind,birth_year'

         self.write_csv(header)


    def ged_reader(self):
        count_none_rin = 0

        # Initialize GED parser.
        with GedcomReader(self.ged_path, encoding='utf-8') as parser:
            n_na = 0
            # iterate over all INDI records
            for i, record in enumerate(parser.records0('INDI')):
                # Get individual RIN ID.
                ind_ref = self.format_rin(record.xref_id)

                # Get information about individual in a dictionary.
                ind_records = {r.tag: r for r in record.sub_records}

                birth = ind_records.get('BIRT')

                # If birth year is not found in record, it is set to NA.
                birth_year = 'NA'
                if birth is not None:
                    birth_records = {r.tag: r for r in birth.sub_records}

                    # Get birth year of individual.
                    birth_date_record = birth_records.get('DATE')  # Date record, or None.
                    if birth_date_record is not None:
                        # Get the birth date as a string.
                        birth_date_str = str(birth_date_record.value)

                        # Unfortunately, the dates are inconsistently formateed.
                        # Use dateutils to automatically parse the date and get the birth year.
                        birth_year_fmt = format_date_year(birth_date_str)

                        # If we were not able to parse the date, use NA.
                        if birth_year_fmt is not None:
                            birth_year = birth_year_fmt
                        else:
                            logging.info('Could not parse birth date of record %s: %s' % (ind_ref, birth_date_str))

                if birth_year == 'NA':
                    n_na += 1

                # Append a tuple to the data list.
                record = (ind_ref, birth_year)
                self.data.append(record)

        logging.info('Number of records with NA birth year: %d' % n_na)


class GetEncryptedID(Ged2Csv):
    def __init__(self, ged_path, csv_path):
         # Call super-class constructor to initalize genealogy.
         super( GetEncryptedID, self).__init__(ged_path, csv_path)

         self.ged_reader()

         header = 'ind,hash_id'

         self.write_csv(header)

    def reformat_refn(self, refn):
        '''
        Reformat REFN. The REFN is in the format:
        yyyymmddxxx

        That is, year, month, day and three digits. We want it in this format:
        ddmmyyxxx
        '''

        # Make a copy of the original REFN, as we will be over-writing it.
        refn_orig = refn

        # Remove all whitespace from REFN.
        refn = ''.join(refn.split())

        # If the ID contains a hyphen, remove it.
        idx = refn.find('-')
        if idx > -1:
            # Hyphen found. Remove it from string.
            refn = refn[:idx] + refn[idx+1:]

        # Check formatting of ID.
        if len(refn) != 11:
            logging.warning('REFN should be of length 11 (excluding hyphen). Ignoring record with REFN: %s' % refn_orig)
            return None

        # REFN ending with "000" are not "real" IDs.
        if refn[-3:] == '000':
            return None

        # Get birth date and three cipher ID from REFN.
        yyyy = refn[:4]
        mm = refn[4:6]
        dd = refn[6:8]
        xxx = refn[8:11]

        # Use two last digits of date.
        yy = yyyy[-2:]

        # Format new ID.
        pid = dd + mm + yy + xxx

        return pid


    def ged_reader(self):
        count_none_rin = 0

        # Initialize GED parser.
        with GedcomReader(self.ged_path, encoding='utf-8') as parser:
            n_na = 0
            # iterate over all INDI records
            for i, record in enumerate(parser.records0('INDI')):
                # Get individual RIN ID.
                ind_ref = self.format_rin(record.xref_id)

                # Get information about individual in a dictionary.
                ind_records = {r.tag: r for r in record.sub_records}

                # Get the record with tag "REFN".
                refn = ind_records.get('REFN')

                # If we are not able to make an encrypted ID, it will be "NA".
                hash_id = 'NA'
                if refn is not None:
                    refn = refn.value

                    # Reformat the ID.
                    pid = self.reformat_refn(refn)

                    # If it was possible to get the ID in the correct format, we encrypt
                    # it using sha256.
                    if pid is not None:
                        # Check that the personal ID is correctly formatted.
                        pid_ok = check_pid(pid)

                        if pid_ok:
                            # Encrypt the personal ID.
                            hash_id = encrypt(pid)
                        else:
                            logging.warning('PID %s (corresponding to REFN %s) does not contain a proper date' %(pid, refn))

                if hash_id == 'NA':
                    n_na += 1

                # Append a tuple to the data list.
                record = (ind_ref, hash_id)
                self.data.append(record)

        logging.info('Number of records with NA hash ID: %d' % n_na)
