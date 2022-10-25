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

## Code description

## Decisions

## Future Work

## Citations

This pipeline was adapted from a previous project: https://github.com/morden35/bills_nlp_large_scale \
https://api.govinfo.gov/docs/ \
https://github.com/usgpo/api
