from huawei_lte_api.Client import Client
import requests as r
import json


def beautifyjson(jsonobj):
    text = json.dumps(jsonobj, sort_keys=True, indent=4)
    return text


def getISP(client):
    """
    Retrieve the ISP operating the router
    """
    return beautifyjson(client.net.current_plmn())

def getDeviceInformation(client):
    """
    Retrieve all the devices information.
    Model, firmware version, IMEI, serial, ...
    """
    return beautifyjson(client.device.information())

def getLanguage(client):
    """
    Retrieve the language of the router
    """
    return beautifyjson(client.language.current_language())

def getConnectedDevices(client):
    """
    Retrieve the currently connected devices
    """
    return beautifyjson(client.wlan.host_list())


def getTimezone(client):
    """
    Retrieve NTP information
    """
    return beautifyjson(client.s_ntp.get_settings())

def getLogs(client):
    """
    Retrieve SysLogs - Need to be decoded ?
    """
    return beautifyjson(client.syslog.querylog())


