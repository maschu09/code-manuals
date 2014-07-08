import os
import re

import common
import cleanttl
from ttlhead import ttlhead

INPUTS = [('000', 'Dimensionless', '1', '1', '1', ' '),
          ('001', 'metre', 'm', 'm', 'M', ' '),
          ('002', 'kilogram', 'kg', 'kg', 'KG', ' '),
          ('003', 'second', 's', 's', 'S', ' '),
          ('004', 'ampere', 'A', 'A', 'A', ' '),
          ('005', 'kelvin', 'K', 'K', 'K', ' '),
          ('006', 'mole', 'mol', 'mol', 'MOL', ' '),
          ('007', 'candela', 'cd', 'cd', 'CD', ' '),
          ('021', 'radian', 'rad', 'rad', 'RAD', ' '),
          ('022', 'steradian', 'sr', 'sr', 'SR', ' '),
          ('030', 'hertz', 'Hz', 'Hz', 'HZ', 's-^1'),
          ('031', 'newton', 'N', 'N', 'N', 'kg m s^-2'),
          ('032', 'pascal', 'Pa', 'Pa', 'PAL', 'kg m^-1 s^-2'),
          ('033', 'joule', 'J', 'J', 'J', 'kg m^2 s^-2'),
          ('034', 'watt', 'W', 'W', 'W', 'kg m^2 s^-3'),
          ('035', 'coulomb', 'C', 'C', 'C', 'A s'),
          ('036', 'volt', 'V', 'V', 'V', 'kg m^2 s^-3 A^-1'),
          ('037', 'farad', 'F', 'F', 'F', 'kg^-1 m^-2 s^4 A^2'),
          ('038', 'ohm', '\u2126', 'Ohm', 'OHM', 'kg m^2 s^-3 A^-2'),
          ('039', 'siemens', 'S', 'S', 'SIE', 'kg^-1 m^-2 s^3 A^2'),
          ('040', 'weber', 'Wb', 'Wb', 'WB', 'kg m^2 s^-2 A^-1'),
          ('041', 'tesla', 'T', 'T', 'T', 'kg s^-2 A^-1'),
          ('042', 'henry', 'H', 'H', 'H', 'kg m^2 s^-2 A^-2'),
          ('060', 'degree Celsius', '\u02DA C', 'Cel', 'CEL', 'K+273.15'),
          ('070', 'lumen', 'lm', 'lm', 'LM', 'cd sr'),
          ('071', 'lux', 'lx', 'lx', 'LX', 'cd sr m^-2'),
          ('080', 'becquerel', 'Bq', 'Bq', 'BQ', 's^-1'),
          ('081', 'gray', 'Gy', 'Gy', 'GY', 'm^2 s^-2'),
          ('082', 'sievert', 'Sv', 'Sv', 'SV', 'm^2 s^-2'),
          ('no', '(yotta)', '(Y)', '(Y)', '(Y)', ' '),
          ('no', '(zetta)', '(Z)', '(Z)', '(Z)', ' '),
          ('no', 'exa', 'E', 'E', 'E', ' '),
          ('no', 'peta', 'P', 'P', 'PE', ' '),
          ('no', 'tera', 'T', 'T', 'T', ' '),
          ('no', 'giga', 'G', 'G', 'G', ' '),
          ('no', 'mega', 'M', 'M', 'MA', ' '),
          ('no', 'kilo', 'k', 'k', 'K', ' '),
          ('no', 'hecto', 'h', 'h', 'H', ' '),
          ('no', 'deca', 'da', 'da', 'D', ' '),
          ('no', 'deci', 'd', 'd', 'D', ' '),
          ('no', 'centi', 'c', 'c', 'C', ' '),
          ('no', 'milli', 'm', 'm', 'M', ' '),
          ('no', 'micro', '\u00B5', 'u', 'U', ' '),
          ('no', 'nano', 'n', 'n', 'N', ' '),
          ('no', 'pico', 'p', 'p', 'P', ' '),
          ('no', 'femto', 'f', 'f', 'F', ' '),
          ('no', 'atto', 'a', 'a', 'A', ' '),
          ('no', '(zepto)', '(z)', '(z)', ' ', ' '),
          ('no', '(yocto)', '(y)', '(y)', ' ', ' '),
          ('110', 'degree (angle)', '\u02DA',  'deg', 'DEG', ' '),
          ('111', 'minute (angle)', '\'', '\'', 'MNT', ' '),
          ('112', 'second (angle)', "''", "''", 'SEC', ' '),
          ('120', 'litre', 'l', 'l', 'L', ' '),
          ('130', 'minute (time)', 'min', 'min', 'MIN', ' '),
          ('131', 'hour', 'h', 'h', 'HR', ' '),
          ('132', 'day', 'd', 'd', 'D', ' '),
          ('150', 'tonne', 't', 't', 'TNE', ' '),
          ('160', 'electron volt', 'eV', 'eV', 'EV', ' '),
          ('161', 'atomic mass unit', 'u', 'u', 'U', ' '),
          ('170', 'astronomic unit', 'AU', 'AU', 'ASU', ' '),
          ('171', 'parsec', 'pc', 'pc', 'PRS', ' '),
          ('200', 'nautical mile', ' ', ' ', ' ', ' '),
          ('201', 'knot', 'kt', 'kt', 'KT', ' '),
          ('210', 'decibel (6)', 'dB', 'dB', 'DB', ' '),
          ('220', 'hectare', 'ha', 'ha', 'HAR', ' '),
          ('230', 'week', ' ', ' ', ' ', ' '),
          ('231', 'year', 'a', 'a', 'A', ' '),
          ('300', 'per cent', '%', '%', 'PERCENT', ' '),
          ('301', 'parts per thousand', '\u2030', '0/00', 'PERTHOU', ' '),
          ('310', 'eighths of cloud', 'okta', 'okta', 'OKTA', ' '),
          ('320', 'degrees true', '\u02DA', 'deg', 'DEG', ' '),
          ('321', 'degrees per second', 'degree/s', 'deg/s', 'DEG/S', ' '),
          ('350', 'degrees Celsius (8)', '\u02DA C', 'C', 'C', ' '),
          ('351', 'degrees Celsius per metre', '\u02DA C/m', 'C/m', 'C/M', ' '),
          ('352', 'degrees Celsius per 100 metres', '\u02DA C/100 m', 'C/100 m', 'C/100 M', ' '),
          ('360', 'Dobson Unit (9)', 'DU', 'DU', 'DU'),
          ('430', 'month', 'mon', 'mon', 'MON'),
          ('441', 'per second (same as hertz)', 's^-1', '/s', '/S'),
          ('442', 'per second squared', 's^-2', 's-2'),
          ('501', 'knots per 1000 metres', 'kt/1000 m', 'kt/km', 'KT/KM'),
          ('510', 'foot', 'ft', 'ft', 'FT'),
          ('520', 'decipascals per second (microbar per second)', 'dPa s^-1', 'dPa/s', 'DPAL/S'),
          ('521', 'centibars per second', 'cb s^-1', 'cb/s', 'CB/S'),
          ('522', 'centibars per 12 hours', 'cb/12 h', 'cb/12 h', 'CB/12 HR'),
          ('523', 'dekapascal', 'daPa', 'daPa', 'DAPAL'),
          ('530', 'hectopascal', 'hPa', 'hPa', 'HPAL'),
          ('531', 'hectopascals per second', 'hPa s^-1', 'hPa/s', 'HPAL/S'),
          ('532', 'hectopascals per hour', 'hPa h^-1', 'hPa/h', 'HPAL/HR'),
          ('533', 'hectopascals per 3 hours', 'hPa/3 h', 'hPa/3 h', 'HPAL/3 HR'),
          ('535', 'nanobar = hPa 10^-6', 'nbar', 'nbar', 'NBAR'),
          ('620', 'grams per kilogram', 'g kg^-1', 'g/kg', 'G/KG'),
          ('621', 'grams per kilogram per second', 'g kg^-1 s^-1', 'g kg-1 s-1'),
          ('622', 'kilograms per kilogram', 'kg kg^-1', 'kg/kg'),
          ('623', 'kilograms per kilogram per second', 'kg kg^-1 s^-1', 'kg kg-1 s-1'),
          ('624', 'kilograms per square metre', 'kg m^-2', 'kg m-2'),
          ('630', 'acceleration due to gravity', 'g', 'g'),
          ('631', 'geopotential metre', 'gpm', 'gpm'),
          ('710', 'millimetre', 'mm', 'mm', 'MM'),
          ('711', 'millimetres per seconds', 'mm s^-1', 'mm/s', 'MM/S'),
          ('712', 'millimetres per hour', 'mm h^-1', 'mm/h', 'MM/HR'),
          ('713', 'millimetres per the sixth power per cubic metre', 'mm^6 m^-3', 'mm6 m-3'),
          ('715', 'centimetre', 'cm', 'cm', 'CM'),
          ('716', 'centimetres per second', 'cm s^-1', 'cm/s', 'CM/S'),
          ('717', 'centimetres per hour', 'cm h^-1', 'cm/h', 'CM/HR'),
          ('720', 'decimetre', 'dm', 'dm', 'DM'),
          ('731', 'metres per second', 'm s^-1', 'm/s', 'M/S'),
          ('732', 'metres per second per metre', 'm s^-1/m', 'm s-1/m'),
          ('733', 'metres per second per 1000 metres', 'm s^-1/1000 m', 'm s-1/km'),
          ('734', 'square metres', 'm^2', 'm2', 'M2'),
          ('735', 'square metres per second', 'm^2 s^-1', 'm2/s', 'M2/S'),
          ('740', 'kilometre', 'km', 'km', 'KM'),
          ('741', 'kilometres per hour', 'km h^-1', 'km/h', 'KM/HR'),
          ('742', 'kilometres per day', 'km/d', 'km/d', 'KM/D'),
          ('743', 'per metre', 'm^-1', 'm-1', '/M'),
          ('750', 'becquerels per litre', 'Bq l^-1', 'Bq/l', 'BQ/L'),
          ('751', 'becquerels per square metre', 'Bq m^-2', 'Bq m-2', 'BQ/M2'),
          ('752', 'becquerels per cubic metre', 'Bq m^-3', 'Bq m-3', 'BQ/M3'),
          ('753', 'millisievert', 'mSv', 'mSv', 'MSV'),
          ('760', 'metres per second squared', 'm s^-2', 'm s-2'),
          ('761', 'square metres second', 'm^2 s', 'm2 s'),
          ('762', 'square metres per second squared', 'm^2 s^-2', 'm2 s-2'),
          ('763', 'square metres per radian squared', 'm^2 rad^-1 s', 'm2 rad-1 s'),
          ('764', 'square metres per hertz', 'm^2 Hz^-1', 'm2/Hz'),
          ('765', 'cubic metres', 'm^3', 'm3'),
          ('766', 'cubic metres per second', 'm^3 s^-1', 'm3/s'),
          ('767', 'cubic metres per cubic metre', 'm^3 m^-3', 'm3 m-3'),
          ('768', 'metres to the fourth power', 'm^4', 'm4'),
          ('769', 'metres to the two thirds power per second', 'm^2/3 s^-1', 'm2/3 s-1'),
          ('772', 'logarithm per metre', 'log (m^-1)', 'log (m-1)'),
          ('773', 'logarithm per square metre', 'log (m^-2)', 'log (m-2)'),
          ('775', 'kilograms per metre', 'km m^-1', 'kg/m'),
          ('776', 'kilograms per square metre per second', 'kg m^-2 s^-1', 'kg m-2 s-1'),
          ('777', 'kilograms per cubic metre', 'kg m^-3', 'kg m-3'),
          ('778', 'per square kilogram per second', 'kg^-2 s^-1', 'kg-2 s-1'),
          ('779', 'seconds per metre', 's m^-1', 's/m'),
          ('785', 'kelvin metres per second', 'K m s^-1', 'K m s-1'),
          ('786', 'kelvins per metre', 'K m^-1', 'K/m'),
          ('787', 'kelvin square metres per kilogram per second', 'K m^2 kg^-1 s^-1', 'K m2 kg-1 s-1'),
          ('788', 'moles per mole', ' mol mol^-1', 'mol/mol'),
          ('790', 'radians per metre', 'rad m^-1', 'rad/m'),
          ('795', 'newtons per square metre', 'N m^-2', 'N m-2'),
          ('800', 'pascals per second', 'Pa s^-1', 'Pa/s'),
          ('801', 'kilopascal', 'kPa', 'kPa'),
          ('805', 'joules per square metre', 'J m^-2', 'J m-2'),
          ('806', 'joules per kilogram', 'J kg^-1', 'J/kg'),
          ('810', 'watts per metre per steradian', 'W m^-1 sr^-1', 'W m-1 sr-1'),
          ('811', 'watts per square metre', 'W m^-2', 'W m-2'),
          ('812', 'watts per square metre per steradian', 'W m^-2 sr^-1', 'W m-2 sr-1'),
          ('813', 'watts per square metre per steradian centimetre', 'W m^-2 sr^-1 cm', 'W m-2 sr-1 cm'),
          ('814', 'watts per square metre per steradian metre', 'W m^-2 sr^-1 m', 'W m-2 sr-1 m'),
          ('815', 'watts per cubic metre per steradian', 'W m^-3 sr^-1', 'W m-3 sr-1'),
          ('820', 'siemens per metre', 'S m^-1', 'S/m'),
          ('825', 'square degrees', 'degrees^2', 'deg^2'),
          ('830', 'becquerel seconds per cubic metre', 'Bq s m^-3', 'Bq s m-3'),
          ('835', 'decibels per metre', 'dB m^-1', 'dB/m'),
          ('836', 'decibels per degree', 'dB degree^-1', 'dB/deg'),
          ('841', 'pH unit', 'pH unit', 'pH unit'),
          ('842', 'N units', 'N units', 'N units')
          ]



