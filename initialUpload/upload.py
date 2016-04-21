import argparse
import copy
import glob
import numpy as np
import os
import requests
import subprocess
import time
import sys
import urllib

parser = argparse.ArgumentParser()
parser.add_argument('user_id')
parser.add_argument("passcode")
parser.add_argument('reg_uri')
parser.add_argument('root')
args = parser.parse_args()

uid = args.user_id
pss = args.passcode



def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')

    return session

def post_file(session, postfile, container, status, bulk=False):
    with open(postfile, 'r') as pf:
        pdata = pf.read()
    params = {'status':status}
    if container == '.':
        container = ''
    else:
        container = '/' + container
    if not args.root and not container:
        container = '/'
    if bulk:
        params = 'batch-managed&' + urllib.urlencode(params)
    url = "{u}{r}{c}".format(u=args.reg_uri,
                                    r=args.root,
                                    c=container)
    print url
    res = session.post(url,
                      headers={'Content-type':'text/turtle'},
                      data=pdata,
                      params=params)
    if res.status_code > 299:
        if res.status_code == 403:
            exists = session.get(url)
            if exists.status_code != 200:
                raise ValueError('Http response code indicates failure\n{}'.format(res.status_code))
        else:
            raise ValueError('Http response code indicates failure\n{}'.format(res.status_code))
    return session


rootDir = os.path.join(os.getcwd(), 'ttl')


session = requests.Session()
session = authenticate(session, args.reg_uri, args.user_id, args.passcode)
    

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        print fname
        status = 'Experimental'
        status = 'Stable'
        if fname.startswith('deprec_'):
            status = 'Deprecated'
        elif fname.startswith('rsvd_'):
            status = 'Reserved'
        if fname.endswith('.ttl'):
            post_file(session,
                                os.path.join(dirName,fname),
                                os.path.relpath(dirName, rootDir),
                                status,
                                fname.startswith('bulk_'))
