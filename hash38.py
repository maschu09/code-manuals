import argparse
import requests

identifier = '<http://metarelate.net/vocabulary/index.html#identifier>'
identified_by = '<http://metarelate.net/vocabulary/index.html#identifiedBy>'


headers = {'content-type': 'text/turtle', 'Accept': 'text/turtle'}

def update_id_pred(session, reg_uri, items):
    for url in items:
        url = url.format(reg_uri)
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            replacement = response.text.replace(identifier, identified_by)
        params = {'status':'Stable'}
        params = {}
        session.get('{}/common'.format(reg_uri))
        res = session.put(url,
                      headers={'Content-type':'text/turtle'},
                      data=replacement.encode('utf-8'),
                      params=params)
        if res.status_code != 204:
            msg = 'Failed to PUT: \n{}\nto:\n{}'.format(replacement, url)
            raise ValueError(msg)

def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')
    session.get('{}/common'.format(base))


def find_id_pred(session, reg_uri):
    sparql_query = ('SELECT ?entity '
                    'WHERE { '
                    '?entity  <http://metarelate.net/vocabulary/index.html#identifier> ?idr .'
                    '} '
                    'group by ?entity')
    endpoint = '{}/system/query'.format(reg_uri)
    payload = {'query': sparql_query, 'output':'json'}
    results = session.get(endpoint, params=payload)
    items = results.json()['results']['bindings']
    items = [i['entity']['value'] for i in items]
    items = [i.replace('http://codes.wmo.int', '{}') for i in items]
    return items
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument("passcode")
    parser.add_argument('reg_uri')
    args = parser.parse_args()
    session = requests.Session()
    authenticate(session, args.reg_uri, args.user_id, args.passcode)
    items = find_id_pred(session, args.reg_uri)
    update_id_pred(session, args.reg_uri, items)

if __name__ == '__main__':
    main()
