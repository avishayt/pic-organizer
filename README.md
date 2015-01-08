Simple tool to automate organizing pictures.
It will go through the pictures in the source directory, and ask for a subject.  Any pictures taken around the same time will belong to the same subject (adjust using the -s option).  The default mode is to use hard links rather than copying to improve speed and save disk space.  In the end, you get a set of directories with the following format:

yyyy-mm/yyyy_mm_dd-subject/yyyy_mm_dd-hh_MM_ss.extension


Works with images and movies, as long as they have some standard embedded time stamp (most cameras/phones do)


usage: picorganizer.py [-h] [-s SKEW_SECONDS] [-c] src_dir dest_dir

positional arguments:
  src_dir               Directory to find input files
  dest_dir              Directory to put output files in

optional arguments:
  -h, --help            show this help message and exit
  -s SKEW_SECONDS,      --skew_seconds SKEW_SECONDS
                        Number of seconds difference between pictures
                        considered for same subject
  -c, --copy            Copy files rather than using hardlinks (uses more
                        space but works across mounts)
