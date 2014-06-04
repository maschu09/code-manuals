import os

import cleanttl

ttlhead = '''@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix qudt: <http://qudt.org/schema/qudt#> .
@prefix gribs: <http://codes.wmo.int/def/gribcore/> .
@prefix grib2s: <http://codes.wmo.int/def/grib2/> .
@prefix ldp: <http://www.w3.org/ns/ldp#> .

'''

INPUTS = [('001', 'metre', 'm', 'm', 'M'),
          ('002', 'kilogram', 'kg', 'kg', 'KG')]



def file_write(members, member_elements):
    os.mkdir('ttl/common')
    with open('ttl/common/c6.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)

        fhandle.write('<c-6> a skos:Collection ;\n')
        fhandle.write('\trdfs:label       "List of units for TDCFs"@en ;\n')
        fhandle.write('\tdct:description  "WMO No. 306 Vol I.2 Common Code-table C-6 List of units for TDCFs."@en ;\n')
        fhandle.write('\tdct:modified     "2014-05-15T15:49:31.167Z"^^xsd:dateTime ;\n')
        fhandle.write('\treg:manager      <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\treg:owner        <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tskos:member ')
        fhandle.write(', '.join(members))
        fhandle.write('\t.\n\n')
        fhandle.write('\n'.join(member_elements))

uri_pattern = '<c-6/{}>'

def main():
    cleanttl.clean()
    members = []
    member_elements = []
    for unit in INPUTS:
        members.append(uri_pattern.format(unit[0]))
        m_elem_str = uri_pattern.format(unit[0])
        m_elem_str += ' a skos:Concept ;\n'
        m_elem_str += '\trdfs:label "{}" ;\n'.format(unit[1])
        m_elem_str += '\tskos:prefLabel "{}" ;\n'.format(unit[1])
        m_elem_str += '\tskos:notation "{}" ;\n'.format(unit[3])
        m_elem_str += '\tskos:altLabel "{}" ;\n'.format(unit[2])
        m_elem_str += '\tskos:altLabel "{}" ;\n'.format(unit[4])
        m_elem_str += '\t.\n'
        member_elements.append(m_elem_str)
    file_write(members, member_elements)
    

if __name__ == '__main__':
    main()
