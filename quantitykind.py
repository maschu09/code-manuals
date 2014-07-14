#
# Note that the content used in this module has been compiled _manually_ by scraping Enrico Fucile's WMO No 306 Vol I.3 code table D-2 document,
# adding in sub-types of qudt:QuantityKind (e.g. qudt:ThermodynamicsQuantityKind) for the Type defintion and, finally, adding in a few things
# that weren't in Enrico's list (geometricHeight, maximumDiameterOfHailstones, pressureTendency, snowDepthWaterEquivalent, totalPrecipitation,
# totalPrecipitationRate, totalSnowDepth, uvIndex, windDirection, windSpeed)
#

import os

import common
import cleanttl
from ttlhead import ttlhead

d2 = {'Meteorological quantity kinds':[
('Air temperature', 'airTemperature', 'qudt:ThermodynamicsQuantityKind',
 'The temperature indicated by a thermometer exposed to the air in a place sheltered from direct solar radiation.', '\u019F')
,
('Atmospheric pressure', 'atmosphericPressure', 'qudt:MechanicsQuantityKind',
'The atmospheric pressure on a given surface is the force per unit area exerted by virtue of the weight of the atmosphere above. The pressure is thus equal to the weight of a vertical column of air above a horizontal projection of the surface, extending to the outer limit of the atmosphere.','ML-1T-2')
,
('Dew-point temperature', 'dewPointTemperature', 'qudt:ThermodynamicsQuantityKind',
'The temperature to which a given air parcel must be cooled at constant pressure and constant water vapour content in order for saturation to occur.','\u019F')
,
('Height of base of cloud', 'heightOfBaseOfCloud', 'qudt:SpaceAndTimeQuantityKind',
'For a given cloud or cloud layer, vertical distance (measured from local ground surface) of the lowest level in the atmosphere at which the air contains a perceptible quantity of cloud particles.','L')
,
('Horizontal visibility','horizontalVisibility', 'qudt:SpaceAndTimeQuantityKind',
'The greatest distance determined in the horizontal plane at the ground surface that prominent objects can be seen and identified by unaided, normal eyes.','L')
,
('Maximum wind gust speed', 'maximumWindGustSpeed', 'qudt:ThermodynamicsQuantityKind',
'Nominal maximum speed of wind during a given period; usually determined as a mean wind speed over a short duration (e.g. 1-minute) within a longer period (e.g. 10-minutes).', 'LT-1')
,
('Sea surface temperature','seaSurfaceTemperature', 'qudt:ThermodynamicsQuantityKind',
'Temperature of the sea water at surface.','\u019F')
,
('Vertical visibility','verticalVisibility', 'qudt:SpaceAndTimeQuantityKind',
'Maximum distance at which an observer can see and identify an object on the same vertical as himself, above or below.','L')
,
('Geometric height','geometricHeight', 'qudt:SpaceAndTimeQuantityKind',
'Vertical distance (Z) of a level, a point or an object considered as a point, measured from mean sea level. (Also known as geometric altitude).','L')
,
('Maximum diameter of hailstones','maximumDiameterOfHailstones', 'qudt:SpaceAndTimeQuantityKind',
'Maximum diameter (size) of hailstone (observed).','L')
,
('Pressure tendency','pressureTendency', 'qudt:MechanicsQuantityKind',
'Rate of change of atmospheric pressure with respect to time.','XXX')
,
('Snow depth water equivelant','snowDepthWaterEquivalent', 'qudt:SpaceAndTimeQuantityKind',
'Depth of lying snow expressed as measure of equivalent depth of water.','L')
,
('Total precipitation','totalPrecipitation', 'qudt:MechanicsQuantityKind',
'Total amount of precipitation measured over a defined period.','ML-2')
,
('Total precipitation rate','totalPrecipitationRate', 'qudt:MechanicsQuantityKind',
'Rate of total precipitation (e.g. combination of convective and large-scale precipitation of all types).','ML-2T-1')
,
('Total snow depth','totalSnowDepth', 'qudt:SpaceAndTimeQuantityKind',
'Depth of lying snow.','L')
,
('UV index','uvIndex', '',
'Global Solar UVI is formulated using the International Commission on Illumination (CIE) reference action spectrum for UV-induced erythema on the human skin (ISO 17166:1999/CIE S 007/E-1998). It is a measure of the UV radiation that is relevant to and defined for a horizontal surface.','dimensionless')
,
('Wind direction','windDirection', 'qudt:SpaceAndTimeQuantityKind',
'Direction from which wind is blowing.','dimensionless')
,
('Wind speed','windSpeed', 'qudt:SpaceAndTimeQuantityKind',
'Ratio of the distance covered by the air to the time taken to cover it. The instantaneous speed corresponds to the case of an infinitely small time interval. The mean speed corresponds to the case of a finite time interval. It is one component of wind velocity, the other being wind direction).','LT-1')
]

,
'Oceanographic quantity kinds':
[('Sea surface temperature','seaSurfaceTemperature', 'qudt:ThermodynamicsQuantityKind',
'Temperature of the sea water at surface.','\u019F')]

,
'Aeronautical quantity kinds':
[
('Aerodrome maximum wind gust speed','aerodromeMaximumWindGustSpeed', 'qudt:SpaceAndTimeQuantityKind',
'Maximum wind speed in the 10 minute period of observation. It is reported only if exceeds the mean speed by 5 m s-1 (10 knots).','LT-1'),
('Aerodrome mean wind direction','aerodromeMeanWindDirection', 'qudt:SpaceAndTimeQuantityKind',
"The mean true direction in degrees from which the wind is blowing over the 10-minute period immediately preceding the observation. When the 10-minute period includes a marked discontinuity in the wind characteristics (1), only data after the discontinuity shall be used for mean wind direction and variations of the wind direction, hence the time interval in these circumstances shall be correspondingly reduced.","dimensionless", "(1) A marked discontinuity occurs when there is an abrupt and sustained change in wind direction of 30\u00B0  or  more,  with  a  wind  speed  of  5  m s-1 (10  KT)  or  more  before  or  after  the change, or a change in wind speed of 5 m s-1 (10 KT) or more, lasting at least two minutes."),
("Aerodrome mean wind speed","aerodromeMeanWindSpeed", 'qudt:SpaceAndTimeQuantityKind',
"The mean speed of the wind over the 10-minute period immediately preceding the observation. When the 10-minute period includes a marked discontinuity in the wind characteristics (1), only data after the discontinuity shall be used for obtaining mean wind speed, hence the time interval in these circumstances shall be correspondingly reduced.","LT-1", "(1) A marked discontinuity occurs when there is an abrupt and sustained change in wind direction of 30\u00B0  or  more,  with  a  wind  speed  of  5  m s-1 (10  KT)  or  more  before  or  after  the change, or a change in wind speed of 5 m s-1 (10 KT) or more, lasting at least two minutes."),
('Aerodrome minimum horizontal visibility',"aerodromeMinimumHorizontalVisibility", 'qudt:SpaceAndTimeQuantityKind',
"The minimum horizontal visibility that is reported when the horizontal visibility is not the same in different directions and when the minimum visibility is different from the prevailing visibility, and less than 1500 metres or less than 50% of the prevailing visibility, and less than 5000 metres.","L"),
("Aerodrome minimum visibility direction","aerodromeMinimumVisibilityDirection", 'qudt:SpaceAndTimeQuantityKind',
"When the minimum horizontal visibility is reported, its general direction in relation to the aerodrome reference point has to be reported and indicated by reference to one of the eight points of the compass. If the minimum visibility is observed in more than one direction, the Dv shall represent the most operationally significant direction.","dimensionless"),
("Aeronautical prevailing horizontal visibility","aeronauticalPrevailingHorizontalVisibility", 'qudt:SpaceAndTimeQuantityKind',
"The greatest visibility value, observed in accordance with the definition of ``visibility'', which is reached within at least half the horizon circle or within at least half of the surface of the aerodrome. These areas could comprise contiguous or non-contiguous sectors.","L"),
("Aeronautical visibility","aeronauticalVisibility", 'qudt:SpaceAndTimeQuantityKind',
"The greater of:(a) The greatest distance at which a black object of suitable dimensions, situated near the ground, can be seen and recognized when observed against a bright background;(b) The greatest distance at which lights in the vicinity of 1000 candelas can be seen and identified against an unlit background.","L"),
("Altimeter setting (QNH)","altimeterSettingQnh", 'qudt:MechanicsQuantityKind',
"Altimeter setting (also known as QNH) is defined as barometric pressure adjusted to sea level. It is a pressure setting used by pilots, air traffic control (ATC), and low frequency weather beacons to refer to the barometric setting which, when set on an aircraft's altimeter, will cause the altimeter to read altitude above mean sea level within a certain defined region.","ML-1T-2"),
("Depth of runway deposit","depthOfRunwayDeposit", 'qudt:SpaceAndTimeQuantityKind',
"Depth of deposit on surface of runway","L"),
("Runway contamination coverage","runwayContaminationCoverage", "",
"Proportion of runway that is contaminated. A runway is considered to be contaminated when more than 25% of the runway surface area(whether in isolated areas or not) within the required length and width being used is covered by the following:(a)  Surface water more than 3 mm deep, or by slush or loose snow equivalent to more than 3 mm of water; (b) Snow which has been compressed into a solid mass which resists further compression and will hold together or break into lumps if picked up (compacted snow); or (c) Ice, including wet ice.","dimensionless"),
("Runway friction coefficient","runwayFrictionCoefficient", "",
"Quantitative assessment of friction coefficient of runway surface.","dimensionless"),
("Runway visual range (RVR)","runwayVisualRangeRvr", 'qudt:SpaceAndTimeQuantityKind',
"The range over which the pilot of an aircraft on the centre line of a runway can see the runway surface markings or the lights delineating the runway or identifying its centre line.","L")]}




