import sys
import hashlib
import requests
import json

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
sha1 = hashlib.sha1()

if len(sys.argv) < 2:
    print('NO FILE FOUND. PLEASE SUBMIT A FILE')
    print('ex: python scan.py FILENAME\n')

elif len(sys.argv) > 2:
    print('SUBMIT 1 FILE FOR SCANNING\n')
else:
    #open file, read in chunks, update the hash
    with open(sys.argv[1], 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    result_sha1 = sha1.hexdigest().upper()

    #read in the apiKey from apiKey.txt
    with open('apiKey.txt','r') as f:
        api_key = f.read()

    #create key:value pair to hold header apikey
    headers = {'apikey':api_key}

    print('\nCHECKING HASH  {}\n'.format(result_sha1))
    res = requests.get('https://api.metadefender.com/v2/hash/{}'.format(result_sha1), headers=headers)
    res.raise_for_status()
    r = res.json()
    if len(r) < 2:
        if r['{}'.format(result_sha1)] == 'Not Found':
            print('HASH NOT FOUND\nUPLOADING FILE: {}  FOR SCANNING'.format(sys.argv[1]))
            with open(sys.argv[1],'rb') as f:
                files = {'file':f}
                res = requests.post(url='https://api.metadefender.com/v2/file', headers=headers, files=files)
            print(res)
            r = res.json()
            print(json.dumps(r, indent=4))
    else:
        print('HASH FOUND\nPrinting Results:')
        print(json.dumps(r, indent=4))