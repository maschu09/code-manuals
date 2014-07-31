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
    reservedstrs = []
    for flag in cflags:
        container = flag[1].replace('"','')
        if len(container) != 6:
            raise ValueError('{} not recognised (reg)'.format(flag))
        fv = flag[3].replace('"','')
        if len(fv.split('-')) == 1:
            try:
                val = int(fv)
                urilabel = '<{}-{}-{}/{}>'.format(container[0], container[1:3],
                                                  container[3:6], val)
                if urilabel.split('/')[0] == collabel:
                    raise ValueError('wrong col\n{}'.format(flag))
                if urilabel in members:
                    raise ValueError('member already declared\n{}'.format(flag))
                label = flag[4].replace('""', "''")
                elemstr = '{} a skos:Concept ; \n'.format(urilabel)
                if not label:
                    label = '""'
                elemstr += '\trdfs:label {}@en ;\n'.format(label)
                elemstr += '\tskos:notation {} ;\n'.format(val)
                elemstr += '\tbufrcommon:fxy {} ;\n'.format(flag[1])
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
                if flag[4].startswith('"Reserved'):
                    reservedstrs.append(elemstr)
                else:
                    members.append(urilabel)
                    elemstrs.append(elemstr)
            except ValueError:
                pass

        else:
            startfv = int(fv.split('-')[0])
            endfv = int(fv.split('-')[1])
            fvs = range(startfv, endfv+1)
            if container == '020089':
                #import pdb; pdb.set_trace()
                for fv in fvs:
                    if fv < 10:
                        label = '0.0{}'.format(fv)
                    elif fv < 100:
                        label = '0.{}'.format(fv)
                    else:
                        #raise ValueError('no label inferred for {}'.format(flag))
                        continue
                    urilabel = '<{}-{}-{}/{}>'.format(container[0], container[1:3],
                                                  container[3:6], fv)
                    if urilabel.split('/')[0] == collabel:
                        raise ValueError('wrong col\n{}'.format(flag))
                    if urilabel in members:
                        raise ValueError('member already declared\n{}'.format(flag))
                    elemstr = '{} a skos:Concept ; \n'.format(urilabel)
                    elemstr += '\tskos:notation {} ;\n'.format(fv)
                    elemstr += '\tbufrcommon:fxy {} ;\n'.format(flag[1])
                    elemstr += '\trdfs:label "{}"@en ;\n'.format(label)
                    elemstr += '\t.\n'
                    members.append(urilabel)
                    elemstrs.append(elemstr)
            # for fv in fvs:
            #     urilabel = '<{}-{}-{}/{}>'.format(container[0], container[1:3],
            #                                       container[3:6], fv)
            #     if urilabel.split('/')[0] == collabel:
            #         raise ValueError('wrong col\n{}'.format(flag))
            #     if urilabel in members:
            #         raise ValueError('member already declared\n{}'.format(flag))
            #     elemstr = '{} a skos:Concept ; \n'.format(urilabel)
            #     elemstr += '\tskos:notation {} ;\n'.format(fv)
            #     elemstr += '\trdfs:label "Reserved"@en ;\n'.format(flag[4])
            #     elemstr += '\tdct:description "Reserved for future use"@en ;\n'
            #     elemstr += '\t.\n'
            #     reservedstrs.append(elemstr)


    colstr = '{} a skos:Collection ;\n'.format(collabel)
    colstr += 'rdfs:label {} ;\n'.format(cflags[0][2])
    colstr += '\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n'
    colstr += '\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n'
    colstr += '\tskos:member '
    astr = ',\n\t\t'.join(members)
    colstr += astr
    colstr += '\t.\n\n'
    if members:
        with open('ttl/bufr4/codeflag/bulk_{}.ttl'.format(cflags[0][1].replace('"','')), 'w') as fhandle:
            fhandle.write(ttlhead)
            fhandle.write(colstr)
            fhandle.write('\n'.join(elemstrs))
        ## reserved cases too hard to handle with current API limitations
        # if reservedstrs:
        #     cname = cflags[0][1].replace('"','')
        #     fname = '{}-{}-{}'.format(cname[0], cname[1:3], cname[3:6])
        #     os.mkdir('ttl/bufr4/codeflag/{c}'.format(c=fname))
        #     with open('ttl/bufr4/codeflag/{c}/rsvd_{c}.ttl'.format(c=fname), 'w') as fhandle:
        #         fhandle.write(ttlhead)
        #         fhandle.write('\n'.join(reservedstrs))

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
    if not os.path.exists('ttl/bufr4'):
        os.mkdir('ttl/bufr4')
        ##register declaration in bufrcommon
    if not os.path.exists('ttl/bufr4/codeflag'):
        os.mkdir('ttl/bufr4/codeflag')
        with open('ttl/bufr4/codeflag.ttl', 'w') as fhandle:
            fhandle.write(ttlhead)
            fhandle.write('<codeflag> a reg:Register ;\n')
            fhandle.write('\tdc:description "WMO No. 306 FM 94 BUFR (edition 4) Code and Flag tables."@en ;\n')
            fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
            fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
            fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
            fhandle.write('\trdfs:label "BUFR4 Code and Flag table"@en.\n')

def main():
    topfilewrite()
    cflags = readfile()
    makettl(cflags)

if __name__ == '__main__':
    cleanttl.clean()
    main()
