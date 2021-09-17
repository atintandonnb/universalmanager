import sys
import requests
import json
import time
import requests.packages.urllib3 as urllib3
urllib3.disable_warnings()
from Configuration import *

headers= {'Content-Type': 'application/json', 'Accept': 'application/json'}

def getTokens():
   data={
           "username":user,
           "password":pwd
           #,"authentication_id":ldapname
       }  
   login_api_url="/ServicesAPI/API/V1/Session"
   Login_url=host_url+login_api_url
   token = requests.post(Login_url,data=json.dumps(data),headers=headers,verify=False)
   if token.status_code==200:
       return token.json()
   else:
       exit(time.ctime()+": Login to NetBrain failed")

def setWorkingDomain():
   data={
           "tenantId":tenant_id,
           "domainId":domain_id
       }  
   set_domain_api="/ServicesAPI/API/V1/Session/CurrentDomain"
   set_domain_url=host_url+set_domain_api
   token = requests.put(set_domain_url,data=json.dumps(data),headers=headers,verify=False)
   if token.status_code==200:
       print(time.ctime()+': Set NetBrain Domain successful \n')
   else:
       exit(time.ctime()+f": Set NetBrain Domain failed {token.text}")


def get_device_raw_data(hostname):
    
    headers["Token"] = token
    get_device_raw_data_url = host_url + "/ServicesAPI/API/V1/CMDB/Devices/DeviceRawData"

    data = {
        "hostname" : hostname,
        "dataType" : 2,
        "tableName" : "",
        "vrf" : "",
        "cmd" : "show log"
    }
    
    try:
        response = requests.get(get_device_raw_data_url, params = data, headers = headers, verify = False)
        if response.status_code == 200:
            result = response.json()
            return (result)
        else:
            return ("Get raw data failed - " + str(response.text))

    except Exception as e:
        return (str(e))


def getDevices():
    full_url = host_url + "/ServicesAPI/API/V1/CMDB/Devices"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    headers["Token"]=token

    data = {
        "version": 1
    }


    try:
        response = requests.get(full_url, params = data, headers = headers, verify = False)
        if response.status_code == 200:
            result = response.json()
            #print (result)
            return result
        else:
            print("Get Devices failed! - " + str(response.text))
    except Exception as e:
        print (str(e)) 


def buildTextFile(hostname, data):

    f= open("test.txt","w+")
    f.write(data)
    f.close()



if __name__ == '__main__':

    #get token
    recievedtoken= getTokens()
    token = recievedtoken['token']
    print(time.ctime()+': Login into NetBrain successful: '+token+'\n')
    headers["Token"] = token
    
    #set working domain
    setWorkingDomain()

    device_data = getDevices()
    device_list = []
    for device in device_data.get("devices"):
        device_list.append(device.get('name'))
    
    print(device_list)

    for device in device_list:
        print(get_device_raw_data(device))

    buildTextFile("US-BOS-R1", "sample text")

