import csv
import json

#set parameters, taking them from the json configuration file:
with open("Parameters.json", "r") as read_file:
    data = json.load(read_file)
    probability_parameter = data["probability_parameter"]       #number of previous stati used to calculate the current status probabilities
    credibility_parameter = data["credibility_parameter"]       #numer of values from previous acquisitions used to calculate the current credibility of HR/RR (1=taken from the sensor, 0=imputated)
    wake_probability_load = data["wake_probability_load"]       #percentage load given to out-of-bed stati when calculate current status probabilities
    inputFile = data["inputFile"]
    outputFile = data["outputFile"]

#set the csv files to be read/written, with their filednames:
inputFieldnames = ('id', 'id_node', 'time_packet', 'timestamp', 'HR', 'RR', 'SV', 'HRV', 'SS', 'status', 'b2b', 'b2b1', 'b2b2')
outputFieldnames = ('id', 'id_node', 'time_packet', 'HR', 'HR_credibility', 'RR', 'RR_credibility', 'status', 'status_probability_out', 'status_probability_in', 'status_probability_mov')
with open(inputFile, mode = 'r') as i_File:
    with open(outputFile, mode = 'w', newline = '') as o_File:
        inputReader = csv.DictReader(i_File, fieldnames = inputFieldnames)
        outputWriter = csv.DictWriter(o_File, fieldnames = outputFieldnames, delimiter=',', quotechar='"', quoting = csv.QUOTE_ALL)

#global variables initialization:
        previous_stati = []                         #contains the previous stati used to calculate current status probabilities
        previous_HRs = []                           #contains the values from previous acquisitions used to calculate current credibility of HR
        for x in range(credibility_parameter):
            previous_HRs.append(1)
        previous_RRs = []                           #contains the values from previous acquisitions used to calculate current credibility of RR
        for x in range(credibility_parameter):
            previous_RRs.append(1)
        line_counter = 0                            #counter for data acquisition
        prev_HR = 0                                 #HR in the previous acquisition
        prev_RR = 0                                 #RR in the previous acquisition
        #outputWriter.writeheader()

#calculate output values for each line of input file:
        for row in inputReader:
            line_counter += 1

#first n inputs, to be ignored (n=probability_parameter):
            if line_counter <= probability_parameter:
                o_id = row['id']
                o_id_node = row['id_node']
                o_time_packet = row['time_packet']
                previous_stati.append(int(row['status']))
                o_status_probalility_out = ''
                o_status_probalility_in = ''
                o_status_probalility_mov = ''
                o_status = ''
                o_HR = ''
                o_HR_credibility = ''
                o_RR = ''
                o_RR_credibility = ''

#inputs starting from n+1:
            elif line_counter > probability_parameter:

#costant informations:
                o_id = row['id']
                o_id_node = row['id_node']
                o_time_packet = row['time_packet']

#status and probabilities:
                previous_stati.pop(0)
                previous_stati.append(int(row['status']))
                zero_sum = 0
                one_sum = 0
                two_sum = 0
                for x in previous_stati:
                    if x == 0:
                        zero_sum += 1
                    elif x == 1:
                        one_sum += 1
                    else:
                        two_sum += 1
                o_status_probalility_out = zero_sum / probability_parameter
                o_status_probalility_in = one_sum / probability_parameter
                o_status_probalility_mov = two_sum / probability_parameter
                if o_status_probalility_out > (wake_probability_load * (o_status_probalility_in + o_status_probalility_mov)):
                    o_status = 0
                elif int(row['status']) == 0:
                    o_status = 1
                else:
                    o_status = int(row['status'])

#HR, RR and credibilities:
                previous_HRs.pop(0)
                if o_status == 0:
                    o_HR = 0
                    previous_HRs.append(1)
                elif int(row['HR']) == 0:
                    o_HR = prev_HR
                    previous_HRs.append(0)
                else:
                    o_HR = int(row['HR'])
                    previous_HRs.append(1)
                prev_HR = o_HR
                if o_status == 0:
                    o_HR_credibility = 1
                else:
                    HRcredibility_sum = 0
                    for x in previous_HRs:
                        HRcredibility_sum += x
                    o_HR_credibility = HRcredibility_sum / credibility_parameter
                previous_RRs.pop(0)
                if o_status == 0:
                    o_RR = 0
                    previous_RRs.append(1)
                elif int(row['RR']) == 0:
                    o_RR = prev_RR
                    previous_RRs.append(0)
                else:
                    o_RR = int(row['RR'])
                    previous_RRs.append(1)
                prev_RR = o_RR
                if o_status == 0:
                    o_RR_credibility = 1
                else:
                    RRcredibility_sum = 0
                    for x in previous_RRs:
                        RRcredibility_sum += x
                    o_RR_credibility = RRcredibility_sum / credibility_parameter

#write results:
            outputWriter.writerow({'id': o_id, 'id_node': o_id_node, 'time_packet' : o_time_packet, 'HR' : o_HR, 'HR_credibility' : o_HR_credibility, 'RR' : o_RR, 'RR_credibility' : o_RR_credibility, 'status' : o_status, 'status_probability_out' : o_status_probalility_out, 'status_probability_in' : o_status_probalility_in, 'status_probability_mov' : o_status_probalility_mov})


