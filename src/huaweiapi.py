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
    data = beautifyjson(client.net.current_plmn())
    new_dict = json.loads(data)
    isp = new_dict["FullName"]
    return "[+] Internet Service Provider(ISP) [+]\nProvider : " + isp

def getDeviceInformation(client):
    """
    Retrieve all the devices information.
    Model, firmware version, IMEI, serial, ...
    """
    data = beautifyjson(client.device.information())
    new_dict = json.loads(data)
    formatted_info = "[+] Device Information [+]\n"
    formatted_info += "Device Name :\t\t" + new_dict["DeviceName"] + "\n"
    formatted_info += "Software Version : \t" + new_dict["SoftwareVersion"] + "\n"
    formatted_info += "Hardware Version : \t" + new_dict["HardwareVersion"] + "\n"
    formatted_info += "Mac Address : \t\t" + new_dict["MacAddress1"] + "\n"
    formatted_info += "Serial Number :\t\t" + new_dict["SerialNumber"] + "\n"
    
    formatted_info += "\n[+] Sim Card Information [+]\n"
    formatted_info += "Sim Card Identity(Iccid): \t" + new_dict["Iccid"] + "\n"
    formatted_info += "Mobile Identity(Imei): \t\t" + new_dict["Imei"] + "\n"
    formatted_info += "Mobile subscriber(Imsi): \t" + new_dict["Imsi"] + "\n"

    return formatted_info
    
def getLanguage(client):
    """
    Retrieve the language of the router
    """
    return beautifyjson(client.language.current_language())

def getConnectedDevices(client):
    """
    Retrieve the currently connected devices
    """
    data = beautifyjson(client.wlan.host_list())
    new_dict = json.loads(data)
    formatted_devices = "[+] List of connected devices [+]\n"
    if len(new_dict["Hosts"]["Host"]) == 0:
        formatted_devices += "No connected devices currently on the WiFi"
    else:
        for x in range(0, len(new_dict["Hosts"]["Host"])):
            formatted_devices += "[+] Device number " + str(x+1) + " [+]\n"
            formatted_devices += "Hostname: \t" + new_dict["Hosts"]["Host"][x]["HostName"] + "\n"
            formatted_devices += "IP address: " + new_dict["Hosts"]["Host"][x]["IpAddress"] + "\n"
            formatted_devices += "Mac address: " + new_dict["Hosts"]["Host"][x]["MacAddress"] + "\n"
    return formatted_devices

def getTimezone(client):
    """
    Retrieve NTP information
    """
    return beautifyjson(client.s_ntp.get_settings())


def getLogs(client):
    """
    Retrieve SysLogs - ONLY ONE AVAILABLE WITHOUT TOUCHING THE HARDWARE SEEMS LIKE
    Log format: "Time","Level","Module name","Result","Content"
    Level : 0 -> Informative
    Level : 1 -> Warning
    Level : 2 -> Error
    Level : 3 -> Critical

    Module name : 0 -> Platform
    1,2??
    Module name : 3 -> Upgrade

    Result: 0 -> Succeeded
    Result: 1 -> Failed

    Content: 0xff1a0001 -> Log in (Succeed)
    Content: 0xff1a0002 -> Log in (Failed)
    Content: 0xff1a0003 -> Log out (Succeed)
    Other codes not disclosed ?!
    """
    def checkLevel(level):
        if level == '0':
            return "Informative"
        elif level == '1':
            return "Warning"
        elif level == '2':
            return "Error"
        else:
            return "Critical"

    def checkModule(level):
        if level == '0':
            return "Platform"
        elif level == '3':
            return "Upgrade"

    def checkResult(level):
        if level == '0':
            return "Succeeded"
        elif level == '1':
            return "Failed"

    def checkContent(level):
        if level == '0xff1a0001':
            return "Log in"
        elif level == '0xff1a0002':
            return "Log in"
        elif level == '0xff1a0003':
            return "Log out"
        else:
            return level + ". Code is not known, check on the web UI"
    
    data = client.syslog.querylog()["content"]
    lines = data.split(";")
    new_lines = []
    for x in lines:
        new_data = x.split(",")
        if '' in new_data:
            break
        new_data[1] = checkLevel(new_data[1])
        new_data[2] = checkModule(new_data[2])
        new_data[3] = checkResult(new_data[3])
        new_data[4] = checkContent(new_data[4])
        to_str = " ".join(new_data)
        new_lines.append(to_str)
    
    formatted_logs = ""

    for x in new_lines:
        formatted_logs += x+"\n"

    return formatted_logs