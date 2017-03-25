#!/usr/bin/env python

# pylint: disable=missing-docstring, locally-disabled, invalid-name, line-too-long, anomalous-backslash-in-string

import mmap
import datetime
import sys
import getopt
import time
import os


def usage():
    print 'Usage:\n\t', sys.argv[0], '-t YYYYMMDDHHMMSS [-m] mkv-file'
    print '''
        -t YYYYMMDDHHMMSS   Change DateUTC field to this date/time
        -m                  Modify file's atime & mtime as well
'''
    sys.exit(1)

def convert(int_value):
    encoded = format(int_value, 'x').zfill(16)
    return encoded.decode('hex')

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y%m%d%H%M%S')
    except ValueError:
        print 'Incorrect data format, should be YYYYMMDDHHMMSS'
        return 1
    return 0

def main():
    modtime = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:m')
    except getopt.GetoptError:
        usage()

    for opt, arg in opts:
        if opt == '-t':
            dateutc = arg
        elif opt == '-m':
            modtime = True
        else:
            usage()

    if len(args) < 1:
        usage()

    if validate(dateutc) != 0:
        sys.exit(1)

    mkvfile = args[0]

    try:
        mkvf = open(mkvfile, 'r+b')
    except IOError:
        print 'ERROR: Unable to open MKV file - %s' %(mkvfile)
        sys.exit(1)

    filemmap = mmap.mmap(mkvf.fileno(), 0)
    seekpos = filemmap.find('\x44\x61\x88')
    if filemmap.seek(seekpos) != -1:
        tzero = datetime.datetime(2001, 01, 01, 00, 00, 00)
        ttime = datetime.datetime.strptime(dateutc, '%Y%m%d%H%M%S')
        tdelta = ttime - tzero
        tsec = tdelta.total_seconds()
        if tsec < 0:
            print 'Date & time should be after 2001-01-01 00:00:00'
            sys.exit(1)
        filemmap.write('\x44\x61\x88' + convert(int(tsec) * 1000000000))
        filemmap.flush()
        filemmap.close()
        mkvf.close()
        print 'Update DateUTC field of', mkvfile
        if modtime:
            mtime = time.mktime(time.strptime(dateutc, '%Y%m%d%H%M%S'))
            os.utime(mkvfile, (mtime, mtime))
            print 'Updated atime & mtime of', mkvfile
    else:
        print 'DateUTC field not found'

if __name__ == "__main__":
    main()
