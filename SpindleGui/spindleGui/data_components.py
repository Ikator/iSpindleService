import requests

def updateData(spindleName):
    resp = requests.get(f'http://spindle-api/spindle/{spindleName}/data')
    
    if resp.status_code != 200:
        # This means something went wrong.
        return None
    else :
        return resp.json()['data']

def getSpindleName(pathname):
    if pathname is not None and pathname != '/':
        return pathname.split('/')[-1]

def convertData(data, attribute ):
    return [d[attribute] for d in data]
            