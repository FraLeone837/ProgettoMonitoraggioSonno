import json

parameters = {
    "probability_parameter" : 120,
    "credibility_parameter" : 10,
    "wake_probability_load": 0.8,
    "inputFile" : "31-01febbraio.csv",
    "outputFile" : "FilteredBedSensorData.csv"
}
toWrite = json.dumps(parameters, indent=4)

with open("Parameters.json", "w") as parameters_file:
    parameters_file.write(toWrite)





