import os

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
        fhandle.write('\t\t<common/wmoAbbreviation>, <common/wmoAbbreviationIA5>, <common/wmoAbbreviationIA2>, \n')
        fhandle.write('\t\t<common/Unit>, <common/unit>, <common/dimensions> ;\n')
        fhandle.write('\t.\n')
        fhandle.write('''
    <common/Edition>
        a owl:Class ;
        rdfs:label "WMO No. 306 Format Edition Number"@en ;
        rdfs:subClassOf skos:Concept ;
        .

    <common/edition>
        a owl:ObjectProperty ;
        rdfs:label "edition number"@en ;
        rdfs:comment "Object property describing the edition number for an entity'."@en ;
        rdfs:range codeform:Edition ;
        .

    <common/Unit>
        a owl:Class ;
        rdfs:label "Unit of measure"@en ;
        rdfs:subClassOf skos:Concept ;
        .

    <common/unit>
        a owl:ObjectProperty ;
        rdfs:label "unit"@en ;
        rdfs:comment "The unit of measure for a physical quantity."@en ;
        rdfs:range codeform:Unit ;
        .

    <common/dimensions>
        a owl:ObjectProperty ;
        rdfs:label "dimensions"@en ;
        rdfs:comment "The dimensions for a physical quantity."@en ;
        .

    <common/wmoAbbreviation> 
        a owl:ObjectProperty ;
        rdfs:label "WMO unit abbreviation"@en ;
        rdfs:comment "Abbreviation for unit of measure - as defined within WMO No. 306 Vol I.2 Common code-table C-6 'List of units for TDCFs'."@en ;
        rdfs:range xsd:string ;
        .

    <common/wmoAbbreviationIA5> 
        a owl:ObjectProperty ;
        rdfs:label "WMO unit abbreviation (IA5)"@en ;
        rdfs:comment "Abbreviation for unit of measure (for IA5/ASCII) - as defined within WMO No. 306 Vol I.2 Common code-table C-6 'List of units for TDCFs'."@en ;
        rdfs:range xsd:string ;
        .

    <common/wmoAbbreviationIA2>
        a owl:ObjectProperty ;
        rdfs:label "WMO unit abbreviation (IA2)"@en ;
        rdfs:comment "Abbreviation for unit of measure (for IA2) - as defined within WMO No. 306 Vol I.2 Common code-table C-6 'List of units for TDCFs'."@en ;
        rdfs:range xsd:string ;
        .

    ''')

if __name__ == '__main__':
    main()