def file_write(members, member_elements):
    if not os.path.exists('ttl/common'):
        common.main()
    with open('ttl/common/bulk_quantitykind.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write('<quantity-kind> a skos:Collection ;\n')
        fhandle.write('\trdfs:label       "Code Table D-2: Physical quantity kinds"@en ;\n')
        fhandle.write('\tskos:notation "D-2" ;\n')
        fhandle.write('\tdct:description  "WMO No. 306 Vol I.3 Common Code-table D-2, Physical quantity kinds."@en ;\n')
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
            m_elem_str += ' a qudt:QuantityKind, skos:Concept'
            if len(elem[2])>0:
                m_elem_str += ', {}'.format(elem[2])
            m_elem_str += ' ;\n'
            m_elem_str += '\tskos:notation "{}" ;\n'.format(urilabel)
            m_elem_str += '\trdfs:label "{}" ;\n'.format(elem[0])
            m_elem_str += '\tdct:description "{}" ;\n'.format(elem[3])
            m_elem_str += '\twmocommon:dimensions "{}" ;\n'.format(elem[4])
            m_elem_str += '\twmocommon:discipline "{}" ;\n'.format(key)
            if len(elem)== 6:
                m_elem_str += '\tskos:note "{}" ;\n'.format(elem[5])
            m_elem_str += '\t.\n\n'
            member_elems.append(m_elem_str)
    return members, member_elems

def main():
    m, me = parseq(d2)
    file_write(m, me)

if __name__ == '__main__':
    cleanttl.clean()
    main()
    
