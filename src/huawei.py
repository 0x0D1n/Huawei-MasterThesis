from huawei_api import *
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
import ipaddress
import sys

def banner():
    motd = """
    ##################################################################
    # Program created to gather information about your Huawei router #
    # for a forensic analysis.                                       #
    # Use it with caution, every call to the API can alter the data  #
    #                                                                #
    # Default username/password is admin/admin.                      #
    ##################################################################
    """
    print(motd)

#https://stackoverflow.com/questions/11264005/using-a-regex-to-match-ip-addresses-in-python
def valid_ip(address):
    try: 
        ipaddress.ip_address(address)
        return True
    except:
        return False

#Save the data gathered to a file
def writeToFile(filename, content):
    file = open(filename, 'w')
    file.write(content)
    file.close()

#Gather all the data using credentials
def getAllInfoLogin(client):
    data = getISP(client) + "\n"
    data += getDeviceInformation(client) + "\n"
    data += getLanguage(client) + "\n"
    data += getConnectedDevices(client) + "\n"
    data += getTimezone(client) + "\n"
    data += getLogs(client)
    return data

#Gather all the data without credentials
def getAllInfoWithoutLogin(client):
    data = getISP(client) + "\n"
    data += getLanguage(client) + "\n"
    data += getTimezone(client) + "\n"
    data += getLogs(client)
    return data
    

def main():
    banner()
    ### Command line -helper for args
    import argparse
    parser = argparse.ArgumentParser(description="Huawei B315s-22 4G router information gathering tool")
    parser.add_argument("-i", "--ip", type=str, help="IP address of the router", metavar=('IP Router'))
    parser.add_argument("-n", "--nologin", action='store_true', help="Use this if you don't have any credentials")
    parser.add_argument("-u", "--username", type=str, default="admin", help="Username used to login to the router, default=admin")
    parser.add_argument("-p", "--password", type=str, default="admin", help="Password used to login to the router, default=admin")
    parser.add_argument("-w", "--write", type=str, help="Filename", metavar=('FILENAME'))
    args = parser.parse_args()

    #Check if atleast the ip address is given
    if args.ip == None:
        parser.print_help()
    elif valid_ip(args.ip) == False:
        sys.exit("Enter a valid IP address")

    if args.nologin == True:
        try:
            connection = Connection('http://192.168.8.1/')
            client = Client(connection)
            data = getAllInfoWithoutLogin(client)
            if args.write:
                print("Data has been written into : " + args.write + "\n")
                writeToFile(args.write, data)
            else:
                print(data)
        except Exception as e:
            print(e)
    
    if args.username and args.password:
        try:
            connection = AuthorizedConnection('http://'+args.username+':'+args.password+'@'+args.ip+'/')
            client = Client(connection)
            data = getAllInfoLogin(client)
            if args.write:
                print("Data has been written into : " + args.write + "\n")
                writeToFile(args.write, data)
            else:
                print(data)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()