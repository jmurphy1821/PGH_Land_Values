# PGH_Land_Values
Pittsburgh Land Value Map

General Idea
1.	Get an assessment file with all the addresses in your county
2.	Use “Separate Zip Codes” to create a bunch of smaller manageable files
3.	Run “AddressToCoordinates” for each of the smaller files
4.	Use “MergeFiles” to combine it into one large complete assessment file
5.	Run “CombineLandValues” to get the shape file with all the total costs
6.	Run “PittsburghMap” with that shape file and display what the land values look like

AddressToCoordinates
	This Takes in a list of addresses (assessment files) and outputs the coordinates of the addresses 
1.	Input files set up
2.	Azure Maps Key (Add your own)
3.	Address Queries are created
4.	API Calls are made to Azure by using thread pools (4 workers work the best)
5.	The Coordinates are added into the data frame 
6.	The data frame is written to a CSV file

AddressToCoordinatesRefinement
	It’s the same as AddressToCoordinates
	Only difference is this takes only the ones that failed
  
CombineLandValues
	This Combines the Census shape file with the Property Coordinates to produce the final shape 	file with the accounted land area as well as total land value and total value of the block
1.	Input files are created
2.	“Hash Squares” are created
-	Hash square are all the block in 0.01 x 0.01 area (usually about a few hundred blocks) 
3.	All the properties are run through, the coordinates are hashed then the corresponding shape which it is contained in has the property land and prices added to it
4.	The map file is output

CombineWithAssessment
	Used for adding in columns that where missed in the coordinate csv files
  
MergeFiles
	Merges multiple csv files into one file
  
MtOliverSelector
	This Takes an input file and creates an output of only one zip code
	NOTE: zip code can be modified for any value
  
PittsburghMap
	This is the actual script you run to display the map of the land values
1.	The shape files are added
2.	The land value ($) per unit is calculated
3.	The Map is then displayed

SeperateZipCodes
	Splits up a large assessment file into multiple smaller files
		(makes running the Azure Maps more bite sized)
	Individual zip codes are separated by occurrence then distributed throughout the new files
  
TestGetShapeMatch
	Used for testing which census block contains a point
  
TestScratchPad
	Used for cleaning up some files
