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
parser.add_argument('entity')
parser.add_argument('filename')

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

def put_file(session, putfile):
    with open(putfile, 'r') as pf:
        pdata = pf.read()
    params = {'status':status}
    url = "{u}{r}{c}".format(u=args.reg_uri,
                                    r=args.entity)
    res = session.put(url,
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


session = requests.Session()
session = authenticate(session, args.reg_uri, args.user_id, args.passcode)
    
put_file(session, args.filename)
