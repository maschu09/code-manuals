import os

import cleanttl
from ttlhead import ttlhead


def main():
    if not os.path.exists('ttl/def'):
        os.mkdir('ttl/def')
    with open('ttl/def/bulk_bufr4.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<BUFR4> a reg:Register, owl:Ontology, ldp:Container ;\n')
        fhandle.write('\trdfs:label "WMO No. 306 Vol FM 94 BUFR (edition 4)" ;\n')
        fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 FM 94 BUFR (edition 4)- Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol."@en ;\n')
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

if __name__ == '___main__'
    cleanttl.clean()
    main()
