#*****histWeather.py*****#
import requests, json, base64

id = 'CN_Tower' # field id
date = '05-23' # month and day that you would like 10 year average for
key = ''
secret = ''

# *****Get aWhere security token*****#
def getToken():
    combination = key+':'+secret.encode()
    auth = base64.b64encode(combination).decode('utf8')

    credential = auth
    response = requests.post('https://api.awhere.com/oauth/token',
                             data='grant_type=client_credentials',
                             headers={'Content-Type': 'application/x-www-form-urlencoded',
                                      'Authorization': 'Basic {}'.format(credential)}).json()

    if 'access_token' and 'expires_in' in response.keys():
        print(response['access_token'])
        return response['access_token']
    else:
        raise ValueError(response)


token = getToken()  # get auth token

headers = {"Authorization": "Bearer " + token,
           "Content-Type": "application/json"}
response = requests.get('https://api.awhere.com/v2/weather/fields/'+id+'/norms/'+date, headers=headers)
data = response.json()
print(str(data['meanTemp']['average']))
print(response)
