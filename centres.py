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

wmo_url = 'http://www.wmo.int/pages/prog/www/WMOCodes/WMO306_vI2/LatestVERSION/Common_20140507_ed.zip'
cffile = 'Common_20140507_ed/Common_C01_20140507_en.txt'


## 1.00,"00","000","0","WMO Secretariat","Operational"


txtline = re.compile(r'(^[0-9]+?\.[0-9]+?),'
                      '"(.*?|\B)",'
                      '"([0-9]+)",'
                      '"([0-9]+)",'
                      '"(.*?|\B)",'
                      '"([a-zA-Z]*)"')

centrerecord = namedtuple('centrerecord', 'CodeFigureForF1F2 CodeFigureForF3F3F3 Octet5GRIB1_Octet6BUFR3 OriginatingGeneratingCentres_en Status')

def parsetxt(line):
    res = None
    matcher = txtline.match(line)
    if matcher:
        if len(matcher.groups()) == 6:
            gs = matcher.groups()
            res = centrerecord(gs[1], gs[2], gs[3], gs[4], gs[5])
        else:
            raise ValueError('matcher should be 6 elems\n'
                             'line is\n'
                             '{}'.format(aline))
    # else:
    #     import pdb; pdb.set_trace()
    return res

def readfile():
    lines = 0
    centres = []

    response = urllib2.urlopen(wmo_url)

    zipfile = ZipFile(StringIO(response.read()))
    for line in zipfile.open(cffile).readlines():
        lines += 1
        parsed = parsetxt(line)
        if parsed:
            centres.append(parsed)


    # if len(centres) != lines-1:
    #     raise ValueError('missing lines\n'
    #                      '{} lines, {} codeflags'.format(lines, len(centres)))
    return centres



def writettl(centres):
    concepts = []
    members = []
    for centre in centres:
        uri = 'http://codes.wmo.int/common/centre/{}'.format(centre.Octet5GRIB1_Octet6BUFR3)
        members.append('<{}>'.format(uri))
        acon = ('<{u}> a skos:Concept ;\n'
                '\trdfs:label "{l}"@en ;\n'
                '\tskos:notation {n} .\n'.format(u=uri,
                                                 l=centre.OriginatingGeneratingCentres_en,
                                                 n=centre.Octet5GRIB1_Octet6BUFR3))
        concepts.append(acon)
    if not os.path.exists('ttl/common'):
        os.mkdir('ttl/common')
    with open('ttl/common/bulk_centre.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<centre> a skos:Collection ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 Centres" ;\n')
        fhandle.write('\tdc:description "Register of Centres registered in  WMO No. 306."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\tskos:member ')
        fhandle.write(', \n\t'.join(members))
        fhandle.write('\t.\n\n')
        fhandle.write('\n'.join(concepts))

def main():
    centres = readfile()
    
    writettl(centres)

if __name__ == '__main__':
    cleanttl.clean()
    main()
