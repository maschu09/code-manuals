from collections import namedtuple
from collections import OrderedDict
import glob
import os
import re
from StringIO import StringIO
import urllib2
from zipfile import ZipFile



wmo_url = 'http://www.wmo.int/pages/prog/www/WMOCodes/WMO306_vI2/LatestVERSION/GRIB2_12_0_0.zip'
cffile = 'GRIB2_12_0_0/GRIB2_12_0_0_CodeFlag_en.txt'


aline = ('6.00,'
         '"Code table 0.0 - Discipline of processed data in the GRIB message, number of GRIB Master table",'
         ','
         '"4-9",'
         ','
         '"Reserved",'
         ','
         ','
         '"Operational"')

nearlyall = '[0-9a-zA-Z \\".:()/=+,-]'
nearlyall = '.'

gtxtline = re.compile(r'(^[0-9]+?\.[0-9]+?)(,)'
                      '("{a}*?")(,)'
                      '("{a}*?"|\B)(,)'
                      '("{a}*?"|\B)(,)'
                      '("{a}*?"|\B)(,)'
                      '("{a}*?"|\B)(,)'
                      '("{a}*?"|\B)(,)'
                      '("{a}*?"|\B)(,)'
                      '("[a-zA-Z]*")'.format(a=nearlyall))


gribcodeflag = namedtuple('gribcodeflag', 'Title_en SubTitle_en CodeFlag Value MeaningParameterDescription_en Note_en UnitComments_en Status')

def parsegribtxt(line):
    res = None
    if not line.startswith('"No",'):
        matcher = gtxtline.match(line)
        if matcher:
            if len(matcher.groups()) == 17:
                gs = matcher.groups()
                codeflag = (gribcodeflag(gs[2],gs[4],gs[6],gs[8],gs[10],gs[12],
                                         gs[14],gs[16]))
                res = codeflag
            else:
                raise ValueError('matcher should be 17 elems\n'
                                 'line is\n'
                                 '{}'.format(aline))
        # else:
        #     import pdb; pdb.set_trace()
    return res

lines = 0
codeflags = []

response = urllib2.urlopen(wmo_url)

zipfile = ZipFile(StringIO(response.read()))
#import pdb; pdb.set_trace()
for line in zipfile.open(cffile).readlines():
    lines += 1
    parsed = parsegribtxt(line)
    if parsed:
        codeflags.append(parsed)


# with open(infile, 'r') as grib:
#     for line in grib.readlines():
#         lines += 1
#         parsed = parsegribtxt(line)
#         if parsed:
#             codeflags.append(parsed)

if len(codeflags) != lines-1:
    raise ValueError('missing lines\n'
                     '{} lines, {} codeflags'.format(lines, len(codeflags)))


#pcatptrn = re.compile('^("Product discipline )([0-9]+?)( - Meteorological products")')
pcatptrn = re.compile('^("Product discipline )([0-9]+?)( - .*?")') 

#pnumptrn = re.compile('^("Product discipline )([0-9]+?)( - [a-zA-Z ]*, parameter category )([0-9]+?)(: [a-zA-Z ]*")')
pnumptrn = re.compile('^("Product [D|d]iscipline )([0-9]+?)( - .*?, parameter category )([0-9]+?)(: .*?")')

slashunit = re.compile('^([a-zA-Z]*)/([a-zA-Z]*)')
codeptrn = re.compile('^(\(Code_table_)(4\.[0-9]+?)\)')

## not yet hit issue with '""' in '"??"' strings
## use '``' instead 

## namespaces
## http://codes.wmo.int/def
##     /grib
##        /core
##        /edition1
##        /edition2
##  e.g.  http://codes.wmo.int/def/grib/edition2/Category
##        http://codes.wmo.int/def/grib/edition2/category

def unit_of_measure(code):
    unit = code.UnitComments_en.replace('"','')
    if unit == '-' or unit == 'sigma value' or unit == 'Numeric':
        unit = ''
    if unit == '%':
        unit = '%25'
    unitmatch = slashunit.match(unit)

    if unitmatch:
        if len(unitmatch.groups()) != 2:
            raise ValueError('unit slash parsing failed with unit: {}'.format(unit))
        unit = '{} {}-1'.format(unitmatch.group(1), unitmatch.group(2))
    unit = unit.replace(' ', '_')
    return unit

