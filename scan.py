import sys
import hashlib
import requests
import json
import time
import os

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
sha1 = hashlib.sha1()

if len(sys.argv) < 2:
    print('\nNO FILE FOUND. PLEASE SUBMIT A FILE')
    print('ex: python scan.py FILENAME\n')

elif len(sys.argv) > 2:
    print('\nSUBMIT 1 FILE FOR SCANNING\n')
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
    if os.path.isfile('apiKey.txt'):
        with open('apiKey.txt','r') as f:
            api_key = f.read()
    else:
        print('\nNO API KEY FILE, USE HARDCODED KEY')
        api_key = '12345'

    #create key:value pair to hold header apikey
    headers = {'apikey':api_key}

    print('\nCHECKING HASH  {}\n'.format(result_sha1))
    #checking sha1 hash against opswat database
    res = requests.get('https://api.metadefender.com/v2/hash/{}'.format(result_sha1), headers=headers)

    #raises an error when result status_code is a failure
    res.raise_for_status()

    #turn the response content into a json object
    r = res.json()
    
    #if the hash is not found, the json object will be small
    if len(r) < 2:
        print('HASH NOT FOUND\nUPLOADING FILE: {}  FOR SCANNING'.format(sys.argv[1]))
        with open(sys.argv[1],'rb') as f:
            file = {'file':f}
            res = requests.post(url='https://api.metadefender.com/v2/file', headers=headers, files=file)
        res.raise_for_status()
        r = res.json()
        data_id = r['data_id']
        print('SCANNING IN PROGRESS')
        while True:
            res = requests.get(url='https://api.metadefender.com/v2/file/{}'.format(data_id), headers=headers)
            r = res.json()
            if 'scan_results' not in r:
                break
            elif r['scan_results']['progress_percentage'] == 100:
                break
            print(r['scan_results']['progress_percentage'])
            #wait 5 seconds between pings for results
            time.sleep(5)
        print('DONE\nPrinting Results:')
        print(json.dumps(r, indent=4))
    else:
        print('HASH FOUND\nPrinting Results:')
        print('filename: {}'.format(sys.argv[1]))
        #pretty print results
        print(json.dumps(r, indent=4))

print('\nEND\n')