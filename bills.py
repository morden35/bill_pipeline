import sys
import requests
import re
# import time
import json
# import sys
# import boto3

API_KEY = 'nt5nhSpwSqMbrGJ7hcsBkXFI1mfk80X0fexbnt45'

def get_bill_ids(lastModifiedStartDate='1990-05-13T02:22:08Z',
                 offset=0,
                 pageSize=1000,
                 congress='116',
                 docClass='s',
                 billVersion='is'):
    '''
    Given an offset value and congress number, this function makes a govinfo
    API call to request a list of 'collections' (bill ids).

    Inputs:
        lastModifiedStartDate (str) - This is the start date and time in
            ISO8601 format (yyyy-MM-dd'T'HH:mm:ss'Z')
        offset (int) - This is the starting record you wish to retrieve
        pageSize (int) - The number of records you would like to return within
            a given request
        congress (str) - congress number (116 default)
        docClass (str) - bill/collection categories (s, hr, hres, sconres)
        billVersion (str) - the bill version (there are 53 possible types)
    Returns:
        data (dictionary) - dictionary returned by API call. contains the
            following keys: count, message, nextPage, previousPage, packages
        returns None if the API call results in bad status code
    '''

    # if docClass == 'all'
    # if billVersion == 'all'

    url = f'https://api.govinfo.gov/collections/BILLS/{lastModifiedStartDate}?offset={offset}&pageSize={pageSize}&congress={congress}&docClass={docClass}&billVersion={billVersion}&api_key={API_KEY}'
    PARAMS = {'headers': 'accept: application/json'}

    r = requests.get(url=url, params=PARAMS)
    # if re.search(r"OVER_RATE_LIMIT", r.content.decode('utf8')):
        # print("Reached limit at offset", offset)
    if r.status_code == 200:
        data = r.json()
        # packages = data['packages']  
        # return data
        with open(f"data/{congress}_{docClass}_{billVersion}.json", "w") as outfile:
            json.dump(data, outfile)
        print(f"{data['count']} bill ids for congress '{congress}', docClass '{docClass}', billVersion '{billVersion}' saved to disk.")
    else:
        print(f"Status code: {r.status_code}")
        # print(r.json()['message'])
        return r.status_code


def get_package(all_bill_ids, congress, version):
    '''
    Given a list of bill ids (pre filtered for those that contain 'climate' in
    title), this function makes a govinfo API call to request the bill text.

    Inputs:
        all_bill_ids (dict) - A dictionary with the congress number as
            the key, and a list of climate_bill_ids (list of bill ids) as the
            value
        congress (str) - the congress number
    Returns:
        This function dumps a dictionary of dictionaries to
        climate_bills/{congress}_bills.json. The dictionary key is the congress
        number. The dictionary value is another nested dictionary. The nested
        dictionary keys are the bill ids. The nested dictionary values are the
        bill text.
    '''
    all_bills = {congress: {}}
    # all_bills = {'116': {}, '115': {}, '114': {}, '113': {}, '112': {},
    #             '111': {}, '110': {}, '109': {}, '108': {}, '107': {},
    #             '106': {}, '105': {}, '104': {}, '103': {}}

    # for congress in all_bill_ids.keys():
    # for num, package in enumerate(all_bill_ids[congress]):
    for num, package in enumerate(all_bill_ids):
        print(num)
        bill_id = package["packageId"]
        # url = f"https://api.govinfo.gov/packages/{bill_id}/summary?api_key={API_KEY}"
        url = f'https://api.govinfo.gov/packages/{bill_id}/htm?api_key={API_KEY}'
        PARAMS = {'headers': 'accept: */*'}
        # PARAMS = {'headers': 'accept: application/json'}
        r = requests.get(url = url, params = PARAMS)
        # need to decode the bytes object
        # bill_summary = json.loads(r.content)
        # bill_text = json.loads(r.content)["download"]["txtLink"]
        if re.search(r"OVER_RATE_LIMIT", r.content.decode('utf8')):
            print("Reached limit at bill", bill_id)
            break
        all_bills[congress][bill_id] = r.content.decode('utf8')

    # NEEDS TO GO IN S3
    bucket_resource.put_object(Key=f'{congress}_bills_v{version}', Body=json.dumps(all_bills))
    print("check S3 again")
    print(len(all_bills[congress]), "bill texts gathered")
#     with open(f'bills/{congress}_bills.json', 'w') as outfile:
#         json.dump(all_bills, outfile)
    # return all_bills


if __name__ == '__main__':
    get_bill_ids()
