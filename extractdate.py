from cStringIO import StringIO
import datetime
import exifread
import os
import re
import sys

from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_metadata import extractMetadata


class DateExtractor(object):
    def get_date(self, input_file):
        base = os.path.basename(input_file).split('.')[0]
        if re.match(r'\d{8}_\d{6}', base):
            creation_date = (base[0:4] + ':' + base[4:6] + ':' + base[6:8] +
                             ':' + base[9:11] + ':' + base[11:13] + ':' +
                             base[13:15])
        else:
            try:
                creation_date = self._get_date_hachoir(input_file)
            except:
                try:
                    creation_date = self._get_date_exif(input_file)
                except:
                    if re.match(r'IMG-\d{8}-WA\d{4}', base):
                        creation_date = (base[4:8] + ':' + base[8:10] + ':' +
                                         base[10:12] + ':0:0:0')
        if creation_date is None:
            print 'Failed to get date information for file', input_file
            return None
        date = creation_date.replace(' ', ':').replace('-', ':').split(':')
        return datetime.datetime(*[int(i) for i in date])

    def _get_date_hachoir(self, input_file):
        filename, realname = unicodeFilename(input_file), input_file
        parser = createParser(filename, realname)
        if not parser:
            raise Exception('Unable to parse file')

        try:
            orig_stderr, sys.stderr = sys.stderr, StringIO()
            metadata = extractMetadata(parser)
        except HachoirError, err:
            raise Exception('Metadata extraction error: %s' % unicode(err))
        finally:
            sys.stderr = orig_stderr

        for meta in metadata:
            if meta.key == 'creation_date':
                return str(meta.values[0].value)
        raise Exception('Date not found')

    def _get_date_exif(self, input_file):
        with open(input_file, 'rb') as file_p:
            tags = exifread.process_file(file_p)
        return str(tags['EXIF DateTimeOriginal'])
