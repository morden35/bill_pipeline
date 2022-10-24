import sys
import requests
import json
import math
# import re
# import time
# import sys
# import boto3

API_KEY = 'nt5nhSpwSqMbrGJ7hcsBkXFI1mfk80X0fexbnt45'

def get_bill_ids(congress='116',
                 docClass='s',
                 billVersion='is',
                 lastModifiedStartDate='1990-05-13T02:22:08Z',
                 offset=0,
                 pageSize=1000):
    '''
    For the given  inputs, this function makes a govinfo
    API call to request a list of 'collections' (bill ids).
    The requested bill ids are saved as json to disk.

    Inputs:
        congress (str) - congress number (116 default)
        docClass (str) - bill/collection categories (s, hr, hres, sconres)
        billVersion (str) - the bill version (there are 53 possible types)
        lastModifiedStartDate (str) - This is the start date and time in
            ISO8601 format (yyyy-MM-dd'T'HH:mm:ss'Z')
        offset (int) - This is the starting record you wish to retrieve
        pageSize (int) - The number of records you would like to return within
            a given request
    Returns:
        if the request succeeds, data (dictionary) is saved to disk
            and get_package() is called
        if the requests does not succeed, returns status code
    '''
    url = f'https://api.govinfo.gov/collections/BILLS/{lastModifiedStartDate}?offset={offset}&pageSize={pageSize}&congress={congress}&docClass={docClass}&billVersion={billVersion}&api_key={API_KEY}'
    PARAMS = {'headers': 'accept: application/json'}

    r = requests.get(url=url, params=PARAMS)
    if r.status_code == 200:
        data = r.json()
        with open(f"data/ids/{congress}/{congress}_{docClass}_{billVersion}.json", "w") as outfile:
            json.dump(data, outfile)
        print(f"{data['count']} bill ids for congress '{congress}', docClass '{docClass}', billVersion '{billVersion}' saved to disk.")
        # Get bill texts
        # print(outfile.name)
        get_package(outfile.name)
    else:
        print(f"Status code: {r.status_code}")
        return r.status_code


def get_package(id_file):
    '''
    Given a list of bill ids, this function makes a govinfo API call to
    request the bill text.

    Inputs:
        all_bill_ids (list) - A list of dictionaries that contain all
            bill ids
        congress (str) - the congress number
        billVersion (str) - the bill version (there are 53 possible types)
        bill_count (int) - the number of bills to retrieve
    Returns:
        This function dumps a dictionary of dictionaries to
        climate_bills/{congress}_bills.json. The dictionary key is the congress
        number. The dictionary value is another nested dictionary. The nested
        dictionary keys are the bill ids. The nested dictionary values are the
        bill text.
    '''
    congress = id_file.split("/")[2]
    with open(id_file, "rb") as read_content:
        id_content = json.load(read_content)
        all_bill_ids = id_content['packages']
        bill_count = id_content['count']

    # The API allows a maximum of 1000 requests per hour for a given API key.
    max_bills = 1000
    num_machines = math.ceil(bill_count / max_bills)
    print(f"{num_machines} machines required to get all {bill_count} bills in 1 hour.")
    print("As a trial, we will get the first 10 bills.")

    bill_ids_saved = []
    for bill in all_bill_ids[:10]:
        bill_id = bill["packageId"]
        bill_ids_saved.append(bill_id)
        url = f'https://api.govinfo.gov/packages/{bill_id}/xml?api_key={API_KEY}'
        PARAMS = {'headers': 'accept: */*'}
        r = requests.get(url = url, params = PARAMS)

        with open(f"data/bills/{congress}/{bill_id}.pdf", "wb") as outfile:
            outfile.write(r.content)
    print(f"10 bill texts (.pdfs) for congress '{congress}' saved to disk: {bill_ids_saved}")


if __name__ == '__main__':
    if sys.argv[0] == 'get_package':
        get_package(*sys.argv[1:])
    else:
        get_bill_ids(*sys.argv[2:])
    

