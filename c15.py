import os

from ttlhead import ttlhead
import cleanttl
import common

def make_regs():
    if not os.path.exists('ttl/common'):
        common.main()
    if not os.path.exists('ttl/common/c-15'):
        os.mkdir('ttl/common/c-15')
    if not os.path.exists('ttl/common/c-15/ae'):
        os.mkdir('ttl/common/c-15/ae')
    if not os.path.exists('ttl/common/c-15/me'):
        os.mkdir('ttl/common/c-15/me')
    if not os.path.exists('ttl/common/c-15/oc'):
        os.mkdir('ttl/common/c-15/oc')
        with open('ttl/common/deprec_c-15.ttl', 'w') as fhandle:
            fhandle.write(ttlhead)
            fhandle.write("""<c-15> a reg:Register , ldp:Container ;
    rdfs:label "Physical quantities"@en ;
    dct:description "WMO No. 306 Vol I.2 Common Code-table C-15 'Physical quantities'."@en ;
    reg:owner <http://codes.wmo.int/system/organization/wmo> ;
    reg:manager <http://codes.wmo.int/system/organization/www-dm> ;
    .
    """)
    with open('ttl/common/c-15/deprec_ae.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write("""<ae> a reg:Register , ldp:Container ;
    rdfs:label "Physical quantities - aeronautical meteorology discipline"@en ;
    dct:description "WMO No. 306 Vol I.2 Common Code-table C-15 'Physical quantities - aeronautical meteorology discipline'."@en ;
    reg:owner <http://codes.wmo.int/system/organization/wmo> ;
    reg:manager <http://codes.wmo.int/system/organization/www-dm> ;
    .
""")
    with open('ttl/common/c-15/deprec_me.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write("""<me> a reg:Register , ldp:Container ;
    rdfs:label "Physical quantities - meteorology discipline"@en ;
    dct:description "WMO No. 306 Vol I.2 Common Code-table C-15 'Physical quantities - meteorology discipline'."@en ;
    reg:owner <http://codes.wmo.int/system/organization/wmo> ;
    reg:manager <http://codes.wmo.int/system/organization/www-dm> ;
    .
""")
    with open('ttl/common/c-15/deprec_oc.ttl', 'w') as fhandle:
        fhandle.write(ttlhead)
        fhandle.write("""<oc> a reg:Register , ldp:Container ;
    rdfs:label "Physical quantities - oceanography discipline"@en ;
    dct:description "WMO No. 306 Vol I.2 Common Code-table C-15 'Physical quantities - oceanography discipline'."@en ;
    reg:owner <http://codes.wmo.int/system/organization/wmo> ;
    reg:manager <http://codes.wmo.int/system/organization/www-dm> ;
    .
""")


    

declared_qk = ['aerodromeMaximumWindGustSpeed', 'aerodromeMeanWindDirection', 'aerodromeMeanWindSpeed', 'aerodromeMinimumHorizontalVisibility', 'aerodromeMinimumVisibilityDirection', 'aeronauticalPrevailingHorizontalVisibility', 'aeronauticalVisibility', 'altimeterSettingQnh', 'depthOfRunwayDeposit', 'runwayContaminationCoverage', 'runwayFrictionCoefficient', 'runwayVisualRangeRvr', 'seaSurfaceTemperature', 'airTemperature', 'atmosphericPressure', 'dewPointTemperature', 'heightOfBaseOfCloud', 'horizontalVisibility', 'maximumWindGustSpeed', 'seaSurfaceTemperature', 'verticalVisibility', 'geometricHeight', 'maximumDiameterOfHailstones', 'pressureTendency', 'snowDepthWaterEquivalent', 'totalPrecipitation', 'totalPrecipitationRate', 'totalSnowDepth', 'uvIndex', 'windDirection', 'windSpeed']


def make_forward(fname, original, target):
    with open(fname, 'w') as fhandle:
        if target not in declared_qk:
            raise ValueError('{} not a declared quanity kind'.format(target))
        fhandle.write(ttlhead)
        fhandle.write('<{}> a reg:NamespaceForward , reg:Delegated \n;'.format(original))
        fhandle.write('\treg:delegationTarget <http://codes.wmo.int/common/quantity-kind/{}> ;\n'.format(target))
        fhandle.write('\treg:forwardingCode "301" \n;')
        fhandle.write('\trdfs:label "{}" ;\n'.format(target))
        fhandle.write('\t.\n')

def make_forwards():
    # note: the resources in the list below that are commented out relate to nominal value types that shouldn't be in 
    # <common/quantity-kind> hence there is no redirect.
    redirects = {'ae':[
    #                   ('cloudDistributionForAviation',''),
    #                   ('significantWeather',''),
    #                   ('significantRecentWeatherPhenomenon',''),
                       ('prevailingHorizontalVisibility','aeronauticalPrevailingHorizontalVisibility'),
                       ('runwayVisualRangeRvr','runwayVisualRangeRvr'),
                       ('verticalVisibility','verticalVisibility'),
                       ('minimumHorizontalVisibility','aeronauticalVisibility'),
                       ('depthOfRunwayDeposit','depthOfRunwayDeposit'),
                       ('runwayFrictionCoefficient','runwayFrictionCoefficient'),
                       ('runwayContamination','runwayContaminationCoverage'),
    #                   ('runwayDeposits','')
                       ],
                 'me':[('dewPointTemperature','dewPointTemperature'),
                       ('airTemperature','airTemperature'),
                       ('uvIndex','uvIndex'),
                       ('horizontalVisibility','horizontalVisibility'),
                       ('maximumDiameterOfHailstones','maximumDiameterOfHailstones'),
                       ('windSpeed','windSpeed'),
                       ('windDirection','windDirection'),
                       ('maximumWindGustSpeed','maximumWindGustSpeed'),
                       ('totalPrecipitationRate','totalPrecipitationRate'),
                       ('totalPrecipitation','totalPrecipitation'),
                       ('snowDepthWaterEquivalent','snowDepthWaterEquivalent'),
                       ('totalSnowDepth','totalSnowDepth'),
                       ('pressureTendency','pressureTendency'),
                       ('pressureReducedToMeanSeaLevel','atmosphericPressure'),
                       ('geometricHeight','geometricHeight'),
                       ('altimeterSettingQnh','altimeterSettingQnh'),
                       ('heightOfBaseOfCloud','heightOfBaseOfCloud'),
    #                   ('cloudType',''),
    #                   ('meteorologicalFeature',''),
    #                   ('characteristicOfPressureTendency','')
                       ],
                 'oc':[('seaSurfaceTemperature','seaSurfaceTemperature'),
    #                   ('seaState','')
                       ]}
    for key, vals in redirects.iteritems():
        for redirect in vals:
            fname = 'ttl/common/c-15/{}/deprec_{}.ttl'.format(key, redirect[0])
            make_forward(fname, redirect[0], redirect[1])

def main():
    make_regs()
    make_forwards()

if __name__ == '__main__':
    cleanttl.clean()
    main()
