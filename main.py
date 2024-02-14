from nameparser import HumanName
import requests
import json
import boto3
import time
import re

# host = ssm.get_parameter(Name='/url')['Parameter']['Value']
# api_key = ssm.get_parameter(Name='/apikey')['Parameter']['Value']
api_key ='ql18qZH2ykC0DDwDqGIsnRFSvekJ4ghPhdz2whWt'
host_camps = 'https://developer.nps.gov/api/v1/campgrounds'
host_parks = "https://developer.nps.gov/api/v1/parks"
params = {"api_key": api_key}

def lambda_handler(event, context):

    activities = event['activities'].split(",")
    cost = event['costCap']
    state = event['state']
    params['stateCode'] = state

    response = requests.get(host_camps, params=params)
    if response.status_code != 200:
        raise Exception(response)
    data = response.json()['data']
    affordable = False
    campgrounds = []
    codes = []
    my_map = {}
    for camp in data:
        for fee in camp['fees']:
            if float(fee['cost']) > float(cost):
                affordable = False
                break
            else:
                affordable = True
        
        if affordable:
            codes.append(camp['parkCode'])
            new_map = {camp['parkCode']:camp['name']}
            my_map.update(new_map)
            

    codes = list(set(codes))
    match = False
    for code in codes:
        params['parkCode'] = code
        response = requests.get(host_parks, params=params)
        data = response.json()['data']
        for d in data:
            for activity in activities:
                for a in d['activities']:
                    if activity == a['name'].lower():
                        match = True
                    
            if match:
                campgrounds.append(my_map[code])
                
    return json.dumps({'campgrounds': campgrounds})



if __name__ == "__main__":
    print(lambda_handler({"state":"CO","activities":"hiking,astronomy","costCap":"6"}, None))
