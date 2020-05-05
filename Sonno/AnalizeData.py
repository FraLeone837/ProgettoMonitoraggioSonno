import csv
import json
import time


def turnIntoHMS(decTime):
    hours = int(decTime)
    temp = 60 * (decTime - hours)
    minutes = int(temp)
    temp2 = 60 * (temp - minutes)
    seconds = int(temp2)
    time= str(hours)+'h '+str(minutes)+'m '+str(seconds)+'s'
    return time

#setting sleeping period
tStart = "2020-2-1 0:30:0"
tEnd = "2020-2-1 7:30:00"
start = time.strptime(tStart, "%Y-%m-%d %H:%M:%S")
end = time.strptime(tEnd, "%Y-%m-%d %H:%M:%S")

#take parameters
with open("Parameters.json", "r") as read_file:
    data = json.load(read_file)
    probability_parameter = data["probability_parameter"]
    credibility_parameter = data["credibility_parameter"]
    wake_probability_load = data["wake_probability_load"]
    inputFile = data["inputFile"]
    outputFile = data["outputFile"]

#open the input file
inputFilteredFile = outputFile
inputFieldnames = ('id', 'id_node', 'time_packet', 'HR', 'HR_credibility', 'RR', 'RR_credibility', 'status', 'status_probability_out', 'status_probability_in', 'status_probability_mov')
with open(inputFilteredFile, mode='r') as iFile:
    inputReader = csv.DictReader(iFile, fieldnames=inputFieldnames)

#global variables initialization
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

    print('Time of awekenings:')
    for row in inputReader:
        lineCounter += 1
        if lineCounter > probability_parameter:         #first n rows are empty (n=probability_parameter)

#take inputs
            i_status = int(row['status'])
            i_HRcredibility = float(row["HR_credibility"])
            i_RRcredibility = float(row["RR_credibility"])
            i_time_packet = str(row["time_packet"])
            currentTime = time.strptime(i_time_packet, "%Y-%m-%d %H:%M:%S")

#update global sums
            rowSumTot += 1
            if i_status == 0:
                zeroSumTot += 1
            elif i_status == 1:
                oneSumTot += 1
            else:
                twoSumTot += 1

            if (start < currentTime < end):
                rowSum += 1
                if i_status == 0:
                    zeroSum += 1
                elif i_status == 1:
                    oneSum += 1
                else:
                    twoSum += 1
                if ((prevStatus>0) and i_status==0):
                    awakenings += 1
                    print(currentTime.tm_year,'-',currentTime.tm_mon,'-',currentTime.tm_mday,' ',currentTime.tm_hour,':',currentTime.tm_min, sep='')
                prevStatus = i_status

                HRcredibilitySum += i_HRcredibility
                RRcredibilitySum += i_RRcredibility

#calculate percentages
    zeroTotPercentage = (zeroSumTot / rowSumTot)
    oneTotPercentage = (oneSumTot / rowSumTot)
    twoTotPercentage = (twoSumTot / rowSumTot)
    zeroPercentage = (zeroSum/rowSum)
    onePercentage = (oneSum/rowSum)
    twoPercentage = (twoSum/rowSum)
    HRcredibilityAVG = (HRcredibilitySum/rowSum)
    RRcredibilityAVG = (RRcredibilitySum / rowSum)

    print('\nNumber of awakenings: ',awakenings)
    print('')
    print('Total data: ', rowSumTot, ' (', turnIntoHMS(rowSumTot/3600), ')', sep='')
    print('zero total percentage: ', zeroTotPercentage*100, ' (',turnIntoHMS(rowSumTot*zeroTotPercentage/3600),')', sep='')
    print('one total percentage: ', oneTotPercentage*100, ' (',turnIntoHMS(rowSumTot*oneTotPercentage/3600),')', sep='')
    print('two total percentage: ', twoTotPercentage*100, ' (',turnIntoHMS(rowSumTot*twoTotPercentage/3600),')\n', sep='')
    print('Sleeping phase data): ', rowSum, ' (',turnIntoHMS(rowSum/3600),')', sep='')
    print('zero percentage: ', zeroPercentage*100, ' (',turnIntoHMS(rowSum*zeroPercentage/3600),')', sep='')
    print('one percentage: ', onePercentage*100, ' (',turnIntoHMS(rowSum*onePercentage/3600),')', sep='')
    print('two percentage: ', twoPercentage*100, ' (',turnIntoHMS(rowSum*twoPercentage/3600),')\n', sep='')
    print('HRcredibilityAVG: ', HRcredibilityAVG*100)
    print('RRcredibilityAVG: ', RRcredibilityAVG*100)


