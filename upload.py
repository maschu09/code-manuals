import argparse
import copy
import glob
import numpy as np
import os
import subprocess
import time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('user_id')
parser.add_argument("passcode")
parser.add_argument('reg_uri')
parser.add_argument('root')
args = parser.parse_args()

uid = args.user_id
uid = 'https://profiles.google.com/100578379482821123729'
pss = args.passcode


authcall = ['curl', '-i' ,'-b', 'cookie-jar', '-c', 'cookie-jar', '--data', 'userid={}&password={}'.format(uid, pss), '{}/system/security/apilogin'.format(args.reg_uri)]
print(' '.join(authcall))
subprocess.check_call(authcall)

fpath = os.path.join(os.getcwd(), 'ttl')

def post_call(postfile, container, status, bulk=False):
    call = ['curl', '-i', '-b', 'cookie-jar', '-H', 'Content-type:text/turtle',
            "-X", "POST", "--data"]
    call.append('@{}'.format(postfile))
    bulkstr = ''
    if bulk:
        bulkstr = 'batch-managed&'
    if container == '.':
        container = ''
    else:
        container = '/' + container
#    container = '/' + container
    if not args.root and not container:
        container = '/'
    call.append("{u}{r}{c}?{b}status={s}".format(u=args.reg_uri,
                                                      r=args.root,
                                                      c=container,
                                                      b=bulkstr,
                                                      s=status))
    print('\n')
    print ' '.join(call)
    subprocess.check_call(call)
    print('\n')
    sys.stdout.flush()

rootDir = os.path.join(os.getcwd(), 'ttl')

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        status = 'Experimental'
        status = 'Stable'
        if fname.startswith('deprec_'):
            status = 'Deprecated'
        elif fname.startswith('rsvd_'):
            status = 'Reserved'
        if fname.endswith('.ttl'):
            post_call(os.path.join(dirName,fname),
                      os.path.relpath(dirName, rootDir),
                      status,
                      fname.startswith('bulk_'))