def makerdf(code):
    res = (None, None, None)
    if code.Title_en.startswith('"Code table 0.0 '):
        c = None
        codeflag = None
        try:
            codeflag = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if codeflag is not None:
            entity = '<http://codes.wmo.int/grib2/codeflag/0.0/{}>'.format(codeflag)
            rdff = ('{e} a skos:Concept, grib2s:Discipline ;\n'
                    '\tgribs:edition <http://codes.wmo.int/gribcore/edition/2>;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, c=codeflag, l=code.MeaningParameterDescription_en))
            res = ('0.0', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.1 '):
        matcher = pcatptrn.match(code.SubTitle_en)
        if not matcher:
            raise ValueError('failed to parse code table 4.1 entry\n'
                             '{}'.format(code))
        disc = None
        cat = None
        if matcher:
            disc = int(matcher.group(2))
        try:
            cat = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if disc is not None and cat is not None:
            entity = '<http://codes.wmo.int/grib2/codeflag/4.1/{d}-{c}>'.format(d=disc, c=cat)
            rdff = ('{e} a skos:Concept, grib2s:Category ;\n'
                    '\tgrib2s:discipline <http://codes.wmo.int/grib2/codeflag/0.0/{d}> ;\n'
                    '\tgribs:edition <http://codes.wmo.int/gribcore/edition/2>;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, d=disc, c=cat, l=code.MeaningParameterDescription_en))
            res = ('4.1', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.2 '):
        matcher = pnumptrn.match(code.SubTitle_en)
        if not matcher:
            raise ValueError('failed to parse code table 4.2 entry\n'
                             '{}'.format(code))
        disc = None
        cat = None
        paramno = None
        datacode = None
        unit = unit_of_measure(code)
        if matcher:
            disc = int(matcher.group(2))
            cat = int(matcher.group(4))
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if disc is not None and cat is not None and paramno is not None:
            unitstr = ''
            if unit:
                unitstr = '\tgribs:unit <http://codes.wmo.int/common/c-6/{u}> ;\n'.format(u=unit)
            datacodestr = ''
            if codeptrn.match(unit):
                datacode = codeptrn.match(unit).group(2)
                unit = ''
            if datacode:
                datacodestr = '\tgrib2s:datacode <http://codes.wmo.int/grib2/codeflag/{}> ;\n'.format(datacode)
            entity = '<http://codes.wmo.int/grib2/codeflag/4.2/{d}-{c}-{pn}>'.format(d=disc, c=cat, pn=paramno)
            rdff = ('{e} a skos:Concept, grib2s:Parameter ;\n'
                    '\tgrib2s:discipline <http://codes.wmo.int/grib2/codeflag/0.0/{d}> ;\n'
                    '\tgrib2s:category <http://codes.wmo.int/grib2/codeflag/4.1/{d}-{c}> ;\n'
                    '\tgribs:edition <http://codes.wmo.int/gribcore/edition/2>;\n'
                    '\tskos:notation {pn} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '{u}{dc}'
                    '\t.\n\n'.format(e=entity, d=disc, c=cat, pn=paramno,
                                     l=code.MeaningParameterDescription_en,
                                     u=unitstr, dc = datacodestr))
            res = ('4.2', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.5 '):
        #import pdb; pdb.set_trace()
        unit = unit_of_measure(code)
        label = code.MeaningParameterDescription_en
        unit = unit_of_measure(code)#.UnitComments_en
        paramno = None
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if paramno is not None:
            unitstr = ''
            if unit:
                unitstr = '\tgribs:unit <http://codes.wmo.int/common/c-6/{u}> ;\n'.format(u=unit)
            entity = '<http://codes.wmo.int/grib2/codeflag/4.5/{s}>'.format(s=paramno)
            rdff = ('{e} a skos:Concept ;\n'
                    '\tgribs:edition <http://codes.wmo.int/gribcore/edition/2>;\n'
                    '\tskos:notation {s} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '{u}'
                    '\t.\n\n'.format(e=entity, s=paramno, l=label, u=unitstr))
            res = ('4.5', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.10 '):
        label = code.MeaningParameterDescription_en
        paramno = None
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if paramno is not None:
            entity = '<http://codes.wmo.int/grib2/codeflag/4.10/{s}>'.format(s=paramno)
            rdff = ('{e} a skos:Concept ;\n'
                    '\tgribs:edition <http://codes.wmo.int/gribcore/edition/2>;\n'
                    '\tskos:notation {s} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, s=paramno, l=label))
            res = ('4.10', entity, rdff)
    return res


cf00 = OrderedDict()
cf41 = OrderedDict()
cf42 = OrderedDict()
cf45 = OrderedDict()
cf410 = OrderedDict()

for cf in codeflags:
    register, entity, rdf = makerdf(cf)
    # import pdb; pdb.set_trace()
    if register == '0.0':
        if not cf00.has_key(entity):
            cf00[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))
    elif register == '4.1':
        if not cf41.has_key(entity):
            cf41[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))
    elif register == '4.2':
        if not cf42.has_key(entity):
            cf42[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))
    elif register == '4.5':
        if not cf45.has_key(entity):
            cf45[entity] = rdf
        else:
            raise ValueError('repeat key {}'.format(entity))
    elif register == '4.10':
        if not cf410.has_key(entity):
            cf410[entity] = rdf
        else:
            raise ValueError('repeat key {}'.format(entity))


## output files

for f in glob.glob('ttl/*.ttl'):
    os.remove(f)

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

with open('ttl/container.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('ldp:Container a owl:Class ;\n'
                  '\trdfs:label "LDP Container"@en ;\n'
                  '\treg:notation "ldp-container" ;\n'
                  '\tldp:membershipPredicate rdfs:member .\n')

with open('ttl/def.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/def> a reg:Register ;\n')
    fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 schemata" ;\n')
    fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol I.2."@en ;\n')
    fhandle.write('\t.\n')

# with open('ttl/defgrib.ttl', 'w') as fhandle:
#     fhandle.write(ttlhead)
#     fhandle.write('<http://codes.wmo.int/def/grib> a reg:Register ;\n')
#     fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 FM 92 GRIB schemata" ;\n')
#     fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 FM 92 GRIB - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol I.2 FM 92 GRIB."@en ;\n')
#     fhandle.write('\t.\n')

with open('ttl/defgribc.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/def/gribcore> a reg:Register, owl:Ontology, ldp:Container ;\n')
    fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 FM 92 GRIB (edition independent) schemata" ;\n')
    fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 FM 92 GRIB (edition independent)  - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol I.2 FM 92 GRIB (edition independent)."@en ;\n')
    #fhandle.write('\treg:inverseMembershipPredicate rdfs:isDefinedBy ;\n')
    fhandle.write('\trdfs:member <http://codes.wmo.int/def/gribcore/Edition>, <http://codes.wmo.int/def/gribcore/edition> ;\n')
    fhandle.write('\t.\n')
    fhandle.write('''
<http://codes.wmo.int/def/gribcore/Edition>
    a owl:Class ;
    rdfs:label "GRIB Edition Number"@en ;
    rdfs:subClassOf skos:Concept ;
    skos:notation "editionNumber" ;
    .

<http://codes.wmo.int/def/gribcore/edition>
    a owl:ObjectProperty ;
    rdfs:label "edition number"@en ;
    rdfs:comment "Object property describing the GRIB edition number valid for an entity'."@en ;
    rdfs:range gribs:Edition ;
    .
    
''')

with open('ttl/defgribe2.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/def/grib2> a reg:Register, owl:Ontology, ldp:Container ;\n')
    fhandle.write('rdfs:label "WMO No. 306 Vol I.2 FM 92 GRIB (edition2) schemata" ;\n')
    fhandle.write('\tdc:description "Schemata required to support WMO No. 306 Vol I.2 FM 92 GRIB (edition2)  - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 Vol I.2 FM 92 GRIB (edition2)."@en ;\n')
#    fhandle.write('\treg:inverseMembershipPredicate rdfs:isDefinedBy ;\n')
    fhandle.write('\trdfs:member <http://codes.wmo.int/def/grib2/Discipline>, '
                  '<http://codes.wmo.int/def/grib2/Category>, '
                  '<http://codes.wmo.int/def/grib2/Parameter>, '
                  '<http://codes.wmo.int/def/grib2/discipline>, '
                  '<http://codes.wmo.int/def/grib2/category>, '
                  '<http://codes.wmo.int/def/grib2/datacode> ;\n')
    fhandle.write('\t.\n')
    fhandle.write('''
<http://codes.wmo.int/def/grib2/Discipline>
    a owl:Class ;
    rdfs:label "Product discipline (Class)"@en ;
    dct:description "Product discipline within which a physical property may be categorised as defined in WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) code-table 0.0 'Discipline of processed data'."@en ;
    rdfs:subClassOf skos:Concept ;
    skos:notation "discipline" ;
    .

<http://codes.wmo.int/def/grib2/Category>
    a owl:Class ;
    rdfs:label "Parameter category (Class)"@en ;
    dct:description "Parameter category within which a physical property may be categorised as defined in WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) code-table 4.1 'Parameter category'."@en ;
    rdfs:subClassOf skos:Concept ;
    skos:notation "parameterCategory" ;
    .

<http://codes.wmo.int/def/grib2/Parameter>
    a owl:Class ;
    rdfs:label "Parameter(Class)"@en ;
    dct:description "Physical property as defined in WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) code-table 4.2 'Parameter number'."@en ;
    rdfs:subClassOf skos:Concept ;
    skos:notation "parameterNumber" ;
    .

<http://codes.wmo.int/def/grib2/discipline> 
    a owl:ObjectProperty ;
    rdfs:label "discipline (property)"@en ;
    rdfs:comment "Object property describing the relationship between a physical property (e.g. QUDT QuantityKind) and the product discipline to which the physical property relates as defined in WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) code-table 0.0 'Discipline of processed data'."@en ;
    rdfs:range grib2s:Discipline ;
    rdfs:domain grib2s:Category, grib2s:Parameter ;
    .

<http://codes.wmo.int/def/grib2/category> 
    a owl:ObjectProperty ;
    rdfs:label "category (property)"@en ;
    rdfs:comment "Object property describing the relationship between a physical property (e.g. QUDT QuantityKind) and the  parameter category to which the physical property relates as defined in WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) code-table 4.1 'Parameter category'."@en ;
    rdfs:range grib2s:Category ;
    rdfs:domain grib2s:Parameter ;
    .

<http://codes.wmo.int/def/grib2/datacode> 
    a owl:ObjectProperty ;
    rdfs:label "parameter data code table"@en ;
    rdfs:comment "Object property describing the relationship between the encoded data values of a message and the code table which these data values reference."@en ;
    rdfs:range skos:Collection ;
    rdfs:domain grib2s:Parameter ;
    .



''')


with open('ttl/gribc.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/gribcore> a reg:Register ;\n')
    fhandle.write('\tdc:description "WMO No. 306 Vol I.2 FM 92 GRIB (edition 2)"@en ;\n')
    fhandle.write('\trdfs:label "GRIB all editions"@en.\n')

with open('ttl/grib1.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib1> a reg:Register ;\n')
    fhandle.write('\tdc:description "WMO No. 306 Vol I.2 FM 92 GRIB"@en ;\n')
    fhandle.write('\trdfs:label "GRIB edition1"@en.\n')


with open('ttl/grib2.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2> a reg:Register ;\n')
    fhandle.write('\tdc:description "WMO No. 306 Vol I.2 FM 92 GRIB (edition 2)"@en ;\n')
    fhandle.write('\trdfs:label "GRIB edition2"@en.\n')

with open('ttl/grib2cflag.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag> a reg:Register ;\n')
    fhandle.write('\tdc:description "WMO No. 306 Vol I.2 FM 92 GRIB (edition 2) Codes and Flags"@en ;\n')
    fhandle.write('\trdfs:label "GRIB2 codes and flags"@en.\n')


with open('ttl/gribedition.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/gribcore/edition> a skos:Collection ;\n')
    fhandle.write('\tdc:description  "WMO published editions of the GRIB specification"@en ;\n')
    fhandle.write('\trdfs:label "GRIB editions"@en ;\n')
    fhandle.write('\tskos:prefLabel "FM 92 GRIB editions"@en ;\n')
    fhandle.write('\tskos:member <http://codes.wmo.int/gribcore/edition/1> ;\n')
    fhandle.write('\tskos:member <http://codes.wmo.int/gribcore/edition/2> ;\n\t.\n\n')
    fhandle.write('<http://codes.wmo.int/gribcore/edition/1> a skos:Concept ;\n')
    fhandle.write('\trdfs:label "FM 92 GRIB edition 1"@en;\n')
    fhandle.write('\tskos:notation 1 .\n\n')
    fhandle.write('<http://codes.wmo.int/gribcore/edition/2> a skos:Concept ;\n')
    fhandle.write('\trdfs:label "FM 92 GRIB edition 2"@en;\n')
    fhandle.write('\tskos:notation 2 .\n')

with open('ttl/grib2disc.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag/0.0> a skos:Collection ;\n')
    fhandle.write('\tdc:description  "Discipline of processed data in the GRIB message, number of GRIB master table"@en ;\n')
    fhandle.write('\trdfs:label "Discipline"@en ;\n')
    fhandle.write('\tskos:prefLabel "Discipline"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf00.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems = mems.rstrip(', ')
    mems += ' .\n\n'
    fhandle.write(mems)
    fhandle.write(elems)

with open('ttl/grib2category.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag/4.1> a skos:Collection ;\n')
    fhandle.write('\tdc:description  "Parameter category by product discipline"@en ;\n')
    fhandle.write('\trdfs:label "Parameter category"@en ;\n')
    fhandle.write('\tskos:prefLabel "Parameter category"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf41.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems = mems.rstrip(', ')
    mems += ' .\n\n'
    fhandle.write(mems)
    fhandle.write(elems)

with open('ttl/grib2parameter.ttl', 'w') as fhandle:
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag/4.2> a skos:Collection ;\n')
    fhandle.write('\tdc:description  "Parameter number by product discipline and parameter category"@en ;\n')
    fhandle.write('\trdfs:label "Parameter number"@en ;\n')
    fhandle.write('\tskos:prefLabel "Parameter number"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf42.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems = mems.rstrip(', ')
    mems += ' .\n\n'
    fhandle.write(mems)
    fhandle.write(elems)

with open('ttl/grib2surftype.ttl', 'w') as fhandle: 
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag/4.5> a skos:Collection ;\n')
    fhandle.write('\tdc:description "Code-table 4.5 - Fixed surface types and units."@en ;\n')
    fhandle.write('\trdfs:label "Fixed surface types and units "@en ;\n')
    fhandle.write('\tskos:prefLabel "Fixed surface types and units "@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf45.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems = mems.rstrip(', ')
    mems += ' .\n\n'
    fhandle.write(mems)
    fhandle.write(elems)


with open('ttl/grib2statprocess.ttl', 'w') as fhandle: 
    fhandle.write(ttlhead)
    fhandle.write('<http://codes.wmo.int/grib2/codeflag/4.10> a skos:Collection ;\n')
    fhandle.write('\tdc:description "Code-table 4.10 - Type of statistical processing. "@en ;\n')
    fhandle.write('\trdfs:label "Type of statistical processing"@en ;\n')
    fhandle.write('\tskos:prefLabel "Type of statistical processing"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf410.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems = mems.rstrip(', ')
    mems += ' .\n\n'
    fhandle.write(mems)
    fhandle.write(elems)
