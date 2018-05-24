import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

url = 'https://api.awhere.com/v2/fields'
consumer_key = '' # key
consumer_secret = '' # secret

# body of request, change to wherever you would like
body = {
    "id": "CN_Tower",
    "name": "Toronto",
    "farmId": "accr",
    "centerPoint": {
        "latitude": 43.642465, # can get these from Google maps
        "longitude": -79.386488
    }
}

# get Authentication token
client = BackendApplicationClient(client_id = consumer_key)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://api.awhere.com/oauth/token', client_id=consumer_key, client_secret=consumer_secret)

# post body to url
client = OAuth2Session(consumer_key, token=token)
field_response = client.post(url, json=body)
print(field_response.json())
