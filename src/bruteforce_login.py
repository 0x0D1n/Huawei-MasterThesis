#from huawei_api import *
#from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
import sys
import datetime

def banner():
    motd = """
    BRUTEFORCE LOGIN
    """
    print(motd)

def main():
    banner()
    currentDT = datetime.datetime.now()
    number_logins = int(input("Number of login attempts: "))
    for x in range(0,number_logins):
        connection = AuthorizedConnection('http://admin:password123@192.168.8.1/')
        client = Client(connection)
        print("Login number " + str(x+1) + " at: " + currentDT.strftime("%I:%M:%S %p"))

if __name__ == "__main__":
    main()
