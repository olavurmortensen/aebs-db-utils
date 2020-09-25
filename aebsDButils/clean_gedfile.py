#!/usr/bin/env python3
'''
NOTE: this code is untested.
'''

import logging
from aebsDButils.utils import is_int

logging.basicConfig(level=logging.INFO)

def dos2unix(intext):
    '''
    Convert DOS linefeeds (crlf) to unix (lf).

    This code was adapted from the followingproject:
    https://github.com/techtonik/dos2unix

    Arguments:
    ----------
    inpath  :   String
        Input file as a string.
    outpath :   String
        Output file as a string.
    '''

    outsize = 0
    outtext = ''
    for line in intext.splitlines():
        outsize += len(line) + 1
        outtext += line + '\n'

    logging.info("Done. Stripped %s bytes." % (len(intext) - outsize))

    return outtext


def remove_unwanted_newlines(intext):
    '''
    The GED file often has some newlines that causes ged4py to be unable to parse
    the file. We remove these lines in this function.

    Arguments:
    ----------
    inpath  :   String
        Input file as a string.
    outpath :   String
        Output file as a string.
    '''

    inlines = intext.splitlines()

    n_empty_lines = 0
    outtext = ''
    for i, line in enumerate(inlines):
        # Strip line of whitespace.
        line = line.strip()

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
        else:
            # End previous line with newline.
            # Write the next line.
            outtext += '\n' + line

    logging.info('Discarded %d empty lines' % n_empty_lines)

    return outtext

def clean_gedfile(inpath, outpath):
    '''
    Arguments:
    ----------
    inpath  :   String
        Path to input file.
    outpath :   String
        Path to output file.
    '''

    with open(inpath) as fid:
        text = fid.read()

    text_unix = dos2unix(text)
    text_stripped = remove_unwanted_newlines(text_unix)

    with open(outpath, 'w') as fid:
        fid.write(text_stripped)

