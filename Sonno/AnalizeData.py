import csv
import json
import time

currentSleep = 12400
currentAwakening = 37600

tStart = "2020-2-1 0:30:0"
tEnd = "2020-2-1 7:30:0"
start = time.strptime(tStart, "%Y-%m-%d %H:%M:%S")
end = time.strptime(tEnd, "%Y-%m-%d %H:%M:%S")

with open("Parameters.json", "r") as read_file:
    data = json.load(read_file)
    probability_parameter = data["probability_parameter"]
    credibility_parameter = data["credibility_parameter"]
    wake_probability_load = data["wake_probability_load"]
    inputFile = data["inputFile"]
    outputFile = data["outputFile"]

inputFilteredFile = outputFile
inputFieldnames = ('id', 'id_node', 'time_packet', 'HR', 'HR_credibility', 'RR', 'RR_credibility', 'status', 'status_probability_out', 'status_probability_in', 'status_probability_mov')
with open(inputFilteredFile, mode='r') as iFile:
    inputReader = csv.DictReader(iFile, fieldnames=inputFieldnames)

    lineCounter = 0
    rowSumTot = 0
    zeroSumTot = 0
    oneSumTot = 0
    twoSumTot = 0
    rowSum = 0
    zeroSum = 0
    oneSum = 0
    twoSum = 0
    HRcredibilitySum = 0
    RRcredibilitySum = 0
    prevStatus = 0
    awakenings = 0

    for row in inputReader:
        lineCounter += 1
        if lineCounter > probability_parameter:
#take inputs
            i_status = int(row['status'])
            i_HRcredibility = float(row["HR_credibility"])
            i_RRcredibility = float(row["RR_credibility"])
            i_time_packet = str(row["time_packet"])
            currentTime = time.strptime(i_time_packet, "%Y-%m-%d %H:%M:%S")
#update sums
            rowSumTot += 1
            if i_status == 0:
                zeroSumTot += 1
            elif i_status == 1:
                oneSumTot += 1
            else:
                twoSumTot += 1
            HRcredibilitySum += i_HRcredibility
            RRcredibilitySum += i_RRcredibility
            #if (currentSleep <= lineCounter <= currentAwakening):
            if (start <= currentTime <= end):
                rowSum += 1
                if i_status == 0:
                    zeroSum += 1
                elif i_status == 1:
                    oneSum += 1
                else:
                    twoSum += 1
                if ((prevStatus>0) and i_status==0):
                    awakenings += 1
                    print(lineCounter)
                prevStatus = i_status
#calculate percentages

    zeroTotPercentage = (zeroSumTot / rowSumTot) * 100
    oneTotPercentage = (oneSumTot / rowSumTot) * 100
    twoTotPercentage = (twoSumTot / rowSumTot) * 100
    zeroPercentage = (zeroSum/(rowSum))*100
    onePercentage = (oneSum/(rowSum))*100
    twoPercentage = (twoSum/(rowSum))*100
    HRcredibilityAVG = (HRcredibilitySum/rowSumTot)*100
    RRcredibilityAVG = (RRcredibilitySum / rowSumTot)*100
    print('Valid tot data: ', rowSumTot)
    print('zeroTotPercentage: ', zeroTotPercentage)
    print('oneTotPercentage: ', oneTotPercentage)
    print('twoTotPercentage: ', twoTotPercentage)
    print(' ')
    print('Valid data: ', rowSum)
    print('zeroPercentage: ', zeroPercentage)
    print('onePercentage: ', onePercentage)
    print('twoPercentage: ', twoPercentage)
    print('Awakenings: ', awakenings)
    print(' ')
    print('HRcredibilityAVG: ', HRcredibilityAVG)
    print('RRcredibilityAVG: ', RRcredibilityAVG)



