#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sqlite3

LOCALES = ("en", "fr")
FEATURES = {
    'A': ('ADM1', 'PCL', 'PCLD', 'PCLF', 'PCLI', 'PCLIX', 'PCLS', 'PRSH', 'TERR', 'ZN'),
    'P': ('PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR',
          'PPLS', 'PPLW', 'STLMT'),
}

def comment_ignorer(iterable):
    for line in iterable:
        if len(line) > 0 and not line.startswith('#'):
            yield line

def geonames_rows():
    with open("geonames/allCountries.txt") as src:
        for row in csv.reader(comment_ignorer(src),
                              delimiter="\t", quoting=csv.QUOTE_NONE):
            if row[6] in FEATURES and row[7] in FEATURES[row[6]]:
                yield row

def alternatenames_rows():
    with open("geonames/alternateNames.txt") as src:
        for row in csv.reader(comment_ignorer(src),
                              delimiter="\t", quoting=csv.QUOTE_NONE):
            if row[2] in LOCALES:
                yield row

def countries_rows():
    with open("geonames/countryInfo.txt") as src:
        for row in csv.reader(comment_ignorer(src),
                              delimiter="\t", quoting=csv.QUOTE_NONE):
            yield row

conn = sqlite3.connect('geonames.db')
conn.text_factory = str
cur = conn.cursor()

print "Inserting geonames..."
cur.executemany("insert into geonames values(" + ", ".join(["?"]*19) + ")",
                geonames_rows())

print "Inserting alternate_names..."
cur.executemany("insert into alternate_names values(" + ", ".join(["?"]*8) + ")",
                alternatenames_rows())

print "Inserting countries..."
cur.executemany("insert into countries values(" + ", ".join(["?"]*19) + ")",
                countries_rows())

conn.commit()
conn.close()
