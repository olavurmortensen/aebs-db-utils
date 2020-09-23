#!/usr/bin/env python
'''
'''

from ged4py import GedcomReader
import sys, re, logging
from dateutil.parser import parse

logging.basicConfig(level=logging.INFO)


class Ged2Csv(object):
    def __init__(self, ged_path, csv_path):
         self.ged_path = ged_path
         self.csv_path = csv_path
         self.data = []

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

        logging.info('Writing %d records to CSV.' % len_record0)

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

                fa = record.father
                fa_ref = '0'
                if not fa is None:
                    if fa.xref_id is not None:
                        fa_ref = self.format_rin(fa.xref_id)

                mo = record.mother
                mo_ref = '0'
                if not mo is None:
                    if mo.xref_id is not None:
                        mo_ref = self.format_rin(mo.xref_id)

                # Get information about individual in a dictionary.
                ind_records = {r.tag: r for r in record.sub_records}

                sex = ind_records['SEX'].value

                birth = ind_records.get('BIRT')

                # NOTE: some individuals are "unknown" in AEBS and usually have no "BIRT" record.
                # Such individuals will always have parental records "0". Therefore, when reconstructing
                # a genealogy in "scripts/lineage.py", any lineage will stop at such an "unknown"
                # individual.

                # If birth year or place is not found in record, it is set to NA.
                birth_year = 'NA'
                birth_place = 'NA'
                if birth is not None:
                    birth_records = {r.tag: r for r in birth.sub_records}

                    # Get birth year of individual.
                    birth_date_record = birth_records.get('DATE')  # Date record, or None.
                    if birth_date_record is not None:
                        # Get the birth date as a string.
                        birth_date_str = str(birth_date_record.value)

                        # Unfortunately, the dates are inconsistently formateed.
                        # Use dateutils to automatically parse the date and get the birth year.
                        # If this fails, we simply skip it.
                        try:
                            dt = parse(birth_date_str)
                            birth_year = dt.year
                        except:
                            birth_year = None
                            logging.info('Could not parse birth date of record %s: %s' % (ind_ref, birth_date_str))

                    # Get birth place of individual.
                    birth_place = birth_records.get('PLAC')  # Get the record with tag "PLAC".
                    if birth_place is not None:
                        birth_place = birth_place.value

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
            # iterate over all INDI records
            for i, record in enumerate(parser.records0('INDI')):
                # Get individual RIN ID.
                ind_ref = self.format_rin(record.xref_id)

                # Get information about individual in a dictionary.
                ind_records = {r.tag: r for r in record.sub_records}

                birth = ind_records.get('BIRT')

                # If birth year or place is not found in record, it is set to NA.
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
                        # If this fails, we simply skip it.
                        try:
                            dt = parse(birth_date_str)
                            birth_year = str(dt.year)
                        except:
                            logging.info('Could not parse birth date of record %s: %s' % (ind_ref, birth_date_str))

                # Append a tuple to the data list.
                record = (ind_ref, birth_year)
                self.data.append(record)


