import urllib.request
import filecmp
import subprocess
import os.path
import re
import sys
import datetime
import csv

downloadPage = []
logFileName = 'log.csv'
pdfFileName = ''
currentFilePath = os.path.dirname(os.path.abspath(__file__))
logFileName = os.path.join(currentFilePath,'log.csv')
modifiedPage = []

def getVisLinks():
    try:
        cdcVisUrl = 'http://www.cdc.gov/vaccines/hcp/vis/current-vis.html'
        cdcVisReq = urllib.request.Request(cdcVisUrl)
        cdcVisResp = urllib.request.urlopen(cdcVisReq)
        cdcVisRespData = cdcVisResp.read()
        cdcVisLinks = re.findall(r'/vaccines/hcp/vis/vis-statements/(.*?)"',str(cdcVisRespData))
        if not cdcVisLinks:
            sys.exit("Regular expession did not find vis-statements on the URL: {}".format(cdcVisUrl))
        else:
            return cdcVisLinks
    except urllib.request.URLError as e:
        sys.exit("There is an issue with the URL: {}".format(cdcVisUrl))

def checkLogAndLibExists(filePath, logFile):
    if os.path.isfile(filePath+logFile) == False:
        subprocess.call(["touch",logFile])
    if os.path.exists(filePath+'/lib/') == False:
        subprocess.call(["mkdir",filePath+"/lib"])

def writeLogEntry(logFile, contents):
    with open(logFile,'a') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerow(contents)
        f.close()

def main():
    cdcVisLinks = getVisLinks()
    global modifiedPage
    for link in cdcVisLinks:
         visPageUrl = 'http://www.cdc.gov/vaccines/hcp/vis/vis-statements/' + link
         visPageReq = urllib.request.Request(visPageUrl)
         visPageResp = urllib.request.urlopen(visPageReq)
         visPageRespData = visPageResp.read()
         downloadPage = re.findall(r'href="/vaccines/hcp/vis/vis-statements/(.*?.pdf)"',str(visPageRespData))
         downloadLink = 'http://www.cdc.gov/vaccines/hcp/vis/vis-statements/' + downloadPage[0]
         urllib.request.urlretrieve(downloadLink,downloadPage[0]) # Download VIS PDF
         pdfFileName = downloadPage[0]
         if os.path.isfile(currentFilePath+'/lib/'+downloadPage[0]) == True:
              #print downloadPage[0],'File exists in ./lib/ folder'
              if filecmp.cmp(downloadPage[0],currentFilePath+'/lib/'+downloadPage[0]) == True:
                   subprocess.call(["rm",downloadPage[0]])
              elif filecmp.cmp(downloadPage[0],currentFilePath+'/lib/'+downloadPage[0]) == False:
                   subprocess.call(["mv",downloadPage[0],currentFilePath+'/lib/'])
                   modifiedPage.append(pdfFileName)
                   writeLogEntry(logFileName, [pdfFileName,datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")])
         else:
              #print downloadPage[0],'File does not exist in ./lib/ folder'
              subprocess.call(["mv",downloadPage[0],'./lib/'])
              modifiedPage.append(pdfFileName)
              writeLogEntry(logFileName, [pdfFileName,datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")])

if __name__ == "__main__":
    checkLogAndLibExists(currentFilePath, logFileName)
    main()
