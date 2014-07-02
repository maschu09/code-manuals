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
cffile = 'BUFRCREX_22_0_1/BUFRCREX_22_0_1_CodeFlag_en.txt'

#2090.00,"010063","Characteristic of pressure tendency","0","Increasing, then decreasing; atmospheric pressure the same or higher than three hours ago",,,,"Operational"
#51.00,"001036","Agency in charge of operating the observing platform","124176-156000","Reserved",,,,"Operational"


bcfline = re.compile(r'(^[0-9]+?\.[0-9]+?),'
                      '("[0-9]+?"),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '(".*?"|\B),'
                      '("[a-zA-Z]*")')

def parsebcf(line):
    res = None
    if not line.startswith('"No",'):
        matcher = bcfline.match(line)
        if matcher:
            if not len(matcher.groups()) == 9:
                raise ValueError('{}\nhas wrong number of elems'.format(line))
            res = matcher.groups()
    return res


def readfile():
    lines = 0
    codeflags = []

    response = urllib2.urlopen(wmo_url)

    zipfile = ZipFile(StringIO(response.read()))
    for line in zipfile.open(cffile).readlines():
        lines += 1
        parsed = parsebcf(line)
        if parsed:
            codeflags.append(parsed)

    if len(codeflags) != lines-1:
        raise ValueError('missing lines\n'
                         '{} lines, {} codeflags'.format(lines, len(codeflags)))
    return codeflags


def make_collection(cflags):
    members = []
    first_container = cflags[0][1]
    first_container = first_container.replace('"','')
    collabel = '<{}-{}-{}>'.format(first_container[0], first_container[1:3],
                                   first_container[3:6])
    elemstrs = []
    for flag in cflags:
        container = flag[1].replace('"','')
        if len(container) != 6:
            raise ValueError('{} not recognised (reg)'.format(flag))
        # this needs addressing 
        # if flag[8] != '"Operational"':
        #     raise ValueError('{} is not Operational'.format(flag))
        try:
            fv = flag[3].replace('"','')
            val = int(fv)
            urilabel = '<{}-{}-{}/{}>'.format(container[0], container[1:3],
                                              container[3:6], val)
            if urilabel.split('/')[0] == collabel:
                raise ValueError('wrong col\n{}'.format(flag))
            if urilabel in members:
                raise ValueError('member already declared\n{}'.format(flag))
            members.append(urilabel)
            elemstr = '{} a skos:Concept ; \n'.format(urilabel)
            elemstr += '\trdfs:label {}@en ;\n'.format(flag[4])
            elemstr += '\tskos:notation {} ;\n'.format(fv)
            elemstr += '\t<http://codes.wmo.int/def/BUFR4/FXY> {} ;\n'.format(flag[1])
            if flag[5]:
                elemstr += '\tskos:note {}@en;\n'.format(flag[5])
            if flag[6]:
                elemstr += '\tskos:note {}@en;\n'.format(flag[6])
            if flag[7]:
                elemstr += '\tskos:note {}@en;\n'.format(flag[7])
            if urilabel == '<0-20-086/6>':
                elemstr += '\tdct:description "Snow or ice on the ground that has been reduced to a soft watery mixture by rain, warm temperature, and/or chemical treatment."@en ;\n'
                elemstr += '\trdfs:label "Neige fondante"@fr ;\n'
                elemstr += '\tdct:description "Neige ou de glace sur le sol qui a \u00E9t\u00E9 r\u00E9duite \u00E0 un doux m\u00E9lange aqueux par la pluie, la temp\u00E9rature chaude et / ou le traitement chimique."@fr ;\n'
            elemstr += '\t.\n'
            elemstrs.append(elemstr)
        except ValueError:
            pass

    colstr = '{} a skos:Collection ;\n'.format(collabel)
    colstr += 'rdfs:label "" ;\n'
    colstr += '\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n'
    colstr += '\trdfs:member '
    astr = ',\n\t\t'.join(members)
    colstr += astr
    colstr += '\t.\n\n'
    with open('ttl/bufr4/bulk_{}.ttl'.format(cflags[0][1].replace('"','')), 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write(colstr)
        fhandle.write('\n'.join(elemstrs))


def makettl(cflags):
    fxy = cflags[0][1]
    acol_flags = []
    for flag in cflags:
        if not flag[1] == fxy:
            make_collection(acol_flags)
            fxy = flag[1]
            acol_flags = []
        acol_flags.append(flag)
        


def topfilewrite():
    if not os.path.exists('ttl/def'):
        os.mkdir('ttl/def')
    if not os.path.exists('ttl/def/bufr4'):
        os.mkdir('ttl/def/bufr4')

    with open('ttl/def/bufr4/bulk_bufr4.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<BUFR4> a reg:Register, owl:Ontology, ldp:Container ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 FM 94 BUFR (edition 4)" ;\n')
        fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 FM 94 BUFR (edition 4)- Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol I.2."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:member <BUFR4/FXY>,<BUFR4/dataWidth_Bits>, <BUFR4/referenceValue>, \n')
        fhandle.write('\t\t<BUFR4/scale> ; \n')
        fhandle.write("""
<BUFR4/FXY>
    a owl:ObjectProperty ; 
    rdfs:label "FXY"@en ; 
    rdfs:comment "6-digit BUFR descriptor for Element (from Table B) or Operator (from Table C)."@en ; 
    rdfs:range xsd:string ;
    .

<BUFR4/DataWidth_Bits> 
    a owl:ObjectProperty ; 
    rdfs:label "Data width (bits)"@en ; 
    rdfs:comment "Number of bits that are used when encoding the value of the BUFR Table B Element in WMO No. 306 Vol I.2 FM 94 BUFR."@en ; 
    rdfs:range xsd:integer ; 
    .

<BUFR4/ReferenceValue> 
    a owl:ObjectProperty ;
    rdfs:label "Reference value"@en ; 
    rdfs:comment "Reference value used when encoding the value of the BUFR Table B Element in WMO No. 306 Vol I.2 FM 94 BUFR."@en ; 
    rdfs:range xsd:integer ; 
    .

<BUFR4/Scale> 
    a owl:ObjectProperty ;
    rdfs:label "Scale"@en ; 
    rdfs:comment "Scale factor used when encoding the value of the BUFR Table B Element in WMO No. 306 Vol I.2 FM 94 BUFR."@en ; 
    rdfs:range xsd:integer ; 
    .
        """)

    if not os.path.exists('ttl/bufr4'):

def main():
    topfilewrite()
    cflags = readfile()
    makettl(cflags)

if __name__ == '__main__':
    cleanttl.clean()
    main()
