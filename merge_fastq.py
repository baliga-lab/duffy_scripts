#!/usr/bin/env python

import os
import sys
import argparse
import re
from collections import defaultdict
import subprocess

def get_merge_files_rec(indir, mate1, mate2):
    entries = os.listdir(indir)
    for e in entries:
        path = os.path.join(indir, e)
        if os.path.isdir(path):
            get_merge_files_rec(path, mate1, mate2)
        else:
            if e.endswith('fastq') or e.endswith('fastq.gz'):
                if e.find('_R1_001.') >= 0:  # Mate1
                    filename = re.sub(r'_L00.+', '', e) + '_R1.fastq.gz'
                    mate1[filename].append(os.path.join(indir, e))
                if e.find('_R2_001.') >= 0:  # Mate2
                    filename = re.sub(r'_L00.+', '', e) + '_R2.fastq.gz'
                    mate2[filename].append(os.path.join(indir, e))

def get_merge_files(indir):
    mate1 = defaultdict(list)
    mate2 = defaultdict(list)
    get_merge_files_rec(indir, mate1, mate2)
    return mate1, mate2

def combine(mate_dir, outdir):
    for dest, infiles in mate_dir.items():
        #print("merging to %s: %s" % (dest, str(infiles)))
        #print("merging to %s: %s" % (dest, str(infiles)))
        command = ['zcat', '-f']
        command.extend(infiles)
        command.extend(['|', 'gzip', '>', os.path.join(outdir, dest)])
        com = ' '.join(command)
        print(com)
        retval = subprocess.call(com, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="merge_fastq.py - merge multiple FASTQ files")
    parser.add_argument('indir', help='input directory')
    parser.add_argument('outdir', help='output directory')
    args = parser.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    mate1, mate2 = get_merge_files(args.indir)
    combine(mate1, args.outdir)
    combine(mate2, args.outdir)
