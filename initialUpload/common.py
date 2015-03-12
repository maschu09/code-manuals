import os

from ttlhead import ttlhead
import cleanttl

def writettl():
    os.mkdir('ttl/common')
    with open('ttl/common.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<common> a reg:Register ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 common concepts" ;\n')
        fhandle.write('\tdc:description "Register of concepts common across WMO No. 306 formats"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\t.\n')

def main():
    writettl()

if __name__ == '__main__':
    cleanttl.clean()
    writettl()
