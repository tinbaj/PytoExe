import time
import sys
import json
import Packages
import math
from myApp import myApp

start_time = time.perf_counter()
Logger = Packages.LoggerDetails()
log = Logger.setLogger()
inputDict = {}
errorFlag = False
if sys.argv[1]:
    funcName = sys.argv[1]
    inputDict["funcName"] = funcName
else:
    log.error("Value not Specified for Parsing Type (TXT/XML/CSV")
    errorFlag = True

if sys.argv[2]:
    fileName = sys.argv[2]
    inputDict["fileName"] = fileName
else:
    log.error("Value not Specified for File Name for Parsing")
    errorFlag = True

if sys.argv[3]:
    inputParams = open(sys.argv[3]).read()
    data_inputParams = json.loads(inputParams)
    inputDict["funcInput"] = data_inputParams
else:
    log.error("Value not Specified for json file containing parsing parameters")
    errorFlag = True


for k,v in inputDict.items():
    print('{0} : {1}'.format(k,v))

if not errorFlag:
    MA = myApp()
    MA.main(**inputDict)
end_time = time.perf_counter()

print("Start Time: ",round(start_time,2))
print("End Time: ",round(end_time,2))
print("Time taken for Parsing: ",end_time-start_time)