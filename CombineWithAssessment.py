import datetime

import pandas

pandas.set_option('display.max_columns', None)
#geopandas.set_option("display.max_columns", 60)

print("Start: " + str(datetime.datetime.now()))


inputFileName = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombinedV3.csv"
inputAssessmentName = "C:/Users/Commander/Downloads/DataSheets/assessments.csv"
output_file_name = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombinedV4.csv"

inputFile = pandas.read_csv(inputFileName)
inputAssessment = pandas.read_csv(inputAssessmentName)

inputAssessment = inputAssessment[['PARID', 'FAIRMARKETBUILDING', 'FAIRMARKETTOTAL']]

#inputFile['FAIRMARKETBUILDING'] = 0
#inputFile['FAIRMARKETTOTAL'] = 0

print(inputFile.head())

inputFile = inputFile.join(inputAssessment.set_index('PARID'), on='PARID')

print(inputFile.head())

inputFile = inputFile[['PARID','PROPERTYHOUSENUM','PROPERTYADDRESS','PROPERTYCITY','PROPERTYSTATE','PROPERTYZIP',
                       'LOTAREA','FAIRMARKETBUILDING','FAIRMARKETLAND','FAIRMARKETTOTAL',
                       'latitude','longitude','addressFound']]


print(inputFile.head())

inputFile.to_csv(output_file_name, sep=',')

print("Finish: " + str(datetime.datetime.now()))

