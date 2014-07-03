from collections import namedtuple
from collections import OrderedDict
import glob
import os
import re
import shutil
from StringIO import StringIO
import urllib2
from zipfile import ZipFile

import cleanttl
from ttlhead import ttlhead

wmo_url = 'http://www.wmo.int/pages/prog/www/WMOCodes/WMO306_vI2/LatestVERSION/BUFRCREX_22_0_1.zip'
cffile = 'BUFRCREX_22_0_1/BUFRCREX_22_0_1_TableB_en.txt'


# "No","ClassNo","ClassName_en","FXY","ElementName_en","Note_en","BUFR_Unit","BUFR_Scale","BUFR_ReferenceValue","BUFR_DataWidth_Bits","CREX_Unit","CREX_Scale","CREX_DataWidth_Char","Status"
# 1.00,"00","BUFR/CREX table entries","000001","Table A: entry",,"CCITT IA5","0","0","24","Character","0","3","Operational"


tbline = re.compile(r'(^[0-9]+?\.[0-9]+?),'
                      '("[0-9]+?"),'
                      '(".*?"|\B),'
                      '("[0-9]+?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '("-*[0-9]+?"|\B),'
                      '("-*[0-9]+? *"|\B),'
                      '(" *[0-9]+?"|\B),'
                      '(".*?"|\B),'
                      '("-*[0-9]+?"|\B),'
                      '("[0-9]+?"|\B),'
                      '("[a-zA-Z]*")')

def parsetb(line):
    res = None
    if not line.startswith('\xef\xbb\xbf"No",'):
        matcher = tbline.match(line)
        if matcher:
            if not len(matcher.groups()) == 14:
                raise ValueError('{}\nhas wrong number of elems'.format(line))
            res = matcher.groups()
        else:
            import pdb; pdb.set_trace()
    return res


def readfile():
    lines = 0
    entries = []

    response = urllib2.urlopen(wmo_url)

    zipfile = ZipFile(StringIO(response.read()))
    for line in zipfile.open(cffile).readlines():
        lines += 1
        parsed = parsetb(line)
        if parsed:
            entries.append(parsed)

    if len(entries) != lines-1:
        raise ValueError('missing lines\n'
                         '{} lines, {} entries'.format(lines, len(entries)))
    return entries

def make_collection(entries):
    members = []
    first_container = entries[0][1]
    first_container = first_container.replace('"','')
    collabel = '<{}>'.format(first_container)
    elemstrs = []
    for entry in entries:
        container = entry[1].replace('"','')


def makettl(entries):
    classno = entries[0][1]
    acol_entries = []
    for entry in entries:
        if not entry[1] == classno:
            make_collection(acol_entries)
            classno = entry[1]
            acol_entries = []
        acol_entries.append(entry)

def topfilewrite():
    if not os.path.exists('ttl/bufr4'):
        os.mkdir('ttl/bufr4')
        ##need a register declaration
    if not os.path.exists('ttl/bufr4/b'):
        os.mkdir('ttl/bufr4/b')
        ##need a register declaration

def main():
    topfilewrite()
    entries = readfile()
    makettl(entries)

if __name__ == '__main__':
    cleanttl.clean()
    main()
