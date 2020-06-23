
import pandas
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor

pandas.set_option("display.max_columns", 60)
requests.Session().verify = False

#AllAssessmentsCombined

input_file_name = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombinedV2.csv"
output_file_name = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombinedV3.csv"

key = '**ADD YOUR KEY HERE**'

#Get Addresses

assessmentSample20 = pandas.read_csv(input_file_name)
assessmentLite = assessmentSample20.loc[assessmentSample20['PROPERTYHOUSENUM'] != 0]
assessmentLite = assessmentLite.loc[assessmentSample20['addressFound'] == False]

print(len(assessmentLite))
addressList = []
for index, row in assessmentLite.iterrows():
   addressTempString = ""
   try:
      addressTempString = (str(int(row['PROPERTYHOUSENUM'])) + " " + str(row['PROPERTYADDRESS']) + " " + str(row['PROPERTYCITY']) + " " + str(row['PROPERTYSTATE']) + " " + str(int(row['PROPERTYZIP'])))
   except:
      addressTempString = (str(row['PROPERTYHOUSENUM']) + " " + str(row['PROPERTYADDRESS']) + " " + str(
         row['PROPERTYCITY']) + " " + str(row['PROPERTYSTATE']) + " " + str(row['PROPERTYZIP']))

   addressList.append([addressTempString, row['PARID']])


#Lookup Long+Lat

positionOfPropRawList = []

totalAPICalls = 0


def MakeAPICall(myAddress):

   address = myAddress[0]
   getReq = 'https://atlas.microsoft.com/search/address/json?api-version=1.0&subscription-key=' + key + '&query=' + address + ''

   global totalAPICalls
   totalAPICalls = totalAPICalls + 1
   if (totalAPICalls % 40 == 0):
      print(totalAPICalls)
   try:
      reqResult = requests.get(getReq)
      if (reqResult.status_code == 200):
         tempList = []
         tempList.append(reqResult.json()["results"][0]["position"]["lat"])
         tempList.append(reqResult.json()["results"][0]["position"]["lon"])
         tempList.append((reqResult.json()["results"][0]["type"] == "Point Address" or
                          reqResult.json()["results"][0]["type"] == "Address Range"))
         tempList.append(myAddress[1])
         positionOfPropRawList.append(tempList)
      else:
         positionOfPropRawList.append([0, 0, False, myAddress[1]])
   except:
      positionOfPropRawList.append([-1, -1, False, myAddress[1]])


print("Starting Step: " + str(datetime.datetime.now()))

#assessmentLite

with ThreadPoolExecutor(max_workers=4) as executor:
   for _ in executor.map(MakeAPICall, addressList):
      pass

print("Finishing Step: " + str(datetime.datetime.now()))




print(positionOfPropRawList)


#Cleaning up URL's

for addressPos in positionOfPropRawList:
   assessmentSample20.loc[assessmentSample20['PARID'] == addressPos[3],
                          ['latitude','longitude','addressFound']] = [addressPos[0],addressPos[1],addressPos[2]]

print(assessmentSample20)

assessmentSample20.to_csv(output_file_name, sep=',')

print("Finished")
