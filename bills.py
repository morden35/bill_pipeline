import sys
import requests
import json
import math
from os.path import exists

API_KEY = 'nt5nhSpwSqMbrGJ7hcsBkXFI1mfk80X0fexbnt45'

# CONGRESS_YRS = ['103', '104', '105', '106', '107', '108', '109', '110',
#                 '111', '112', '113', '114', '115', '116', '117']
# DOC_CLASSES = ['s', 'sres', 'sconres', 'sjres', 'hr', 'hres', 'hconres',
#                'hjres']
# BILL_VERSIONS = ['as', 'ash', 'ath', 'ats', 'cdh', 'cds', 'cph', 'cps', 'eah',
#                    'eas', 'eh', 'eph', 'phs', 'enr', 'es', 'fah', 'fph', 'fps',
#                    'hdh', 'hds', 'ih', 'iph', 'ips', 'is', 'lth', 'lts', 'oph',
#                    'ops', 'pav', 'pch', 'pcs', 'pp', 'pap', 'pwah', 'rah',
#                    'ras', 'rch', 'rcs', 'rdh', 'rds', 'reah', 'res', 'renr',
#                    'rfh', 'rfs', 'rh', 'rih', 'ris', 'rs', 'rth', 'rts', 'sas',
#                    'sc']

def get_bill_ids(num_bills=25,
                 congress='116',
                 docClass='s',
                 billVersion='is'):
    '''
    For the given  inputs, this function makes a govinfo
    API call to request a list of 'collections' (bill ids).
    The requested bill ids are saved as json to disk.

    Inputs:
        num_bills (str) - The number of bill texts to retrieve (default 25).
        congress (str) - congress number (116 default)
        docClass (str) - bill/collection categories (s, hr, hres, sconres)
        billVersion (str) - the bill version (there are 53 possible types)
    Returns:
        if the request succeeds, data (dictionary) is saved to disk
            and get_bills() is called
        if the requests does not succeed, returns status code
    '''
    if int(num_bills) > 999:
        print("Max number of API requests reached. Try again with fewer bills.")
        return 400

    bill_id_file = (f"data/ids/{congress}/{congress}_{docClass}_{billVersion}"
                    ".json")
    if exists(bill_id_file):
        # Skip getting bill ids
        # Just get bill texts
        print(f"Id file already exitst for congress '{congress}', docClass "
              f"'{docClass}', billVersion '{billVersion}'.")
        return get_bills(bill_id_file, int(num_bills))

    lastModifiedStartDate='1990-05-13T02:22:08Z'
    offset=0
    pageSize=1000
    url = (f'https://api.govinfo.gov/collections/BILLS/{lastModifiedStartDate}'
           f'?offset={offset}&pageSize={pageSize}&congress={congress}&docClass'
           f'={docClass}&billVersion={billVersion}&api_key={API_KEY}')
    PARAMS = {'headers': 'accept: application/json'}

    print(f"Requesting bill ids for congress '{congress}', docClass '{docClass}', "
          f"billVersion '{billVersion}'.")
    
    try:
        r = requests.get(url=url, params=PARAMS)
    except:
        return "API request failed. Try again with valid arguments."

    if r.status_code == 200:
        data = r.json()
        # Save bill ids to disk
        with open((f"data/ids/{congress}/{congress}_{docClass}_{billVersion}"
                    ".json"), "w") as outfile:
            json.dump(data, outfile)
        print(f"{data['count']} bill ids for congress '{congress}', docClass "
                f"'{docClass}', billVersion '{billVersion}' saved to disk.")
        # Get bill texts
        return get_bills(outfile.name, int(num_bills))
    return r.status_code


def get_bills(bill_id_file, num_bills):
    '''
    Given a file containing bill ids, this function makes a govinfo API call to
    request the bill text.

    Inputs:
        bill_id_file (str) - Path to a file containing json with all bill ids
        num_bills (int) - The number of bill texts to retrieve (default 25).
    Returns:
        This function dumps pdf files containing bill texts into their
        respective folders on disk.
    '''
    congress = bill_id_file.split("/")[2]
    # Read in file with bill ids
    with open(bill_id_file, "rb") as read_content:
        id_content = json.load(read_content)
        all_bill_ids = id_content['packages']
        bill_count = id_content['count']

    # The API allows a maximum of 1000 requests per hour for a given API key.
    max_bills = 999
    num_machines = math.ceil(bill_count / max_bills)
    print(f"At least {num_machines} machines required to reqeust all {bill_count} bills.")
    print(f"Requesting {num_bills} bill texts.")

    bill_ids_saved = []
    for bill in all_bill_ids:
        if len(bill_ids_saved) == num_bills:
            break
        bill_id = bill["packageId"]
        bill_pdf_path = f"data/bills/{congress}/{bill_id}.pdf"
        # Don't request bill that is already saved
        if exists(bill_pdf_path):
            continue
        bill_ids_saved.append(bill_id)
        url = (f"https://api.govinfo.gov/packages/{bill_id}/xml?api_key="
               f"{API_KEY}")
        PARAMS = {'headers': 'accept: */*'}

        # Request bill pdfs
        try:
            r = requests.get(url = url, params = PARAMS)
        except:
            return r.status_code

        # Save bill pdf
        with open(bill_pdf_path, "wb") as outfile:
            outfile.write(r.content)
            print(f"{bill_id} saved")
    print(f"{len(bill_ids_saved)} bill texts (.pdfs) for congress '{congress}'"
          f" saved to disk.")


if __name__ == '__main__':
    get_bill_ids(*sys.argv[1:])
