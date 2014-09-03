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



#def writettl(codeflags):
def writettl():
    if not os.path.exists('ttl/def'):
        os.mkdir('ttl/def')
    # os.mkdir('ttl/def/grib')

    with open('ttl/def/bulk_gribe1.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<grib1> a reg:Register, owl:Ontology, ldp:Container ;\n')
        fhandle.write('rdfs:label "WMO No. 306 FM 92 GRIB (edition1) schemata" ;\n')
        fhandle.write('\tdct:description "Schemata required to support WMO No. 306 FM 92 GRIB (edition1)  - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 FM 92 GRIB (edition1)."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:member <grib1/table2version>, '
                      '<grib1/indicatorOfParameter> ;\n')
        fhandle.write('\t.\n')
        fhandle.write('<grib1/table2version> a owl:ObjectProperty ;\n'
                      '\trdfs:label "table 2 version"@en ;\n'
                      '\trdfs:comment "Object property describing the table 2 version used by a GRIB (edition 1) message."@en ;\n'
                      '\trdfs:range rdf:Literal ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "table2version" ;\n'
                      '\trdfs:isDefinedBy <grib1>\n'
                      '\t.\n\n')
        fhandle.write('<grib1/indicatorOfParameter> a owl:ObjectProperty ;\n'
                      '\trdfs:label "parameter indicator"@en ;\n'
                      '\trdfs:comment "Object property describing the indicator of parameter for a GRIB (edition 1) message."@en ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "indicatorOfParameter" ;\n'
                      '\trdfs:isDefinedBy <grib1>\n'
                      '\t.\n\n')

def main():
    #codeflags = readfile()
    writettl()

if __name__ == '__main__':
    cleanttl.clean()
    main()
