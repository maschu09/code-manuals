import argparse
import requests

coulomb = '<http://codes.wmo.int/common/unit/C>'
degc = '<http://codes.wmo.int/common/unit/degC>'

items = ['{}/bufr4/b/12/023',
         '{}/bufr4/b/12/024'
         ]

headers = {'content-type': 'text/turtle', 'Accept': 'text/turtle'}

def update_units(session, reg_uri):
    for url in items:
        url = url.format(reg_uri)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            replacement = response.text.replace(coulomb, degc)
        params = {'status':'Stable'}
        res = session.put(url,
                          headers={'Content-type':'text/turtle'},
                          data=replacement,
                          params=params)

def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')

    return session



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument("passcode")
    parser.add_argument('reg_uri')
    args = parser.parse_args()
    session = requests.Session()
    session = authenticate(session, args.reg_uri, args.user_id, args.passcode)
    update_units(session, args.reg_uri)

if __name__ == '__main__':
    main()
