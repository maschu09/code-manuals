import argparse
import copy
import glob
import numpy as np
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('user_id')
parser.add_argument("passcode")
parser.add_argument('reg_uri')
parser.add_argument('root')
args = parser.parse_args()

uid = args.user_id
uid = 'https://profiles.google.com/100578379482821123729'
pss = args.passcode

#authcall = ['curl', '-i' ,'-b', 'cookie-jar', '-c', 'cookie-jar', '--data', 'userid=https://profiles.google.com/100578379482821123729&password={}'.format(pss), 'http://{}/system/security/apilogin']

authcall = ['curl', '-i' ,'-b', 'cookie-jar', '-c', 'cookie-jar', '--data', 'userid={}&password={}'.format(uid, pss), 'http://{}/system/security/apilogin'.format(args.reg_uri)]
print ' '.join(authcall)
subprocess.check_call(authcall)

fpath = os.path.join(os.getcwd(), 'ttl')

def post_call(postfile, container, status, bulk=False):
    call = ['curl', '-i', '-b', 'cookie-jar', '-H', 'Content-type:text/turtle',
            "-X", "POST", "--data"]
    # concall = copy.copy(call)
    call.append('@{}'.format(postfile))
    bulkstr = ''
    if bulk:
        bulkstr = 'batch-managed&'
    call.append("http://{r}/{c}?{b}status={s}".format(r=args.reg_uri,
                                                      c=args.root,
                                                      b=bulkstr,
                                                      s=status))
    print ' '.join(call)
    subprocess.check_call(call)
    print '\n\n'

rootDir = os.path.join(os.getcwd(), 'ttl')

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname.endswith('.ttl'):
            post_call(os.path.join(dirName,fname),
                      os.path.relpath(dirName, rootDir),
                      'Experimental',
                      fname.startswith('bulk_'))
