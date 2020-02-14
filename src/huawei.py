from huaweiapi import *
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
import ipaddress
import sys

def banner():
    motd = """
    -----------------------------------------------------------------------------
    | Program created to gather information about your Huawei router            |
    | for a forensic analysis. Even if Huawei don't disclose much to the public.|
    |                                                                           |
    | Default username/password is admin/admin.                                 |
    -----------------------------------------------------------------------------
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
    

def main():
    banner()
    ### Command line -helper for args
    import argparse
    parser = argparse.ArgumentParser(description="Huawei-router information gathering")
    parser.add_argument("-i", "--ip", type=str, help="IP address of the router")
    parser.add_argument("-u", "--username", type=str, default="admin", help="Username used to login to the router, default=admin")
    parser.add_argument("-p", "--password", type=str, default="admin", help="Password used to login to the router, default=admin")
    parser.add_argument("-w", "--write", type=str, help="Filename")
    args = parser.parse_args()

    #Check if atleast the ip address is given
    if args.ip == None:
        parser.print_usage()
    elif valid_ip(args.ip) == False:
        sys.exit("Enter a valid IP address")

    try:
        # connection = Connection('http://192.168.8.1/') For limited access, I have valid credentials no need for limited access
        connection = AuthorizedConnection('http://'+args.username+':'+args.password+'@'+args.ip+'/')
        client = Client(connection)
    except Exception as e:
        print(e)
    
    #data = getDeviceInformation(client)
    #writeToFile("test.txt", data)
    print(getDeviceInformation(client))


if __name__ == "__main__":
    main()