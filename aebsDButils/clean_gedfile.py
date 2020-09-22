#!/usr/bin/env python3
'''
NOTE: this code is untested.
'''

import logging

logging.basicConfig(level=logging.INFO)

def dos2unix(inpath, outpath):
    '''
    Convert DOS linefeeds (crlf) to unix (lf).

    This code was copied from the followingproject:
    https://github.com/techtonik/dos2unix

    Arguments:
    ----------
    inpath  :   String
        Path to input file.
    outpath :   String
        Path to output file.
    '''

    content = ''
    outsize = 0
    with open(inpath, 'rb') as infile:
        content = infile.read()
    with open(outpath, 'wb') as output:
        for line in content.splitlines():
	    outsize += len(line) + 1
	    output.write(line + b'\n')

    logging.info("Done. Stripped %s bytes." % (len(content) - outsize))

def is_int(string):
    '''
    Checks whether string represents an integer.
    '''
    try:
        int(string)
    except ValueError:
        return False
    return True

def remove_unwanted_newlines(inpath, outpath):
    with open(inpath) as fid:
        inlines = fid.readlines()

    n_empty_lines = 0
    outtext = ''
    for i, line in enumerate(inlines):
        # Strip line of whitespace.
        line = line.strip()

        # Just print first line, which should be '0 HEAD'.
        if i == 0:
            outtext.append(line)
            continue

        if len(line) == 0:
            # Empty line, ignore.
            n_empty_lines += 1
            continue
        elif not is_int(line[0]):
            # Continuation of previous line.
            outtext.append(' ' + line)
        else:
            # End previous line with newline.
            # Write the next line.
            print('\n' + line, end='')
            outtext.append('\n' + line)

    logging.info('Discarded %d empty lines' % n_empty_lines)

    with open(outpath, 'w') as fid:
        fid.write(outtext)

