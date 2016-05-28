#!/usr/bin/python

from lxml import etree, html
import os
import csv
from textblob.classifiers import NaiveBayesClassifier

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__),'Results2')


def parseNavigator():
    doc = html.parse(os.path.join(TEST_DIRECTORY,'Navigator.html'))
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

def getTestcasefailure(tcdoc):
    failure = tcdoc.xpath("(.//div[@class='TestItemOutcome Failed'])[1]/ancestor::div[1]/div/text()")
    return ''.join(failure)

def updateCsv():
    return True

def startParse():
    return True


if __name__ == "__main__":
    print "analysing report"
    parseNavigator()
