import datetime

import geopandas
import matplotlib
import pandas

pandas.set_option('display.max_columns', None)

print("Start: " + str(datetime.datetime.now()))

CensusShapeFile = "C:/Users/Commander/Downloads/DataSheets/tl_2019_42_tabblock10/tl_2019_42_tabblock10.shp"
PGHShapeFile = "C:/Users/Commander/Downloads/DataSheets/AlleganyCountyFullAssesment/AlleganyCountyFullAssesmentV5.shp"

PA_Map = geopandas.read_file(PGHShapeFile)
PGH_Map = PA_Map.loc[PA_Map['COUNTYFP10'] == '003']

PGH_Map['LCostPerLand'] = 0
PGH_Map['TCostPerLand'] = 0

for index, row in PGH_Map.iterrows():
    if PGH_Map['TAP_Land'][index] > 0:
        PGH_Map['LCostPerLand'][index] = PGH_Map['TAP_LValue'][index] / PGH_Map['TAP_Land'][index]
        PGH_Map['TCostPerLand'][index] = PGH_Map['TAP_TValue'][index] / PGH_Map['TAP_Land'][index]

ax = PGH_Map.plot(figsize=(10,10), zorder=1, column='LCostPerLand', legend=True, legend_kwds={'label': "Price Per Land Unit"})


matplotlib.pyplot.show()

print("Finish: " + str(datetime.datetime.now()))
