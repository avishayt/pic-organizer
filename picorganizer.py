#!/usr/bin/python

import argparse
import os

import copyfiles
import extractdate
import organizesubjects

DATE_TOPIC_LIST = []

def main():
    args = parse_args()

    extractor = extractdate.DateExtractor()
    organizer = organizesubjects.SubjectOrganizer(args.skew_seconds)
    copier = copyfiles.FileCopier(args.dest_dir, args.copy)
    failed = []

    for root, _, files in os.walk(args.src_dir):
        files.sort()
        for file_name in files:
            abs_file_name = os.path.join(root, file_name)
            print 'Processing file', abs_file_name
            file_date = extractor.get_date(abs_file_name)
            if not file_date:
                failed.append(abs_file_name)
                continue
            print 'Date:', str(file_date)

            subject = organizer.get_subject(abs_file_name, file_date)
            print 'Subject:', subject
            if subject != 'skip':
                copier.copy_file(abs_file_name, file_date, subject)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir', help='Directory to find input files',
                        type=str)
    parser.add_argument('dest_dir', help='Directory to put output files in',
                        type=str)
    parser.add_argument('-s', '--skew_seconds', help='Number of seconds '
                        'difference between pictures considered for same '
                        'subject', type=int, default=900)
    parser.add_argument('-c', '--copy', help='Copy files rather than using '
                        'hardlinks (uses more space but works across mounts)',
                        action='store_true')

    args = parser.parse_args()

    if not os.path.isabs(args.src_dir):
        args.src_dir = os.path.abspath(args.src_dir)
    if not os.path.isabs(args.dest_dir):
        args.dest_dir = os.path.abspath(args.dest_dir)

    return args

if __name__ == '__main__':
    main()
