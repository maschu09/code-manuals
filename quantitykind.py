import os

import cleanttl
from ttlhead import ttlhead

d2 = {'Meteorological quantities':[
('Air temperature', 'airTemperature',
 'The temperature indicated by a thermometer exposed to the air in a place sheltered from direct solar radiation.', '\u019F')
,
('Atmospheric pressure', 'atmosphericPressure',
'The atmospheric pressure on a given surface is the force per unit area exerted by virtue of the weight of the atmosphere above. The pressure is thus equal to the weight of a vertical column of air above a horizontal projection of the surface, extending to the outer limit of the atmosphere.','ML-1T-2')
,
('Dew-point temperature', 'dewPointTemperature',
'The temperature to which a given air parcel must be cooled at constant pressure and constant water vapour content in order for saturation to occur.','\u019F')
,
('Height of base of cloud', 'heightOfBaseOfCloud',
'For a given cloud or cloud layer, vertical distance (measured from local ground surface) of the lowest level in the atmosphere at which the air contains a perceptible quantity of cloud particles.','L')
,
('Horizontal visibility','horizontalVisibility',
'The greatest distance determined in the horizontal plane at the ground surface that prominent objects can be seen and identified by unaided, normal eyes.','L')
,
('Maximum wind gust speed', 'maximumWindGustSpeed',
'Nominal maximum speed of wind during a given period; usually determined as a mean wind speed over a short duration (e.g. 1-minute) within a longer period (e.g. 10-minutes).', 'LT-1')
,
('Sea surface temperature','seaSurfaceTemperature','Temperature of the sea water at surface.','\u019F')
,
('Vertical visibility','verticalVisibility',
'Maximum distance at which an observer can see and identify an object on the same vertical as himself, above or below.','L')
]

,
'Oceanographic quantities':
[('Sea surface temperature','seaSurfaceTemperature','Temperature of the sea water at surface.','\u019F')]

,
'Aeronautical quantities':
[
('Aerodrome maximum wind gust speed','aerodromeMaximumWindGustSpeed','Maximum wind speed in the 10 minute period of observation. It is reported only if exceeds the mean speed by 5 m s-1 (10 knots).','LT-1'),
('Aerodrome mean wind direction	aerodromeMeanWindDirection',"The mean true direction in degrees from which the wind is blowing over the 10-minute period immediately preceding the observation. When the 10-minute period includes a marked discontinuity in the wind characteristics (1), only data after the discontinuity shall be used for mean wind direction and variations of the wind direction, hence the time interval in these circumstances shall be correspondingly reduced.","dimensionless", "(1) A marked discontinuity occurs when there is an abrupt and sustained change in wind direction of 30\u00B0  or  more,  with  a  wind  speed  of  5  m s-1 (10  KT)  or  more  before  or  after  the change, or a change in wind speed of 5 m s-1 (10 KT) or more, lasting at least two minutes."),
("Aerodrome mean wind speed","aerodromeMeanWindSpeed","The mean speed of the wind over the 10-minute period immediately preceding the observation. When the 10-minute period includes a marked discontinuity in the wind characteristics (1), only data after the discontinuity shall be used for obtaining mean wind speed, hence the time interval in these circumstances shall be correspondingly reduced.","LT-1", "(1) A marked discontinuity occurs when there is an abrupt and sustained change in wind direction of 30\u00B0  or  more,  with  a  wind  speed  of  5  m s-1 (10  KT)  or  more  before  or  after  the change, or a change in wind speed of 5 m s-1 (10 KT) or more, lasting at least two minutes."),
('Aerodrome minimum horizontal visibility',"aerodromeMinimumHorizontalVisibility","The minimum horizontal visibility that is reported when the horizontal visibility is not the same in different directions and when the minimum visibility is different from the prevailing visibility, and less than 1500 metres or less than 50% of the prevailing visibility, and less than 5000 metres.","L"),
("Aerodrome minimum visibility direction","aerodromeMinimumVisibilityDirection","When the minimum horizontal visibility is reported, its general direction in relation to the aerodrome reference point has to be reported and indicated by reference to one of the eight points of the compass. If the minimum visibility is observed in more than one direction, the Dv shall represent the most operationally significant direction.","dimensionless"),
("Aeronautical prevailing horizontal visibility","aeronauticalPrevailingHorizontalVisibility","The greatest visibility value, observed in accordance with the definition of ``visibility'', which is reached within at least half the horizon circle or within at least half of the surface of the aerodrome. These areas could comprise contiguous or non-contiguous sectors.","L"),
("Aeronautical visibility","aeronauticalVisibility","The greater of:(a) The greatest distance at which a black object of suitable dimensions, situated near the ground, can be seen and recognized when observed against a bright background;(b) The greatest distance at which lights in the vicinity of 1000 candelas can be seen and identified against an unlit background.","L"),
("Altimeter setting (QNH)","altimeterSettingQnh",
"Altimeter setting (also known as QNH) is defined as barometric pressure adjusted to sea level. It is a pressure setting used by pilots, air traffic control (ATC), and low frequency weather beacons to refer to the barometric setting which, when set on an aircraft's altimeter, will cause the altimeter to read altitude above mean sea level within a certain defined region.","ML-1T-2"),
("Depth of runway deposit","depthOfRunwayDeposit","Depth of deposit on surface of runway","L"),
("Runway contamination coverage","runwayContaminationCoverage","Proportion of runway that is contaminated. A runway is considered to be contaminated when more than 25% of the runway surface area(whether in isolated areas or not) within the required length and width being used is covered by the following:(a)  Surface water more than 3 mm deep, or by slush or loose snow equivalent to more than 3 mm of water; (b) Snow which has been compressed into a solid mass which resists further compression and will hold together or break into lumps if picked up (compacted snow); or (c) Ice, including wet ice.","dimensionless"),
("Runway friction coefficient","runwayFrictionCoefficient","Quantitative assessment of friction coefficient of runway surface.","dimensionless"),
("Runway visual range (RVR)","runwayVisualRangeRvr",
"The range over which the pilot of an aircraft on the centre line of a runway can see the runway surface markings or the lights delineating the runway or identifying its centre line.","L")]}




