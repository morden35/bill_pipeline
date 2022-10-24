import sys
import requests
import json
import math
from os.path import exists
# import re
# import time
# import sys
# import boto3

API_KEY = 'nt5nhSpwSqMbrGJ7hcsBkXFI1mfk80X0fexbnt45'

CONGRESS_YRS = ['103', '104', '105', '106', '107', '108', '109', '110',
                '111', '112', '113', '114', '115', '116', '117']
DOC_CLASSES = ['s', 'sres', 'sconres', 'sjres', 'hr', 'hres', 'hconres',
               'hjres']
BILL_VERSIONS = ['as', 'ash', 'ath', 'ats', 'cdh', 'cds', 'cph', 'cps', 'eah',
                   'eas', 'eh', 'eph', 'phs', 'enr', 'es', 'fah', 'fph', 'fps',
                   'hdh', 'hds', 'ih', 'iph', 'ips', 'is', 'lth', 'lts', 'oph',
                   'ops', 'pav', 'pch', 'pcs', 'pp', 'pap', 'pwah', 'rah',
                   'ras', 'rch', 'rcs', 'rdh', 'rds', 'reah', 'res', 'renr',
                   'rfh', 'rfs', 'rh', 'rih', 'ris', 'rs', 'rth', 'rts', 'sas',
                   'sc']

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
    bill_id_file = f'data/ids/{congress}/{congress}_{docClass}_{billVersion}.json'
    if exists(bill_id_file):
        # Skip getting bill ids
        # Just get bill texts
        return get_package(bill_id_file)
    
    url = f'https://api.govinfo.gov/collections/BILLS/{lastModifiedStartDate}?offset={offset}&pageSize={pageSize}&congress={congress}&docClass={docClass}&billVersion={billVersion}&api_key={API_KEY}'
    PARAMS = {'headers': 'accept: application/json'}

    r = requests.get(url=url, params=PARAMS)
    if r.status_code == 200:
        data = r.json()
        with open(f"data/ids/{congress}/{congress}_{docClass}_{billVersion}.json", "w") as outfile:
            json.dump(data, outfile)
        print(f"{data['count']} bill ids for congress '{congress}', docClass '{docClass}', billVersion '{billVersion}' saved to disk.")
        # Get bill texts
        return get_package(outfile.name)
    print(f"Status code: {r.status_code}")
    return r.status_code


def get_package(bill_id_file):
    '''
    Given a file containing bill ids, this function makes a govinfo API call to
    request the bill text.

    Inputs:
        bill_id_file (str) - Path to a file containing json with all bill ids
    Returns:
        This function dumps pdf files containing bill texts into their respective
        folders on disk.
    '''
    congress = bill_id_file.split("/")[2]
    with open(bill_id_file, "rb") as read_content:
        id_content = json.load(read_content)
        all_bill_ids = id_content['packages']
        bill_count = id_content['count']

    # The API allows a maximum of 1000 requests per hour for a given API key.
    max_bills = 1000
    num_machines = math.ceil(bill_count / max_bills)
    print(f"{num_machines} machines required to get all {bill_count} bills in 1 hour.")
    print("As a trial, we will get the first 10 bills.")

    bill_ids_saved = []
    for bill in all_bill_ids:
        if len(bill_ids_saved) == 10:
            break
        bill_id = bill["packageId"]
        bill_pdf_path = f"data/bills/{congress}/{bill_id}.pdf"
        if exists(bill_pdf_path):
            continue
        bill_ids_saved.append(bill_id)
        url = f'https://api.govinfo.gov/packages/{bill_id}/xml?api_key={API_KEY}'
        PARAMS = {'headers': 'accept: */*'}
        r = requests.get(url = url, params = PARAMS)
        with open(bill_pdf_path, "wb") as outfile:
            outfile.write(r.content)
    print(f"{len(bill_ids_saved)} bill texts (.pdfs) for congress '{congress}' saved to disk: {bill_ids_saved}")


if __name__ == '__main__':
    try:
        get_bill_ids(*sys.argv[1:])
    except:
        print("Please try again with valid command line arguments.")
