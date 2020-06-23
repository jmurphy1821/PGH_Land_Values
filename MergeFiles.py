import pandas
import requests
import json
import geopandas
from geopandas import read_file
import matplotlib
import descartes
import fiona
import shapely
from shapely.geometry import MultiPoint
import http.client
import socket
import datetime
from concurrent.futures import ThreadPoolExecutor

#pandas.set_option('display.max_columns', None)
#geopandas.set_option("display.max_columns", 60)

print("Start: " + str(datetime.datetime.now()))

fileIn = []

fileIn.append("C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part1.csv")
fileIn.append("C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part2.csv")
fileIn.append("C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part3.csv")
fileIn.append("C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part4-01.csv")
fileIn.append("C:/Users/Commander/Downloads/DataSheets/assessmentsOutput-Part4-02.csv")
fileIn.append("C:/Users/Commander/Downloads/DataSheets/output-MtOliverV2.csv")

outputFile = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombined2.csv"

pandasFilesIn = []
for fileName in fileIn:
    pandasFilesIn.append(pandas.read_csv(fileName))

result = pandas.concat(pandasFilesIn, ignore_index=True)
print(result)

result.to_csv(outputFile, sep=',')

print("Finish: " + str(datetime.datetime.now()))

