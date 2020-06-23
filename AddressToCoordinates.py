
import pandas
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor

pandas.set_option("display.max_columns", 60)
requests.Session().verify = False

input_file_name = "C:/Users/Commander/Downloads/DataSheets/assessmentOutput4Way-04-02.csv"
output_file_name = "C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part4-02.csv"

key = '**ADD YOUR KEY HERE**'


#Get Addresses

assessmentSample20 = pandas.read_csv(input_file_name)

assessmentLite = assessmentSample20[['PARID', 'PROPERTYHOUSENUM','PROPERTYADDRESS','PROPERTYCITY','PROPERTYSTATE','PROPERTYZIP','LOTAREA','FAIRMARKETLAND']]

addressList = []
for index, row in assessmentLite.iterrows():
   addressTempString = ""
   try:
      addressTempString = (str(int(row['PROPERTYHOUSENUM'])) + " " + str(row['PROPERTYADDRESS']) + " " + str(row['PROPERTYCITY']) + " " + str(row['PROPERTYSTATE']) + " " + str(int(row['PROPERTYZIP'])))
   except:
      addressTempString = (str(row['PROPERTYHOUSENUM']) + " " + str(row['PROPERTYADDRESS']) + " " + str(
         row['PROPERTYCITY']) + " " + str(row['PROPERTYSTATE']) + " " + str(row['PROPERTYZIP']))

   addressList.append(addressTempString)

#Lookup Long+Lat

positionOfPropRawList = []

totalAPICalls = 0


def MakeAPICall(address):
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
         tempList.append((reqResult.json()["results"][0]["type"] == "Point Address"))
         positionOfPropRawList.append(tempList)
      else:
         positionOfPropRawList.append([0, 0, False])
   except:
      positionOfPropRawList.append([-1, -1, False])


print("Starting Step: " + str(datetime.datetime.now()))

with ThreadPoolExecutor(max_workers=4) as executor:
   for _ in executor.map(MakeAPICall, addressList):
      pass

print("Finishing Step: " + str(datetime.datetime.now()))

print(positionOfPropRawList)


#Cleaning up URL's


assessmentLite['latitude'] = [rawPos[0] for rawPos in positionOfPropRawList ]
assessmentLite['longitude'] = [rawPos[1] for rawPos in positionOfPropRawList ]
assessmentLite['addressFound'] = [rawPos[2] for rawPos in positionOfPropRawList ]

print(assessmentLite)

#Output into new csv File



assessmentLite.to_csv(output_file_name, sep=',')

print("Finished")