def file_write(members, member_elements):
    if not os.path.exists('ttl/common'):
        os.mkdir('ttl/common')
        with open('ttl/common/bulk_quantitykind.ttl', 'w') as fhandle:
            fhandle.write(ttlhead)
            fhandle.write('<quantity-kind> a skos:Collection ;\n')
            fhandle.write('\trdfs:label       "Physical quantities"@en ;\n')
            fhandle.write('\tdct:description  "WMO No. 306 Vol I.2 Common Code-table D-2, Physical quantities."@en ;\n')
            fhandle.write('\treg:manager      <http://codes.wmo.int/system/organization/www-dm> ;\n')
            fhandle.write('\treg:owner        <http://codes.wmo.int/system/organization/wmo> ;\n')
            fhandle.write('\tskos:member ')
            fhandle.write(', '.join(members))
            fhandle.write('\t.\n\n')
            fhandle.write('\n'.join(member_elements))

def parseq(indict):
    members = []
    member_elems = []
    urilabel_list = []
    for key in indict.keys():
        for elem in indict[key]:
            urilabel = elem[1]
            if urilabel in urilabel_list:
                raise ValueError('{} already in use'.format(urilabel))
            uri = '<quantity-kind/{}>'.format(urilabel)
            members.append(uri)
            m_elem_str = uri
            m_elem_str += ' a owl:Class ;\n'
            m_elem_str += '\trdfs:label "{}" ;\n'.format(elem[0])
            m_elem_str += '\tdct:description "{}" ;\n'.format(elem[2])
            m_elem_str += '\trdfs:subClassOf skos:Concept ;\n'
            m_elem_str += '\twmocommon:dimensions "{}" ;\n'.format(elem[3])
            if len(elem)== 5:
                m_elem_str += '\tskos:note "{}" ;\n'.format(elem[4])
            member_elems.append(m_elem_str)
    return members, member_elems

def main():
    m, me = parseq(d2)
    file_write(m, me)

if __name__ == '__main__':
    cleanttl.clean()
    main()
    
