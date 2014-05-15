import argparse
import copy
import glob
import numpy as np
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("passcode")
args = parser.parse_args()

pss = args.passcode
#base = '54.229.172.81'
#base = '54.229.147.46'
base = 'test.wmocodes.info'

#authcall = ['curl', '-i' ,'-b', 'cookie-jar', '-c', 'cookie-jar', '--data', 'userid=https://profiles.google.com/100578379482821123729&password={}'.format(pss), 'http://{}/system/security/apilogin']

authcall = ['curl', '-i' ,'-b', 'cookie-jar', '-c', 'cookie-jar', '--data', 'userid=https://profiles.google.com/100578379482821123729&password={}'.format(pss), 'http://{}/system/security/apilogin'.format(base)]

subprocess.check_call(authcall)

fpath = os.path.join(os.getcwd(), 'ttl')

call = ['curl', '-i', '-b', 'cookie-jar', '-H', 'Content-type:text/turtle',
        "-X", "POST", "--data"]


concall = copy.copy(call)
concall.append('@{}/container.ttl'.format(fpath))
concall.append("http://{}/system/bulkCollectionTypes?status=Stable".format(base))
print ' '.join(concall)
subprocess.check_call(concall)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/def.ttl'.format(fpath))
um_call.append("http://{}/?status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'


# c4_call = copy.copy(call)
# c4_call.append('@{}/defgrib.ttl'.format(fpath))
# c4_call.append("http://{}/def?status=Experimental".format(base))
# print ' '.join(c4_call)
# subprocess.check_call(c4_call)
# print '\n\n'


fc_call = copy.copy(call)
fc_call.append('@{}/defgribc.ttl'.format(fpath))
#fc_call.append("http://{}/def/grib?batch-managed&status=Experimental".format(base))
fc_call.append("http://{}/def?batch-managed&status=Experimental".format(base))
print ' '.join(fc_call)
subprocess.check_call(fc_call)
print '\n\n'


fc_call = copy.copy(call)
fc_call.append('@{}/defgribe2.ttl'.format(fpath))
#fc_call.append("http://{}/def/grib?batch-managed&status=Experimental".format(base))
fc_call.append("http://{}/def?batch-managed&status=Experimental".format(base))
print ' '.join(fc_call)
subprocess.check_call(fc_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/gribc.ttl'.format(fpath))
um_call.append("http://{}/?status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib1.ttl'.format(fpath))
um_call.append("http://{}/?status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'


um_call = copy.copy(call)
um_call.append('@{}/grib2.ttl'.format(fpath))
um_call.append("http://{}/?status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/gribedition.ttl'.format(fpath))
um_call.append("http://{}/gribcore?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib2cflag.ttl'.format(fpath))
um_call.append("http://{}/grib2?status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'



um_call = copy.copy(call)
um_call.append('@{}/grib2disc.ttl'.format(fpath))
um_call.append("http://{}/grib2/codeflag?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib2statprocess.ttl'.format(fpath))
um_call.append("http://{}/grib2/codeflag?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib2category.ttl'.format(fpath))
um_call.append("http://{}/grib2/codeflag?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib2parameter.ttl'.format(fpath))
um_call.append("http://{}/grib2/codeflag?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

um_call = copy.copy(call)
um_call.append('@{}/grib2surftype.ttl'.format(fpath))
um_call.append("http://{}/grib2/codeflag?batch-managed&status=Experimental".format(base))
print ' '.join(um_call)
subprocess.check_call(um_call)
print '\n\n'

