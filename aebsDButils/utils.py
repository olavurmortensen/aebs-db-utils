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
    '''

    assert is_int(pid), 'Error: personal ID is not an integer: ' + pid

    assert len(pid) == 9, 'Error: personal ID must be 9 digits long.'

    # Check that the "date" part of the ID is a proper date.
    pid_date = pid[:-3]

    try:
        datetime.datetime.strptime(pid_date, '%d%m%y')
    except ValueError:
        assert False, 'Error: personal ID does not contain a proper date: ' + pid

    return True

