
import re

slashunit = re.compile('^([a-zA-Z]*)/([a-zA-Z]*)')

def unit_of_measure(code):
    unit = code
    if unit == '-':
        unit = 'N_unit'
    elif unit == 'sigma value' or unit == 'Numeric' or unit == 'Proportion':
        unit = '1'
    elif unit == '%':
        unit = 'percent'
    unitmatch = slashunit.match(unit)

    if unitmatch:
        if len(unitmatch.groups()) != 2:
            raise ValueError('unit slash parsing failed with unit: {}'.format(unit))
        unit = '{} {}-1'.format(unitmatch.group(1), unitmatch.group(2))
    unit = unit.replace(' ', '_')
    return unit
