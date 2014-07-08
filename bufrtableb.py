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
from helpers import unit_of_measure
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

# "No","ClassNo","ClassName_en","FXY","ElementName_en",
# "Note_en","BUFR_Unit","BUFR_Scale","BUFR_ReferenceValue","BUFR_DataWidth_Bits",
# "CREX_Unit","CREX_Scale","CREX_DataWidth_Char","Status"
def make_collection(entries):
    members = []
    first_container = entries[0][1]
    first_container = first_container.replace('"','')
    collabel = '<{}>'.format(first_container)
    elemstrs = []
    for entry in entries:
        container = entry[1].replace('"','')
        codeval = entry[3].replace('"','')
        test = (int(container), int(codeval))
        urilabel = '<{}/{}>'.format(container, codeval[-3:])
        elemstr = '{} a skos:Concept ; \n'.format(urilabel)
        label = entry[4].replace('""', '``')
        elemstr += '\trdfs:label {}@en ;\n'.format(label)
        elemstr += '\tbufrcommon:fxy {} ;\n'.format(codeval)
        elemstr += '\tskos:notation {} ;\n'.format(codeval[-3:])
        if entry[5]:
            elemstr += '\tskos:note {}@en ;\n'.format(entry[5])
        unit = unit_of_measure(entry[6].replace('"',''))
        elemstr += '\tbufrcommon:unit <http://codes.wmo.int/common/c-6/{u}> ;\n'.format(u=unit)
        elemstr += '\tbufrcommon:scale {} ;\n'.format(entry[7].replace('"',''))
        elemstr += '\tbufrcommon:referenceValue {} ;\n'.format(entry[8].replace('"',''))
        elemstr += '\tbufrcommon:dataWidth_Bits {} ;\n'.format(entry[9].replace('"',''))
        if entry[10]:
            cunit = unit_of_measure(entry[10].replace('"',''))
            elemstr += '\tcrexcommon:unit <http://codes.wmo.int/common/c-6/{u}> ;\n'.format(u=unit)
        if entry[11]:
            elemstr += '\tcrexcommon:scale {} ;\n'.format(entry[11].replace('"',''))
        if entry[12]:
            elemstr += '\tcrexcommon:referenceValue {} ;\n'.format(entry[12].replace('"',''))
        elemstr += '\t.\n'
        if entry[13] == '"Operational"':
            members.append(urilabel)
            elemstrs.append(elemstr)
        else:
            raise ValueError('status not recognised\n{}'.format(entry))
    colstr = '{} a skos:Collection ;\n'.format(collabel)
    colstr += 'rdfs:label {}@en ;\n'.format(entries[0][2])
    colstr += '\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n'
    colstr += '\tskos:member '
    astr = ',\n\t\t'.join(members)
    colstr += astr
    colstr += '\t.\n\n'
    with open('ttl/bufr4/b/bulk_{}.ttl'.format(entries[0][1].replace('"','')), 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write(colstr)
        fhandle.write('\n'.join(elemstrs))
        



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
        ##register declaration in bufrcommon
    if not os.path.exists('ttl/bufr4/b'):
        os.mkdir('ttl/bufr4/b')
        with open('ttl/bufr4/b.ttl', 'w') as fhandle:
            fhandle.write(ttlhead)
            fhandle.write('<b> a reg:Register ;\n')
            fhandle.write('\tdc:description "WMO No. 306 FM 94 BUFR (edition 4) Table B."@en ;\n')
            fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
            fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
            fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
            fhandle.write('\trdfs:label "BUFR4 table B"@en.\n')



def main():
    topfilewrite()
    entries = readfile()
    makettl(entries)

if __name__ == '__main__':
    cleanttl.clean()
    main()
