import hashlib
import os
import random
import shutil
import string

BLOCKSIZE = 65536

class FileCopier(object):
    def __init__(self, dest_dir, copy):
        self._dest_dir = dest_dir
        self._copy = copy

    def copy_file(self, in_path, date, subject):
        out_dir = self._get_directory_name(date, subject)
        out_file = self._get_file_name(in_path, date)
        self._create_dir(out_dir)
        out_path = os.path.join(out_dir, out_file)
        if os.path.exists(out_path):
            if self._hash_file(in_path) == self._hash_file(out_path):
                print 'File already exists - skipping'
                return
            else:
                basename, extension = os.path.splitext(out_path)
                rand_str = ''.join(random.choice(string.lowercase) for i in range(10))
                out_file = basename + '-' + rand_str + extension
                out_path = os.path.join(out_dir, out_file)
        self._copy_file(in_path, out_path)

    def _get_directory_name(self, date, subject):
        month_dir = '%(y)s-%(m)s' % {'y': date.year, 'm': date.month}
        subject_dir = ('%(y)s_%(m)s_%(d)s-%(subj)s' %
                       {'y': date.year, 'm': date.month, 'd': date.day,
                        'subj': subject})
        return os.path.join(self._dest_dir, month_dir, subject_dir)

    def _get_file_name(self, in_path, date):
        file_basename = ('%(y)s_%(m)s_%(d)s-%(hr)s_%(min)s_%(sec)s' %
                         {'y': date.year, 'm': date.month, 'd': date.day,
                          'hr': date.hour, 'min': date.minute,
                          'sec': date.second})
        extension = os.path.splitext(in_path)[1]
        return file_basename + extension

    def _create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _hash_file(self, path):
        hasher = hashlib.md5()
        with open(path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

    def _copy_file(self, in_path, out_path):
        print 'Copying file from', in_path, 'to', out_path
        if self._copy:
            shutil.copy2(in_path, out_path)
        else:
            os.link(in_path, out_path)
