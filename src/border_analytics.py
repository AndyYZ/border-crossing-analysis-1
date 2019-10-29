import csv
import operator
import sys, os

from decimal import Decimal, getcontext, ROUND_HALF_UP
dc = getcontext()
dc.rounding = ROUND_HALF_UP
'''
Example showed in the original problem use ROUND_HALF_UP
round(10.5) = 11 while the default round(10.5) = 10
'''

def main():
    '''
    To call this funciotn, run run.sh in the 
    parent folder /border_crossling_analysis-1 
    bash run.sh 

    This funcion reads a input file as in run.sh
    with format
    https://github.com/ivboh/border-crossing-analysis-1/blob/master/insight_testsuite/tests/test_1/input/Border_Crossing_Entry_Data.csv


    Outputs a file as in run.sh 
    Summarize the monthly total and the trailing month average
    for difference border, states, date and measure.
    For detailed description of the problem please see
    https://github.com/InsightDataScience/border-crossing-analysis
    '''
    inputFileName = os.getcwd()+sys.argv[1][1:]
    outputFileName = os.getcwd()+sys.argv[2][1:]
    
    #Sum up the monthly total value for each combination
    # of state, month and measure 
    d={}
    with open(inputFileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            border = row[3]
            date = row[4]
            month = date_to_month(date)
            measure = row[5]
            value = int(row[6])
            k = (border, measure, date, month)
            if k in d:
                d[k] = (d[k][0]+value, 0)
            elif not k in d:
                d[k] = (value, 0)


    # Sort the date under each combination of
    # state and measure, and compute the trailing
    # monthly average.
    set_border_measure = set(k[0:2] for k in d)
    for b_m in set_border_measure:
       keys_by_border_measure = [k for k in d if k[0:2] == b_m]
       keys_by_border_measure.sort(key = operator.itemgetter(3))
       sum_of_value = 0
       for i in range(len(keys_by_border_measure)):
            v = d[keys_by_border_measure[i]][0]
            if i>0:
                average = round(Decimal(sum_of_value/i),0)
                sum_of_value += v
            else:
                average = 0
                sum_of_value = v
            d[keys_by_border_measure[i]] = (v, average)


    #Print the result to the output file       
    list_k_v = [[*k, *v] for k,v in d.items()]
    list_k_v.sort(key = operator.itemgetter(3,4,1,0),reverse = True)

    outputfile = open(outputFileName, 'w')
    outputfile.write('Border,Date,Measure,Value,Average\n')
    for ele in list_k_v:
        ele = [str(i) for i in ele]
        del ele[3]
        ele[1], ele[2] = ele[2],ele[1]
        outputfile.write(','.join(ele))
        outputfile.write('\n')
    outputfile.close()

def date_to_month(date): 
    '''
    This function takes date in the input csv file
    and return a month as integer for
    sorting the date.
    for example input  03/01/2019 12:00:00 AM
    returns 2019*12+03
    '''
    l = date.split(" ")
    [month, day, year] = l[0].split("/")
    return (int(year)*12+int(month))


if __name__ == "__main__":
    main()    
