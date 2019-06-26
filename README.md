# search-competetor-customer-in-gmail
Search from new email leads in email, ie for a given keyword get the the list of from and list of Cc for all search results
1. It looks up all gmails for a given query.
2. For each of the emails it fetch the 'From' and 'Cc'
3. It pushes those emial to a google spread sheet named "competetor-customer-fetch-from-email"

## Setup

1. Create OAuth credentials and download credentials file as json (https://developers.google.com/gmail/api/quickstart/python)
2. Create Service Account Credentials and download credentials file as json
3. Create a google spread sheet named "competetor-customer-fetch-from-email" and share it with `username@serviceaccountname.iam.gserviceaccount.com`
4. Move the downloaded OAuth's `client_secret.json` file(ie `client_secret_ishandutta2007.json` in my case) to the project root directory.
5. Move the downloaded Service account credentials' json file(ie `bigbullscollab-55669a1c65c2.json` in my case) to the project root directory.
6. `pip install -r requirements.txt`
7. Change the `query_string` varibale in `fetch_from_mail_and_pushto_spreadsheet.py` as per your need and run `python3 fetch_from_mail_and_pushto_spreadsheet.py`


### Support:

If you want the good work to continue please support us on

* [PAYPAL](https://www.paypal.me/ishandutta2007)
* [BITCOIN ADDRESS: 3LZazKXG18Hxa3LLNAeKYZNtLzCxpv1LyD](https://www.coinbase.com/join/5a8e4a045b02c403bc3a9c0c)
