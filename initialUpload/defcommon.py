import os

import cleanttl
from ttlhead import ttlhead

def main():
    if not os.path.exists('ttl/def'):
        os.mkdir('ttl/def')
    with open('ttl/def.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<def> a reg:Register ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 Vol (common) schemata" ;\n')
        fhandle.write('\tdc:description "Schemata required to support WMO No. 306 - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\t.\n')

    with open('ttl/def/bulk_common.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<common> a reg:Register, owl:Ontology, ldp:Container ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 Code Forms" ;\n')
        fhandle.write('\tdc:description "Schemata required to support WMO No. 306 - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:member <common/Edition>, <common/edition>, \n')
        fhandle.write('\t<common/Centre>, <common/centre>, \n')
        fhandle.write('\t\t<common/wmoAbbreviation>, <common/wmoAbbreviationIA5>, <common/wmoAbbreviationIA2>, \n')
        fhandle.write('\t\t<common/Unit>, <common/unit>, <common/dimensions> ;\n')
        fhandle.write('\t.\n')
        fhandle.write('<common/Edition>'
                      '\ta owl:Class ;\n'
                      '\trdfs:label "WMO No. 306 Format Edition Number"@en ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/edition> a owl:ObjectProperty ;'
                      '\trdfs:label "edition number"@en ;\n'
                      '\trdfs:comment "Object property describing the edition number for an entity."@en ;\n'
                      '\trdfs:range wmocommon:Edition ;\n'
                      '\trdfs:domain wmocodeform:GRIB-message, wmocodeform:BUFR-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "editionNumber" ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/Centre>'
                      '\ta owl:Class ;\n'
                      '\trdfs:label "WMO Centre"@en ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/centre> a owl:ObjectProperty ;'
                      '\trdfs:label "WMO centre"@en ;\n'
                      '\trdfs:comment "Object property describing the WMO centre for an entity."@en ;\n'
                      '\trdfs:range wmocommon:Centre ;\n'
                      '\trdfs:domain wmocodeform:GRIB-message, wmocodeform:BUFR-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "centre" ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/Unit> a owl:Class ;'
                      '\trdfs:label "Unit of measure"@en ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/unit> a owl:ObjectProperty ;'
                      '\trdfs:label "unit"@en ;\n'
                      '\trdfs:comment "The unit of measure for a physical quantity."@en ;\n'
                      '\trdfs:range wmocommon:Unit ;\n'
                      '\trdfs:domain wmocodeform:GRIB-message, wmocodeform:BUFR-message ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/dimensions> a owl:ObjectProperty ;'
                      '\trdfs:label "dimensions"@en ;\n'
                      '\trdfs:comment "The dimensions for a physical quantity."@en ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/wmoAbbreviation> a owl:ObjectProperty ;'
                      '\trdfs:label "WMO unit abbreviation"@en ;\n'
                      '\trdfs:comment "Abbreviation for unit of measure - as defined within WMO No. 306 Common code-table C-6 1List of units for TDCFs1."@en ;\n'
                      '\trdfs:range xsd:string ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/wmoAbbreviationIA5> a owl:ObjectProperty ;'
                      '\trdfs:label "WMO unit abbreviation (IA5)"@en ;\n'
                      '\trdfs:comment "Abbreviation for unit of measure (for IA5/ASCII) - as defined within WMO No. 306 Vol I.2 Common code-table C-6 `List of units for TDCFs`."@en ;\n'
                      '\trdfs:range xsd:string ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')
        fhandle.write('<common/wmoAbbreviationIA2> a owl:ObjectProperty ;'
                      '\trdfs:label "WMO unit abbreviation (IA2)"@en ;\n'
                      '\trdfs:comment "Abbreviation for unit of measure (for IA2) - as defined within WMO No. 306 Vol I.2 Common code-table C-6 `List of units for TDCFs`."@en ;\n'
                      '\trdfs:range xsd:string ;\n'
                      '\trdfs:isDefinedBy <common>;\n'
                      '\t.\n\n')


    with open('ttl/def/bulk_codeform.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<codeform> a owl:Ontology, ldp:Container ;\n'
                      '\trdfs:label "Schemata for WMO code forms";\n'
                      '\trdfs:member <codeform/GRIB-message>, <codeform/BUFR-message> ;\n'
                      '\t.\n\n')
        fhandle.write('<codeform/GRIB-message> a owl:Class ;\n'
                      '\trdfs:isDefinedBy <codeform>;\n'
                      '\trdfs:label "GRIB message" ;\n'
                      '\tdct:description "GRIdded Binary message, as defined '
                      'in WMO No. 306 FM 92 GRIB" ;\n'
                      '\t.\n\n')
        fhandle.write('<codeform/BUFR-message> a owl:Class ;\n'
                      '\trdfs:isDefinedBy <codeform>;\n'
                      '\trdfs:label "BUFR message" ;\n'
                      '\tdct:description "Binary Universal Form for the '
                      'Representation of meteorological data message, as '
                      'defined in WMO No. 306 FM 94 BUFR" ;\n'
                      '\t.\n')

if __name__ == '__main__':
    cleanttl.clean()
    main()
