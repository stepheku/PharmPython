import urllib.request
import urllib
import filecmp
import subprocess
import os.path
import re
import datetime
import csv

downloadPage = []
logFileName = 'log.csv'
pdfFileName = ''
filePath = os.path.dirname(os.path.abspath(__file__))
logFileName = filePath+'/'+logFileName
cdcVisUrl = 'http://www.cdc.gov/vaccines/hcp/vis/'
cdcVisReq = urllib.request.Request(cdcVisUrl)#,None,headers)
cdcVisResp = urllib.request.urlopen(cdcVisReq)
cdcVisRespData = cdcVisResp.read()
cdcVisLinks = re.findall(r'/vaccines/hcp/vis/vis-statements/(.*?)"',str(cdcVisRespData))
modifiedPage = []

if os.path.isfile(filePath+logFileName) == False:
     subprocess.call(["touch",logFileName])
if os.path.exists(filePath+'/lib/') == False:
     subprocess.call(["mkdir",filePath+"/lib"])
def writeLogEntry():
      with open(logFileName,'a') as f:
          writer = csv.writer(f,delimiter=',')
          writer.writerow([pdfFileName,datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")])
          f.close()    
      modifiedPage.append(pdfFileName)
for link in cdcVisLinks:
     visPageUrl = 'http://www.cdc.gov/vaccines/hcp/vis/vis-statements/' + link
     visPageReq = urllib.request.Request(visPageUrl)
     visPageResp = urllib.request.urlopen(visPageReq)
     visPageRespData = visPageResp.read()
     downloadPage = re.findall(r'href="/vaccines/hcp/vis/vis-statements/(.*?.pdf)"',str(visPageRespData))
     downloadLink = 'http://www.cdc.gov/vaccines/hcp/vis/vis-statements/' + downloadPage[0]
     urllib.request.urlretrieve(downloadLink,downloadPage[0]) # Download VIS PDF
     pdfFileName = downloadPage[0]
     if os.path.isfile(filePath+'/lib/'+downloadPage[0]) == True:
          #print downloadPage[0],'File exists in ./lib/ folder'
          if filecmp.cmp(downloadPage[0],filePath+'/lib/'+downloadPage[0]) == True:
               subprocess.call(["rm",downloadPage[0]])
          elif filecmp.cmp(downloadPage[0],filePath+'/lib/'+downloadPage[0]) == False:
               subprocess.call(["mv",downloadPage[0],filePath+'/lib/'])
               writeLogEntry()
     else:
          #print downloadPage[0],'File does not exist in ./lib/ folder'
          subprocess.call(["mv",downloadPage[0],'./lib/'])
          writeLogEntry()
