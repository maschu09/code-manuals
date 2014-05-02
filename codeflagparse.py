from collections import namedtuple
from collections import OrderedDict
import re


infile = 'GRIB2_12_0_0/GRIB2_12_0_0_CodeFlag_en.txt'

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

with open(infile, 'r') as grib:
    for line in grib.readlines():
        lines += 1
        parsed = parsegribtxt(line)
        if parsed:
            codeflags.append(parsed)

if len(codeflags) != lines-1:
    raise ValueError('missing lines\n'
                     '{} lines, {} codeflags'.format(lines, len(codeflags)))


pcatptrn = re.compile('^("Product discipline )([0-9]+?)( - Meteorological products")') 

pnumptrn = re.compile('^("Product discipline )([0-9]+?)( - [a-zA-Z ]*, parameter category )([0-9]+?)(: [a-zA-Z ]*")')

def makerdf(code):
    res = (None, None, None)
    if code.Title_en.startswith('"Code table 0.0'):
        c = None
        codeflag = None
        try:
            codeflag = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if codeflag is not None:
            entity = '<http://codes.wmo.int/grib2/codeflag/0.0/{}>'.format(codeflag)
            rdff = ('{e} a skos:Concept ;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, c=codeflag, l=code.MeaningParameterDescription_en))
            res = ('0.0', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.1'):
        matcher = pcatptrn.match(code.SubTitle_en)
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
            rdff = ('{e} a skos:Concept, <http://codes.wmo.int/grib2/schema/parameter/Category> ;\n'
                    '\t<http://codes.wmo.int/grib2/schema/parameter/discipline> <http://test.wmocodes.info/grib2/codeflag/0.0/{d}> ;\n'
                    '\tskos:notation {c} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, d=disc, c=cat, l=code.MeaningParameterDescription_en))
            res = ('4.1', entity, rdff)
    elif code.Title_en.startswith('"Code table 4.2'):
        #import pdb; pdb.set_trace()
        matcher = pnumptrn.match(code.SubTitle_en)
        disc = None
        cat = None
        paramno = None
        if matcher:
            disc = int(matcher.group(2))
            cat = int(matcher.group(4))
        try:
            paramno = int(code.CodeFlag.replace('"', ''))
        except ValueError:
            pass
        if disc is not None and cat is not None and paramno is not None:
            entity = '<http://codes.wmo.int/grib2/codeflag/4.2/{d}-{c}-{pn}>'.format(d=disc, c=cat, pn=paramno)
            rdff = ('{e} a skos:Concept ;\n'
                    '\t<http://codes.wmo.int/grib2/schema/parameter/discipline> <http://test.wmocodes.info/grib2/codeflag/0.0/{d}> ;\n'
                    '\t<http://codes.wmo.int/grib2/schema/parameter/category> <http://test.wmocodes.info/grib2/codeflag/4.1/{c}> ;\n'
                    '\tskos:notation {pn} ;\n'
                    '\trdfs:label {l}@en ;\n'
                    '\tskos:prefLabel {l}@en ;\n'
                    '\tdc:description {l}@en ;\n'
                    '\t.\n\n'.format(e=entity, d=disc, c=cat, pn=paramno, l=code.MeaningParameterDescription_en))
            res = ('4.2', entity, rdff)
    return res


cf00 = OrderedDict()
cf41 = OrderedDict()
cf42 = OrderedDict()

for cf in codeflags:
    register, entity, rdf = makerdf(cf)
    # import pdb; pdb.set_trace()
    if register == '0.0':
        if not cf00.has_key(entity):
            cf00[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))
    if register == '4.1':
        if not cf41.has_key(entity):
            cf41[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))
    if register == '4.2':
        if not cf42.has_key(entity):
            cf42[entity] = rdf
        else:
            raise ValueError('repeat key: {}'.format(entity))

ttlhead = '''@prefix dc: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

'''

with open('grib2disc.ttl', 'w') as disc:
    disc.write(ttlhead)
    disc.write('<http://codes.wmo.int/grib2/codeflag/0.0> a skos:Collection ;\n')
    disc.write('\tdc:description  "Discipline of processed data in the GRIB message, number of GRIB master table"@en ;\n')
    disc.write('\trdfs:label "Discipline"@en ;\n')
    disc.write('\tskos:prefLabel "Discipline"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf00.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems += ' .\n\n'
    disc.write(mems)
    disc.write(elems)

with open('grib2category.ttl', 'w') as disc:
    disc.write(ttlhead)
    disc.write('<http://codes.wmo.int/grib2/codeflag/4.1> a skos:Collection ;\n')
    disc.write('\tdc:description  "Parameter category by product discipline"@en ;\n')
    disc.write('\trdfs:label "Parameter category"@en ;\n')
    disc.write('\tskos:prefLabel "Parameter category"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf41.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems += ' .\n\n'
    disc.write(mems)
    disc.write(elems)

with open('grib2parameter.ttl', 'w') as disc:
    disc.write(ttlhead)
    disc.write('<http://codes.wmo.int/grib2/codeflag/4.2> a skos:Collection ;\n')
    disc.write('\tdc:description  "Parameter number by product discipline and parameter category"@en ;\n')
    disc.write('\trdfs:label "Parameter number"@en ;\n')
    disc.write('\tskos:prefLabel "Parameter number"@en ;\n')
    mems = '\tskos:member '
    elems = '\n'
    for k,v in cf42.iteritems():
        mems += '{}, '.format(k)
        elems += v
    mems += ' .\n\n'
    disc.write(mems)
    disc.write(elems)


