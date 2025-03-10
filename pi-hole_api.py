#!/usr/bin/env python3

import requests,json

env_file = '.env.txt'

url = "https://pi.hole/api/auth"

def read_data(filename):
    try:
        data_infile = open( filename , 'r')
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        create_api_file(filename)
        data_infile = open( filename , 'r')
    read_data=data_infile.read()
    data_infile.close()
    return read_data

def create_api_file(filename):
    api_key=input("Please enter a valid api key: ")
    
    try:
        data_outfile = open( filename , 'w')
        
        data_outfile.write("{{ 'password' : '{}' }}".format(api_key))
    except IOError:
        print("Unable to open "+data_outfile)

def load_payload(env_file):
    payload = json.loads(read_data(env_file))
    return payload

def get_response(url,payload) :
    response = requests.request("POST",url, json=payload, verify=False)
    return response

def close_conn(url,sid) :
    headers = {
        "X-FTL-SID": sid
    }

    response = requests.request("DELETE", url, headers=headers, data=payload, verify=False)
    
    if response == 204:
        print (response)
    else:
        print(response,response.text)


payload = load_payload(env_file)
# print (payload,type(payload),json.dumps(payload))

response = get_response(url,payload)
print (response.text)


# response = {"session":{"valid":true,"totp":false,"sid":"/ZIH3QlXxOa8FE030aVXfg=","csrf":"Tt63cGi4McV/BAQeSlWz4g=","validity":2592000,"message":"app-password correct"},"took":0.99909329414367676}
resp_json = response.json()

session_data = resp_json['session'].items()

valid, topt, sid, csrf, validity, message = dict(session_data).values() 
# print (dict(session_data).values())

close_conn(url,sid)

print(valid, topt, sid, csrf, message)
