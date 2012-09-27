#!/usr/bin/env python

# osis2usfm.py
# OSIS to USFM transformation script.
#
# Copyright (C) 2012 Jaakko Luttinen
# 
# This file is licensed under Version 3.0 of the GNU General Public
# License.

"""
Python script for transforming Bible in OSIS format to USFM format.
The script transforms OSIS Bible to USFM Bible. It is assumed that the
XML structure of the OSIS file is:

    <osis>
      <osisText>
        <header>
          ... this is ignored ...
        </header>
        <div type="x-testament">
          <div type="book">
            <chapter>
              <verse>
              </verse>
              ...
            </chapter>
            ...
          </div>
        </div>
        <div type="x-testament">
          <div type="book">
            <chapter>
              <verse>
              </verse>
              ...
            </chapter>
            ...
          </div>
        </div>
      </osisText>
    </osis>

No other tags are understood, thus it is a very simple transformation.

Usage:

    python osis2usfm.py inputfile.osis

Outputs a set of files named inputfile_##_XXX.usfm where ## is the
number of the book and XXX is the id of the book.
"""

import xml.etree.ElementTree as ET
import codecs
import sys
from os.path import splitext

filename = sys.argv[1]
basename = splitext(filename)[0]

# Parse XML
tree = ET.parse(filename)

root = tree.getroot()

# Book IDs
ids = (
    'GEN',
    'EXO',
    'LEV',
    'NUM',
    'DEU',
    'JOS',
    'JDG',
    'RUT',
    '1SA',
    '2SA',
    '1KI',
    '2KI',
    '1CH',
    '2CH',
    'EZR',
    'NEH',
    'EST',
    'JOB',
    'PSA',
    'PRO',
    'ECC',
    'SNG',
    'ISA',
    'JER',
    'LAM',
    'EZK',
    'DAN',
    'HOS',
    'JOL',
    'AMO',
    'OBA',
    'JON',
    'MIC',
    'NAM',
    'HAB',
    'ZEP',
    'HAG',
    'ZEC',
    'MAL',
    'MAT',
    'MRK',
    'LUK',
    'JHN',
    'ACT',
    'ROM',
    '1CO',
    '2CO',
    'GAL',
    'EPH',
    'PHP',
    'COL',
    '1TH',
    '2TH',
    '1TI',
    '2TI',
    'TIT',
    'PHM',
    'HEB',
    'JAS',
    '1PE',
    '2PE',
    '1JN',
    '2JN',
    '3JN',
    'JUD',
    'REV',
    )

id_ind = 0
for testament in root[0][1:]:
    for (book_ind, book) in enumerate(testament):
        # Write each book in a separate file
        outfile = basename + ('_%02d_' % (id_ind+1)) + ids[id_ind] + '.usfm'
        f = codecs.open(outfile,
                        mode='w',
                        encoding='utf-8')

        f.write(u"\\id " + ids[id_ind] + "\n")
        f.write(u"\\h \n")
        f.write(u"\\toc2 \n")
        for (chapter_ind, chapter) in enumerate(book):
            f.write(u"\\c %d\n" % (chapter_ind+1))
            for (verse_ind, verse) in enumerate(chapter):
                f.write(u"\\v %d " % (verse_ind+1))
                if verse.text:
                    f.write(verse.text)
                f.write(u"\n")
        id_ind += 1

        f.close()
    
