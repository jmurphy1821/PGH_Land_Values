import datetime
import math
from collections import defaultdict

import geopandas
import pandas
import shapely
import shapely.geometry
from shapely.geometry import MultiPoint


def IsPropertyInBlock(propertyLong, propertyLat, blockShape):
    propertyPoint = shapely.geometry.Point(propertyLong,propertyLat)
    return blockShape.contains(propertyPoint)

def AddAllHashSquares(shapePolygon, shapeGeoID, index):
    ajustedBounds = [(math.floor(shapePolygon.bounds[0] * 100)/100),
                     (math.floor(shapePolygon.bounds[1] * 100)/100),
                     (math.ceil(shapePolygon.bounds[2] * 100)/100),
                     (math.ceil(shapePolygon.bounds[3] * 100)/100)]

    totalXSquares = int((ajustedBounds[0] - ajustedBounds[2]) * -100) + 1
    totalYSquares = int((ajustedBounds[1] - ajustedBounds[3]) * -100) + 1

    for xSquare in range(totalXSquares):
        for ySquare in range(totalYSquares):
            localSquare = shapely.geometry.Polygon([(ajustedBounds[0] + (0.01*xSquare), ajustedBounds[1] + (0.01*ySquare)),
                                         (ajustedBounds[0] + (0.01*xSquare), (ajustedBounds[1] + (0.01*ySquare) + 0.01)),
                                         ((ajustedBounds[0] + (0.01*xSquare) + 0.01), (ajustedBounds[1] + (0.01*ySquare) + 0.01)),
                                         ((ajustedBounds[0] + (0.01*xSquare) + 0.01), ajustedBounds[1] + (0.01*ySquare))])

            if(shapePolygon.intersects(localSquare)):
                hashVal = GetCordinateHash(ajustedBounds[0] + (0.01*xSquare),(ajustedBounds[1] + (0.01*ySquare)))

                dictionaryOfShapes[hashVal].append([shapePolygon,shapeGeoID,index])

                if (shapeGeoID == '420030201001024'):
                    print("ShapeBound = " + str(shapePolygon.bounds))
                    print("AjustBound = " + str(ajustedBounds))
                    print("TotalSquares (X,Y) = (" + str(totalXSquares) + "," + str(totalYSquares) + ")")
                    print("Squares (X,Y) = (" + str(xSquare) + "," + str(ySquare) + ")")
                    print(localSquare)
                    print(str(ajustedBounds[0] + (0.01*xSquare)) + ":" + str(ajustedBounds[1] + (0.01*ySquare)))
                    print(hashVal)
                    print(dictionaryOfShapes[hashVal])


def GetCordinateHash(lonX, latY):
    return format(lonX, '.2f') + "," + format(latY,'.2f')

pandas.set_option('display.max_columns', None)

print("Start: " + str(datetime.datetime.now()))

CensusShapeFileName = "C:/Users/Commander/Downloads/DataSheets/AlleganyCounty/AlleganyCounty.shp"
AssessmentFileName = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombinedV4.csv"
outputFileName = "C:/Users/Commander/Downloads/DataSheets/AlleganyCountyFullAssesment/AlleganyCountyFullAssesmentV5.shp"
dictionaryOfShapes = defaultdict(list)

MapFile = geopandas.read_file(CensusShapeFileName)
AssessmentFile = pandas.read_csv(AssessmentFileName)
MapFile['TAP_LValue'] = 0
MapFile['TAP_BValue'] = 0
MapFile['TAP_TValue'] = 0
MapFile['TAP_Land'] = 0

print(len(AssessmentFile))
AssessmentFile = AssessmentFile.loc[AssessmentFile['addressFound'] == True]
print(len(AssessmentFile))

print("NumRows1: " + str(len(MapFile.index)))
print("NumRows2: " + str(len(AssessmentFile.index)))

#--------------------------------------------------------------------
#Set up HashSquares
print("Starting HashSquares: " + str(datetime.datetime.now()))


for index, mapRow in MapFile.iterrows():
    AddAllHashSquares(mapRow['geometry'], mapRow['GEOID10'], index)

print("Finished HashSquares: " + str(datetime.datetime.now()))

#--------------------------------------------------------------------

for index, currentProp in AssessmentFile.iterrows():
    if index % 300 == 0:
        print(index)
    currentPropHash = GetCordinateHash(math.floor(currentProp.loc['longitude'] * 100) / 100,
                                       math.floor(currentProp.loc['latitude'] * 100) / 100)
    if (currentPropHash in dictionaryOfShapes):
        for shape in dictionaryOfShapes[currentPropHash]:
            if IsPropertyInBlock(currentProp.loc['longitude'], currentProp.loc['latitude'], shape[0]):
                addedLand = currentProp.loc['LOTAREA']
                addedValue = currentProp.loc['FAIRMARKETLAND']
                addedBuilding = currentProp.loc['FAIRMARKETBUILDING']
                addedTotal = currentProp.loc['FAIRMARKETTOTAL']
                MapFile.loc[[shape[2]], ['TAP_LValue', 'TAP_Land', 'TAP_BValue', 'TAP_TValue']] = [
                    (MapFile.loc[shape[2]].at['TAP_LValue'] + addedValue),
                    (MapFile.loc[shape[2]].at['TAP_Land'] + addedLand),
                    (MapFile.loc[shape[2]].at['TAP_BValue'] + addedBuilding),
                    (MapFile.loc[shape[2]].at['TAP_TValue'] + addedTotal)]
                break

MapFile.to_file(outputFileName)

print("Finish: " + str(datetime.datetime.now()))

