from huawei_lte_api.Client import Client
import requests as r
import json


def beautifyjson(jsonobj):
    text = json.dumps(jsonobj, sort_keys=True, indent=4)
    return text


def getDeviceInformation(client):
    """
    Retrieve all the devices information.
    Model, firmware version, IMEI, serial, ...
    """
    return beautifyjson(client.device.information())