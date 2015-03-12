import glob
import os
import re
import shutil

import cleanttl
from ttlhead import ttlhead


def main():
    with open('ttl/bulk_codeform.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<codeform> a skos:Collection ;\n')
        fhandle.write('\tdc:description  "WMO No. 306 "@en ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 "@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\tskos:member <codeform/grib1> ;\n')
        fhandle.write('\tskos:member <codeform/grib2> ;\n')
        fhandle.write('\tskos:member <codeform/bufr4> ;\n')
        fhandle.write('\t.\n\n')
        fhandle.write('<codeform/grib1> a skos:Concept, wmocommon:Edition ;\n')
        fhandle.write('\trdfs:label "FM 92 GRIB edition 1"@en;\n')
        fhandle.write('\tskos:notation 1 .\n\n')
        fhandle.write('<codeform/grib2> a skos:Concept, wmocommon:Edition ;\n')
        fhandle.write('\trdfs:label "FM 92 GRIB edition 2"@en;\n')
        fhandle.write('\tskos:notation 2 .\n')
        fhandle.write('<codeform/bufr4> a skos:Concept, wmocommon:Edition ;\n')
        fhandle.write('\trdfs:label "FM 94 BUFR edition 4"@en;\n')
        fhandle.write('\tskos:notation 4 .\n')

if __name__ == '__main__':
    cleanttl.clean()
    main()
