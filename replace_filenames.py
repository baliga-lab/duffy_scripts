#!/usr/bin/env python3

import os
import argparse
from collections import defaultdict

"""
A script that automates the tedious and error-prone task of substituting
file names in Annotation.txt files from a given RawSequenceFiles directory.

It is assumed that the samples and names will match up, there are no
additional checks other than that there is a sample and an "R" number
"""

def read_sample_filenames(indir):
    entries = os.listdir(indir)
    result = defaultdict(list)
    for e in entries:
      comps = e.replace("fastq.gz", "").split("_")
      rnum = comps[-1]
      samplenum = comps[-2]
      result[samplenum].append(e)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="replace_filenames.py - replace file names in Annotation.txt")
    parser.add_argument('indir', help='input directory')
    parser.add_argument('annfile', help='Annotation.txt file')
    parser.add_argument('outfile', help="output file")
    # a lot of hacks hide in the sampleindex parameter. They help with patching up the
    # sample name, specificilally where the sample number part is hiding.
    # the index is the index of the component, when splitting the sample name by
    # separator '_'. When it is -1, there is no sample number component and the
    # sample number is inferred
    parser.add_argument('--sampleindex', type=int, default=0)
    args = parser.parse_args()
  
    sample_filenames = read_sample_filenames(args.indir)
    for snum, fnames in sample_filenames.items():
      print("%s => %s" % (snum, str(fnames)))
    with open(args.annfile) as infile, open(args.outfile, 'w') as outfile:
      header = infile.readline()
      outfile.write(header)
      linenum = 1
      for line in infile:
        comps = line.split('\t')
        samplename = comps[0]
        if args.sampleindex == -1:
            samplenum = linenum
        else:
          # The sample number format in RawSequenceFiles does not have leading 0s for
          # numbers less than 10, so we need to adjust the format
          samplenum = int(samplename.split('_')[args.sampleindex].replace("S", ""))
        # first try
        snum = "S%d" % samplenum
        files = sorted(sample_filenames[snum])
        #print(snum)
        #print(files)
        print("%s => %s" % (samplename, ",".join(files)))
        # Do a cleanup of comp[0] - no leading digits, no "-"
        comps[0] = samplename.replace("-", "_")
        if args.sampleindex == -1:
            comps[0] = ('S%d_' % samplenum) + comps[0]
        if comps[0][0].isdigit():
          comps[0] = "S" + comps[0]

        comps[1] = ','.join(files)
        outfile.write("%s" % '\t'.join(comps))
        linenum += 1
