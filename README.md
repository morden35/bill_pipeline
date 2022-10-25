# Congressional Bills Pipeline

The [GovInfo](https://www.govinfo.gov/) site provides access to U.S. government information and documents to the public. This project focuses specifically on accessing and downloading [Congressional Bills](https://www.govinfo.gov/app/collection/bills). GovInfo provides an [API](https://api.govinfo.gov/docs/), which allows developers to request bills (and accompanying information) programmatically. This could be valuable for a number of use cases. For example, if a user is interested in all Senate bills from the 116th Congress (years 2019-2020), they could access those bills via the API. Projects could include natural language processing and/or machine learning techniques to determine which bills are likely to pass/fail and become law. Alternative projects could include sorting and filtering bills based on keywords such as 'climate' or 'reproductive health'. Such projects are dependend on the acquisition and storage of the 240,000+ available bill texts, which is the focus of this project.

## Dependencies

In order to run the Congressional Bills pipeline, a version of Python 3 must be installed on your machine. Visit [Python's documentation](https://www.python.org/downloads/) to download the latest Python version for your machine. I worked in Python 3.9.12 for this project.

The pipeline requires the following modules. These modules are built into [Python's standard library](https://docs.python.org/3/library/) (no need to install if Python 3 is already installed on your machine):
- sys
- json
- math
- os.path

Additionally, the pipeline requires the installation of the [requests library](https://pypi.org/project/requests/). Installation step included in the [How to run](https://github.com/morden35/bill_pipeline#how-to-run) section of this document.

## How to run

First, clone and navigate to this repository:\
`$ git clone git@github.com:morden35/bill_pipeline.git`\
`$ cd bill_pipeline/`

Next, install the required libraries:\
`$ pip install -r requirements.txt`

The pipeline takes in 4 optional arguments:
- num_bills - The number of bill texts to retrieve (default 25, max 999)
- congress - congress number (default 116), (options include 103-117)
- docClass - bill category (defaut s), (options include: s, hr, hres, sconres)
- billVersion - bill version (default is), (there are 53 possible version types, listed in [bills.py](https://github.com/morden35/bill_pipeline/blob/main/bills.py) file)

To run the pipeline, run the following from the command line:\
`$ python3 bills.py <num_bills> <congress> <docClass> <billVersion>`

## Pipeline description

Arguments -> get_bill_ids() -> get_bills() -> Storage

This pipeline is relatively simple and is made up of 2 functions, get_bill_ids() and get_bills().

### get_bill_ids()

In order to request and download bill texts from the GovInfo API, we first need to know the bill ids (aka 'packageID') of interest. The goal of get_bill_ids() is to retrieve the bill ids of interest from the API before calling get_bills(). It does so through the following steps:

- Take in the user provided argments (if any) and check if those arguments are valid.
- Check if the file with the bill ids of interest is already saved to disk as to avoid extra API calls.
- If the file already exists, call get_bills().
- If the file with the bill ids does not exists, make a request to the GovInfo API \/collections endpoint.
- If the request succeeds, save the bill ids to disk and call get_bills().
- If the request fails, return the status code.

### get_bills()

Once we have a file containing the bill ids of interest, we can finally get the bill texts of interest. get_bills() does so through the following steps:

- Open and read the file contents.
- Retrieve the bill ids of interest and the number of total bills.
- For each bill id, check that the bill text is not already saved to disk as to avoid extra API calls.
- If the bill text is already saved, move on to the next bill id.
- If the bill text is not already saved, make a request to the GovInfo API \/packages endpoint.
- If the request succeeds, save the bill text (.pdf) to disk.
- If the request fails, return the status code.

## Decisions

## Future Work

1. Parallelization
2. More Robust Storage
3. More Robust Input Checks
4. More Robust Error Handling

## Citations

This pipeline was adapted from a previous project: https://github.com/morden35/bills_nlp_large_scale \
https://api.govinfo.gov/docs/ \
https://github.com/usgpo/api
