# MKVchgdate

Python script to change the DateUTC field in an MKV file.

The DateUTC field is also sometimes known as the encoding date or production date.

Syntax :-

Usage:
    mkvchgdate.py -t YYYYMMDDHHMMSS [-m] mkv-file

        -t YYYYMMDDHHMMSS   Change DateUTC field to this date/time
        -m                  Modify file's atime & mtime as well

