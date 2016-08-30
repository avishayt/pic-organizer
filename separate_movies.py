#!/usr/bin/python

import os
import sys

src = sys.argv[1]
dst = sys.argv[2]

for root, directories, filenames in os.walk(src):
    for filename in filenames:
        if filename.lower().endswith('.mp4') or filename.lower().endswith('.mov') or filename.lower().endswith('.avi'):
            dst_root = root.replace(src, dst)
            src_full = os.path.abspath(os.path.join(root, filename))
            dst_full = os.path.abspath(os.path.join(dst_root, filename))
            try:
                os.makedirs(os.path.dirname(dst_full))
            except OSError:
                pass
            os.rename(src_full, dst_full)
