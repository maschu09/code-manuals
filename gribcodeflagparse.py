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

wmo_url = 'http://www.wmo.int/pages/prog/www/WMOCodes/WMO306_vI2/LatestVERSION/GRIB2_13_0_1.zip'
cffile = 'GRIB2_13_0_1/GRIB2_13_0_1_CodeFlag_en.txt'


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

def readfile():
    lines = 0
    codeflags = []

    response = urllib2.urlopen(wmo_url)

    zipfile = ZipFile(StringIO(response.read()))
    for line in zipfile.open(cffile).readlines():
        lines += 1
        parsed = parsegribtxt(line)
        if parsed:
            codeflags.append(parsed)


    if len(codeflags) != lines-1:
        raise ValueError('missing lines\n'
                         '{} lines, {} codeflags'.format(lines, len(codeflags)))
    return codeflags


pcatptrn = re.compile('^("Product discipline )([0-9]+?)( - .*?")') 

pnumptrn = re.compile('^("Product [D|d]iscipline )([0-9]+?)( - .*?, parameter category )([0-9]+?)(: .*?")')


codeptrn = re.compile('^(Code_table_)(4\.[0-9]+?)')

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
            entity = '<0.0/{}>'.format(codeflag)
            rdff = ('{e} a skos:Concept, grib2s:Discipline ;\n'
                    '\twmocommon:edition <http://codes.wmo.int/codeform/grib2>;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdct:description {l}@en ;\n'
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
            entity = '<4.1/{d}-{c}>'.format(d=disc, c=cat)
            rdff = ('{e} a skos:Concept, grib2s:Category ;\n'
                    '\tgrib2s:discipline <http://codes.wmo.int/grib2/codeflag/0.0/{d}> ;\n'
                    '\twmocommon:edition <http://codes.wmo.int/codeform/grib2>;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdct:description {l}@en ;\n'
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
        unit = unit_of_measure(code.UnitComments_en.replace('"',''))
        if matcher:
            disc = int(matcher.group(2))
            cat = int(matcher.group(4))
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if disc is not None and cat is not None and paramno is not None:
            refs = ''
            unitstr = ''
            datacodestr = ''
            # if unit == 'Code_table_4.217':
            #     import pdb; pdb.set_trace()
            if codeptrn.match(unit):
                datacode = codeptrn.match(unit).group(2)
                refs = '\tdct:references <http://codes.wmo.int/grib2/codeflag/{}> \n ;'
                cflag = unit.split('_')[-1]
                datacodestr = refs.format(cflag)
                unit = 'N_unit'
            if unit:
                unitstr = '\twmocommon:unit <http://codes.wmo.int/common/unit/{u}> ;\n'.format(u=unit)
            entity = '<4.2/{d}-{c}-{pn}>'.format(d=disc, c=cat, pn=paramno)
            rdff = ('{e} a skos:Concept, grib2s:Parameter ;\n'
                    '\tgrib2s:discipline <http://codes.wmo.int/grib2/codeflag/0.0/{d}> ;\n'
                    '\tgrib2s:category <http://codes.wmo.int/grib2/codeflag/4.1/{d}-{c}> ;\n'
                    '\twmocommon:edition <http://codes.wmo.int/codeform/grib2>;\n'
                    '\tgrib2s:parameter {pn} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdct:description {l}@en ;\n'
                    '\t<http://metarelate.net/vocabulary/index.html#identifier> <http://codes.wmo.int/def/common/edition> ;\n'
                    '\t<http://metarelate.net/vocabulary/index.html#identifier> grib2s:discipline ;\n'
                    '\t<http://metarelate.net/vocabulary/index.html#identifier> grib2s:category ;\n'
                    '\t<http://metarelate.net/vocabulary/index.html#identifier> grib2s:parameter ;\n'
                    '{u}{dc}'
                    '\t.\n\n'.format(e=entity, d=disc, c=cat, pn=paramno,
                                     l=code.MeaningParameterDescription_en,
                                     u=unitstr, dc = datacodestr))
            if not code.MeaningParameterDescription_en.startswith('"Reserved'):
                res = ('4.2', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.5 '):
        label = code.MeaningParameterDescription_en
        unit = unit_of_measure(code.UnitComments_en.replace('"',''))
        paramno = None
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if paramno is not None:
            unitstr = ''
            if unit:
                unitstr = '\twmocommon:unit <http://codes.wmo.int/common/unit/{u}> ;\n'.format(u=unit)
            entity = '<4.5/{s}>'.format(s=paramno)
            rdff = ('{e} a skos:Concept ;\n'
                    '\twmocommon:edition <http://codes.wmo.int/codeform/grib2>;\n'
                    '\tskos:notation {s} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdct:description {l}@en ;\n'
                    '{u}'
                    '\t.\n\n'.format(e=entity, s=paramno, l=label, u=unitstr))
            if not code.MeaningParameterDescription_en.startswith('"Reserved'):
                res = ('4.5', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.10 '):
        label = code.MeaningParameterDescription_en
        paramno = None
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if paramno is not None:
            entity = '<4.10/{s}>'.format(s=paramno)
            rdff = ('{e} a skos:Concept ;\n'
                    '\twmocommon:edition <http://codes.wmo.int/codeform/grib2>;\n'
                    '\tskos:notation {s} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdct:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, s=paramno, l=label))
            res = ('4.10', entity, rdff)
    return res

def writettl(codeflags):
    cf00 = OrderedDict()
    cf41 = OrderedDict()
    cf42 = OrderedDict()
    cf45 = OrderedDict()
    cf410 = OrderedDict()

    for cf in codeflags:
        register, entity, rdf = makerdf(cf)
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
    #cleanttl.clean()

    #import defcommon
    # with open('ttl/defgrib.ttl', 'w') as fhandle:
    #     fhandle.write(ttlhead)
    #     fhandle.write('<http://codes.wmo.int/def/grib> a reg:Register ;\n')
    #     fhandle.write('\trdfs:label "WMO No. 306 FM 92 GRIB schemata" ;\n')
    #     fhandle.write('\tdct:description "Schemata required to support WMO No. 306 FM 92 GRIB - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 FM 92 GRIB."@en ;\n')
    #     fhandle.write('\t.\n')

    if not os.path.exists('ttl/def'):
        os.mkdir('ttl/def')
    # os.mkdir('ttl/def/grib')

    with open('ttl/def/bulk_gribe2.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<grib2> a reg:Register, owl:Ontology, ldp:Container ;\n')
        fhandle.write('rdfs:label "WMO No. 306 FM 92 GRIB (edition2) schemata" ;\n')
        fhandle.write('\tdct:description "Schemata required to support WMO No. 306 FM 92 GRIB (edition2)  - Manual on Codes; including definitions of structure and domain-specific metadata required to describe terms from WMO No. 306 FM 92 GRIB (edition2)."@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:member <grib2/Discipline>, '
                      '<grib2/Category>, '
                      '<grib2/Parameter>, '
                      '<grib2/discipline>, '
                      '<grib2/category>, '
                      '<grib2/parameter> ;\n')
        fhandle.write('\t.\n')
        fhandle.write('<grib2/Discipline> a owl:Class ; \n'
                      '\trdfs:label "Product discipline (Class)"@en ;\n'
                      '\tdct:description "Product discipline within which a physical property may be categorised as defined in WMO No. 306 FM 92 GRIB (edition 2) code-table 0.0 `Discipline of processed data`."@en ;\n'
                      # '\trdfs:subClassOf skos:Concept ;\n'
                      # '\tskos:notation "discipline" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/Category> a owl:Class ;\n'
                      '\trdfs:label "Parameter category (Class)"@en ;\n'
                      '\tdct:description "Parameter category within which a physical property may be categorised as defined in WMO No. 306 FM 92 GRIB (edition 2) code-table 4.1 `Parameter category`."@en ;\n'
                      # '\trdfs:subClassOf skos:Concept ;\n'
                      # '\tskos:notation "parameterCategory" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/Parameter> a owl:Class ;\n'
                      '\trdfs:label "Parameter(Class)"@en ;\n'
                      '\tdct:description "Physical property as defined in WMO No. 306 FM 92 GRIB (edition 2) code-table 4.2 `Parameter number`."@en ;\n'
                      # '\trdfs:subClassOf skos:Concept ;\n'
                      # '\tskos:notation "parameterNumber" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/discipline> a owl:ObjectProperty ;\n'
                      '\trdfs:label "discipline (property)"@en ;\n'
                      '\trdfs:comment "Object property describing the relationship between a physical property (e.g. QUDT QuantityKind) and the product discipline to which the physical property relates as defined in WMO No. 306 FM 92 GRIB (edition 2) code-table 0.0 `Discipline of processed data`."@en ;\n'
                      '\trdfs:range grib2s:Discipline ;\n'
                      '\trdfs:domain grib2s:Category, grib2s:Parameter, wmocodeform:GRIB-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "discipline" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/category> a owl:ObjectProperty ;\n'
                      '\trdfs:label "category (property)"@en ;\n'
                      '\trdfs:comment "Object property describing the relationship between a physical property (e.g. QUDT QuantityKind) and the  parameter category to which the physical property relates as defined in WMO No. 306 FM 92 GRIB (edition 2) code-table 4.1 `Parameter category`."@en ;\n'
                      '\trdfs:range grib2s:Category ;\n'
                      '\trdfs:domain grib2s:Parameter, wmocodeform:GRIB-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "parameterCategory" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/parameter> a owl:ObjectProperty ;\n'
                      '\trdfs:label "parameter data code table"@en ;\n'
                      '\trdfs:comment "Object property describing the relationship between the encoded data values of a message and the code table which these data values reference."@en ;\n'
                      '\trdfs:range grib2s:Parameter ;\n'
                      #'\trdfs:range skos:Collection ;\n'
                      '\trdfs:domain grib2s:Parameter, wmocodeform:GRIB-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "parameterNumber" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')
        fhandle.write('<grib2/parameterId> a owl:ObjectProperty ;\n'
                      '\trdfs:label "parameter identifier"@en ;\n'
                      '\trdfs:comment "Object property defining the parameter for a GRIB (edition 2) message RDF representation."@en ;\n'
                      '\trdfs:range grib2s:Parameter ;\n'
                      '\trdfs:domain wmocodeform:GRIB-message ;\n'
                      '\trdfs:subClassOf skos:Concept ;\n'
                      '\tskos:notation "grib2_parameter" ;\n'
                      '\trdfs:isDefinedBy <grib2>\n'
                      '\t.\n\n')





    # os.mkdir('ttl/codeform')
    # with open('ttl/codeform.ttl', 'w') as fhandle:
    #     fhandle.write(ttlhead)
    #     fhandle.write('<codeform> a reg:Register ;\n')
    #     fhandle.write('\tdct:description "WMO No. 306 FM 92"@en ;\n')
    #     fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
    #     fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
    #     fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
    #     fhandle.write('\trdfs:label "Code forms"@en.\n')

    # os.mkdir('ttl/grib1')
    # with open('ttl/grib1.ttl', 'w') as fhandle:
    #     fhandle.write(ttlhead)
    #     fhandle.write('<grib1> a reg:Register ;\n')
    #     fhandle.write('\tdct:description "WMO No. 306 FM 92 GRIB (edition 1)"@en ;\n')
    #     fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
    #     fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
    #     fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
    #     fhandle.write('\trdfs:label "GRIB edition1"@en.\n')


    os.mkdir('ttl/grib2')
    with open('ttl/grib2.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<grib2> a reg:Register ;\n')
        fhandle.write('\tdct:description "WMO No. 306 FM 92 GRIB (edition 2)"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:label "GRIB edition 2"@en.\n')

    os.mkdir('ttl/grib2/codeflag')
    with open('ttl/grib2/grib2cflag.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<codeflag> a reg:Register ;\n')
        fhandle.write('\tdct:description "WMO No. 306 FM 92 GRIB (edition 2) Codes and Flags"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\trdfs:label "GRIB2 codes and flags"@en.\n')



    with open('ttl/grib2/codeflag/bulk_disc.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<0.0> a skos:Collection ;\n')
        fhandle.write('\tdct:description  "Discipline of processed data in the GRIB message, number of GRIB master table"@en ;\n')
        fhandle.write('\trdfs:label "Discipline"@en ;\n')
        fhandle.write('\tskos:prefLabel "Discipline"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        mems = '\tskos:member '
        elems = '\n'
        for k,v in cf00.iteritems():
            mems += '{}, '.format(k)
            elems += v
        mems = mems.rstrip(', ')
        mems += ' .\n\n'
        fhandle.write(mems)
        fhandle.write(elems)

    with open('ttl/grib2/codeflag/bulk_category.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<4.1> a skos:Collection ;\n')
        fhandle.write('\tdct:description  "Parameter category by product discipline"@en ;\n')
        fhandle.write('\trdfs:label "Parameter category"@en ;\n')
        fhandle.write('\tskos:prefLabel "Parameter category"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        mems = '\tskos:member '
        elems = '\n'
        for k,v in cf41.iteritems():
            mems += '{}, '.format(k)
            elems += v
        mems = mems.rstrip(', ')
        mems += ' .\n\n'
        fhandle.write(mems)
        fhandle.write(elems)

    with open('ttl/grib2/codeflag/bulk_parameter.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<4.2> a skos:Collection ;\n')
        fhandle.write('\tdct:description  "Parameter number by product discipline and parameter category"@en ;\n')
        fhandle.write('\trdfs:label "Parameter number"@en ;\n')
        fhandle.write('\tskos:prefLabel "Parameter number"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        mems = '\tskos:member '
        elems = '\n'
        for k,v in cf42.iteritems():
            mems += '{}, '.format(k)
            elems += v
        mems = mems.rstrip(', ')
        mems += ' .\n\n'
        fhandle.write(mems)
        fhandle.write(elems)

    with open('ttl/grib2/codeflag/bulk_surftype.ttl', 'w') as fhandle: 
        fhandle.write(ttlhead)
        fhandle.write('<4.5> a skos:Collection ;\n')
        fhandle.write('\tdct:description "Code-table 4.5 - Fixed surface types and units."@en ;\n')
        fhandle.write('\trdfs:label "Fixed surface types and units "@en ;\n')
        fhandle.write('\tskos:prefLabel "Fixed surface types and units "@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        mems = '\tskos:member '
        elems = '\n'
        for k,v in cf45.iteritems():
            mems += '{}, '.format(k)
            elems += v
        mems = mems.rstrip(', ')
        mems += ' .\n\n'
        fhandle.write(mems)
        fhandle.write(elems)


    with open('ttl/grib2/codeflag/bulk_statprocess.ttl', 'w') as fhandle: 
        fhandle.write(ttlhead)
        fhandle.write('<4.10> a skos:Collection ;\n')
        fhandle.write('\tdct:description "Code-table 4.10 - Type of statistical processing. "@en ;\n')
        fhandle.write('\trdfs:label "Type of statistical processing"@en ;\n')
        fhandle.write('\tskos:prefLabel "Type of statistical processing"@en ;\n')
        fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        mems = '\tskos:member '
        elems = '\n'
        for k,v in cf410.iteritems():
            mems += '{}, '.format(k)
            elems += v
        mems = mems.rstrip(', ')
        mems += ' .\n\n'
        fhandle.write(mems)
        fhandle.write(elems)

def main():
    codeflags = readfile()
    writettl(codeflags)

if __name__ == '__main__':
    cleanttl.clean()
    main()
