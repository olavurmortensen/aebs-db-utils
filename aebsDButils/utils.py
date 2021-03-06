#!/usr/bin/env python3
'''
'''

import logging, hashlib, datetime

logging.basicConfig(level=logging.INFO)

def is_int(string):
    '''
    Checks whether string represents an integer.
    '''
    try:
        int(string)
    except ValueError:
        return False
    return True


def encrypt(string):
    '''
    Encrypt a string using sha256. Returns encrypted string as a hexadecimal string.
    '''
    # Initialize sha256 object.
    hash_obj = hashlib.sha256()

    # Feed the sha256 algorithm a string.
    hash_obj.update(str.encode(string))

    # Get the encrypted ID as a hexadecimal.
    hash_id = hash_obj.hexdigest()

    return hash_id

def check_pid(pid):
    '''
    Check that the personal ID (string) has the format:
    ddmmyyxxx

    If any problem with the ID is found, an error is raised. Otherwise, the function
    returns `True`.

    Arguments:
    ----------
    pid :   String

    Returns:
    ----------
    Boolean
    '''

    assert is_int(pid), 'Error: personal ID is not an integer: ' + pid

    assert len(pid) == 9, 'Error: personal ID must be 9 digits long.'

    # Check that the "date" part of the ID is a proper date.
    pid_date = pid[:-3]

    try:
        datetime.datetime.strptime(pid_date, '%d%m%y')
    except ValueError:
        return False

    return True


def clean_ged(inpath, outpath):
    '''
    The GED files sometimes have some issues that means ged4py can't parse them. Some
    issues addressed are:
    * Fields spanning multiple lines
    * DOS newlines/linefeed
    * Trailing whitespace

    Arguments:
    ----------
    inpath  :   String
        Input file as a string.
    outpath :   String
        Output file as a string.
    '''

    with open(inpath) as fid:
        intext = fid.read()

    inlines = intext.splitlines()

    n_empty_lines = 0
    n_cont = 0
    outtext = ''
    n_stripped = 0
    for i, line in enumerate(inlines):
        # Strip line of whitespace.
        temp = line
        line = line.strip()

        # Add number of characters stripped from line to tally.
        n_stripped += len(temp) - len(line)

        # Just print first line, which should be '0 HEAD'.
        if i == 0:
            outtext += line
            continue

        if len(line) == 0:
            # Empty line, ignore.
            n_empty_lines += 1
            continue
        elif not is_int(line[0]):
            # Continuation of previous line.
            outtext += ' ' + line
            n_cont += 1
        else:
            # End previous line with newline.
            # Write the next line.
            outtext += '\n' + line

    logging.info('Stripped %d whitespace characters.' % n_stripped)
    logging.info('Discarded %d empty lines' % n_empty_lines)
    logging.info('Collapsed %d lines where a data field contained multiple lines.' % n_cont)

    with open(outpath, 'w') as fid:
        fid.write(outtext)

def format_date_year(date):
    '''
    The dates in AEBS are not represented in any standard fashion, so we have to try
    several formats. If we are able to parse the date, we return the year.

    Arguments:
    ----------
    date    :   String

    Returns:
    ----------
    String
        Year.
    '''

    # If we can't parse the data, None will be returned.
    year = None

    # All the different formats to try.
    date_format_list = ['%d %b %Y', '%b %Y','%Y', 'ABOUT %Y', 'UML %Y', 'FYR %Y', 'FYRI %Y']

    for date_format in date_format_list:
        try:
            # Parse the date.
            dt = datetime.datetime.strptime(date, date_format)
        except ValueError:
            # Could not parse with this format.
            pass
        else:
            # Parsing using this format worked. Get the year from the datetime object.
            year = str(dt.year)

    return year




