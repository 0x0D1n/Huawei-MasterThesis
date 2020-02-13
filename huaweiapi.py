import requests as r
#import json

'''
def beautifyjson(jsonobj):
    text = json.dumps(jsonobj, sort_keys=True, indent=4)
    print(text)
'''

def getDeviceInformation(ipaddr):
    res = r.get('http://'+ipaddr+'/api/wlan/host-list')
    return res.text