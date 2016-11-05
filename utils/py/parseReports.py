#!/usr/bin/python

from lxml import etree, html
import os
import csv
from textblob.classifiers import NaiveBayesClassifier
import re

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__),'Results2')
tcCount=0
moduleName=None

def parseNavigator():
    try:
        doc = html.parse(os.path.join(TEST_DIRECTORY,'Navigator.html'))
    except Exception,e:
        print(e)
        return

    modules = doc.xpath("//h3[text()='Results']/following-sibling::ul//li[text()='tests']/ul/li")
    csvfile = open('results.csv','wb')
    csvWriter = csv.writer(csvfile, delimiter=",", 
            quotechar="|", quoting=csv.QUOTE_MINIMAL)
    # Write the column names
    csvWriter.writerow(["#","Module","TestCase","Result","FailureReason","FailureType"])
    with open('train.csv','r') as trdata:
        cl = NaiveBayesClassifier(trdata, format="csv")
    tcCount=0
    for module in modules:
        moduleName = module.xpath("./text()")[0]

        tc_lnks = module.xpath(".//li[contains(@class,'TestCaseImpl')]")
        for tc in tc_lnks:
            tchref = tc.xpath("./a/@href")[0]
            tcName = tc.xpath("./a/text()")[0]
            tcresulttext = "pass" if "Successful" in tc.xpath("./@class")[0] else "fail"
            failure = ''
            failureType=''
            if tcresulttext == "fail":
                tcdoc = html.parse(os.path.join(TEST_DIRECTORY, tchref))
                failure = getTestcasefailure(tcdoc)
                failure = failure.replace(",",";")
                #import ipdb; ipdb.set_trace() # BREAKPOINT


            tcCount+=1

            # TODO: write to file only if test case name matches a pattern
            if "TC" in tcName:
                if failure:
                    clsfy = cl.classify(failure)
                else:
                    clsfy = ''

                csvWriter.writerow([tcCount, moduleName, tcName, tcresulttext, failure.replace("\r",""), clsfy])
    return True

def getTestcasefailure(tcdoc):
    failure = tcdoc.xpath("(.//div[@class='TestItemOutcome Failed'])[1]/ancestor::div[1]/div/text()")
    if failure:
        return ''.join(failure)

def updateCsv():
    return True

def startParse():
    return True

def searchTests(d=None):
    print("trying alternate method of searching test cases ", d)
    if d is None:
        d = os.path.join(TEST_DIRECTORY)
    print("training the classifier.....")
    with open('train.csv','r') as trdata:
        cl = NaiveBayesClassifier(trdata, format="csv")
    csvfile = open('results.csv','wb')
    csvWriter = csv.writer(csvfile, delimiter=",", 
            quotechar="|", quoting=csv.QUOTE_MINIMAL)

    print("recording test case results.... ")
    recordTCsResult(d, csvWriter, cl)

    csvfile.close()

def recordTCsResult(d, csvWriter, cl):
    for item in os.listdir(d):
        itempath = os.path.join(d, item)
        global moduleName
        if os.path.isdir(itempath):
            recordTCsResult(itempath, csvWriter, cl)
        else:
            if "TC" in item and ".testcase.html" in item:
                # print " > test case", item
                # extract the Module Name using re
                patrn = ".*tests(.*)(TestScenarios|Test Scenarios).*"
                moduleName_raw = re.match(patrn, itempath)
                if moduleName_raw:
                    moduleName = moduleName_raw.groups()[0].replace("\\","")
                else:
                    moduleName = ''
                tcdoc = html.parse(itempath)
                result = "pass"
                clsfy = ''
                failure = getTestcasefailure(tcdoc)
                if failure:
                    failure = failure.replace(",",";")
                    failure = failure.replace("\r","")
                    clsfy = cl.classify(failure)
                    result = "fail"
                global tcCount
                tcCount += 1
                csvWriter.writerow([tcCount, moduleName, item, result, failure, clsfy])


if __name__ == "__main__":
    print "analysing report"
    if not parseNavigator():
        searchTests()
