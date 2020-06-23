import pandas

#pandas.set_option("display.max_columns", 60)
input_file_name = "C:/Users/Commander/Downloads/DataSheets/AllAssessmentsCombined.csv"

output_file_name = "C:/Users/Commander/Downloads/DataSheets/outputDownTown.csv"

print("Start")
assessmentFull = pandas.read_csv(input_file_name)
print(assessmentFull['PROPERTYZIP'].value_counts())


MtOliverValues = assessmentFull.loc[assessmentFull['PROPERTYZIP'] == 15222]
print(MtOliverValues)
MtOliverValues.to_csv(output_file_name, sep=',')