#!/usr/bin/env python
'''
'''

import logging

logging.basicConfig(level=logging.INFO)


def read_csv(csv, header=True):
    '''
    '''

    sep = ','

    data = []
    with open(csv) as fid:
        if header:
            header = fid.readline().strip()
        for line in fid:
            # Remove trailing and leading whitespace.
            line = line.strip()
            # Split the row into fields.
            line = line.split(sep)
            # Convert to tuple.
            record = tuple(line)
            # Append record to data list.
            data.append(record)

    return data