def file_write(members, member_elements):
    if not os.path.exists('ttl/common'):
        common.main()
        # os.mkdir('ttl/common')
        # with open('ttl/common.ttl', 'w') as fhandle:
        #     fhandle.write(ttlhead)
        #     fhandle.write('<common> a reg:Register ;\n')
        #     fhandle.write('\trdfs:label "WMO No. 306 Vol I.2 common concepts" ;\n')
#     fhandle.write('\tdc:description "Register of concepts common across WMO No. 306 Vol I.2 formats"@en ;\n')
        #     fhandle.write('\treg:owner <http://codes.wmo.int/system/organization/wmo> ;\n')
        #     fhandle.write('\tdct:publisher <http://codes.wmo.int/system/organization/wmo> ;\n')
        #     fhandle.write('\treg:manager <http://codes.wmo.int/system/organization/www-dm> ;\n')
        #     fhandle.write('\t.\n')

    with open('ttl/common/bulk_c6.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)

        fhandle.write('<c-6> a skos:Collection ;\n')
        fhandle.write('\trdfs:label       "List of units for TDCFs"@en ;\n')
        fhandle.write('\tdct:description  "WMO No. 306 Vol I.2 Common Code-table C-6 List of units for TDCFs."@en ;\n')
        fhandle.write('\treg:manager      <http://codes.wmo.int/system/organization/www-dm> ;\n')
        fhandle.write('\treg:owner        <http://codes.wmo.int/system/organization/wmo> ;\n')
        fhandle.write('\tskos:member ')
        fhandle.write(', '.join(members))
        fhandle.write('\t.\n\n')
        fhandle.write('\n'.join(member_elements))

uri_pattern = '<c-6/{}>'

slashunit = re.compile('^([-_123 ^a-zA-Z]*)/([a-zA-Z]*)')

def main():
    members = []
    member_elements = []
    urilabel_list = []
    for unit in INPUTS:
        unitmatch = slashunit.match(unit[3])
        if unitmatch:
            if len(unitmatch.groups()) != 2:
                raise ValueError('unit slash parsing failed with unit: {}'.format(unit))
            urilabel = '{} {}-1'.format(unitmatch.group(1), unitmatch.group(2))
        elif unit[3] == '%':
            urilabel = '%25'
        elif unit[0] == 'no':
            urilabel = '{}_pref'.format(unit[3])
        elif unit[3] == ' ' and unit[1]:
            urilabel = unit[1]
        elif unit[3] == 'deg' and unit[1]:
            urilabel = unit[1].replace(' ', '_')
        elif unit[3] == 'C' and unit[0] == '350':
            urilabel = 'degC'
        elif unit[3] == 'deg^2':
            urilabel = 'deg2'
        elif unit[3] == '0/00':
            urilabel = '0.001'
        else:
            urilabel = unit[3]
        urilabel = urilabel.replace(' ', '_')
        if urilabel.startswith('_'):
            urilabel = urilabel.lstrip('_')
        if len(urilabel.split('/')) > 1:
            raise ValueError('{} uri with / not allowed\n{}'.format(urilabel, unit))
        m_elem_str = uri_pattern.format(urilabel)
        members.append(uri_pattern.format(urilabel))
        m_elem_str += ' a skos:Concept, wmocommon:Unit ;\n'
        m_elem_str += '\trdfs:label "{}" ;\n'.format(unit[1])
        m_elem_str += '\tskos:prefLabel "{}" ;\n'.format(unit[1])
        if unit[3] == 'C' and unit[0] == '350':
            m_elem_str += '\tskos:notation "{}" ;\n'.format('degC')
        else:
            m_elem_str += '\tskos:notation "{}" ;\n'.format(unit[3])
        m_elem_str += '\t<http://codes.wmo.int/def/common/wmoAbbreviation> "{}" ;\n'.format(unit[3])
        m_elem_str += '\tskos:altLabel "{}" ;\n'.format(unit[2])
        m_elem_str += '\t<http://codes.wmo.int/def/common/code_figure> "{}" ;\n'.format(unit[0])
        try:
            if unit[4] and unit[4] != ' ':
                m_elem_str += '\t<http://codes.wmo.int/def/common/wmoAbbreviationIA2> "{}" ;\n'.format(unit[4])
            if unit[5] and unit[5] != ' ':
                m_elem_str += '\t<http://codes.wmo.int/def/common/wmoAbbreviationIA5> "{}" ;\n'.format(unit[5])
        except IndexError:
            pass
        m_elem_str += '\t.\n'
        member_elements.append(m_elem_str)
        if urilabel in urilabel_list:
            raise ValueError('{} is already declared\n{}'.format(urilabel, unit))
        else:
            urilabel_list.append(urilabel)
    file_write(members, member_elements)
    

if __name__ == '__main__':
    cleanttl.clean()
    main()
