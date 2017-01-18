#!/usr/bin/python
import csv
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import threading
import Queue

# assuming that I am on Windows
uhome = os.path.expanduser("~")
ffprofile_path = os.path.join(
        uhome, "AppData", "Roaming", "Mozilla" ,
        "Firefox", "Profiles", "p26q9tvw.dev")

# required FF binary version is installed as per below target path
binary_path = os.path.abspath(
        os.path.join(uhome, "firefoxes\\35.5\\firefox.exe"))
ffbinary = FirefoxBinary(firefox_path=binary_path)

# content types found using HTTP Headers that can be downloaded
content_types = [
'image/png',
'application/octet-stream',
'application/zip',
'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
'application/vnd.ms-excel',
'text/html',
'text/csv',
'image/jpeg',
'audio/mpeg',
'video/mp4',
'application/pdf',
'application/vnd.ms-powerpoint',
'application/vnd.openxmlformats-officedocument.presentationml.presentation',
'application/vnd.openxmlformats-officedocument.presentationml.template',
'image/tiff',
'application/vnd.visio',
'application/msword',
'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'application/xml',
'application/x-unknown',
]

# below map is for reference
"""
content_types_map={
'png': 'image/png',
'unknown': 'application/octet-stream',
'zip': 'application/zip',
'excel_x': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
'excel': 'application/vnd.ms-excel',
'html': 'text/html',
'htm': 'text/html',
'csv': 'text/csv',
'jpg': 'image/jpeg',
'mp3': 'audio/mpeg',
'mp4': 'video/mp4',
'pdf': 'application/pdf',
'power_point': 'application/vnd.ms-powerpoint',
'power_point_x': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
'power_point_t': 'application/vnd.openxmlformats-officedocument.presentationml.template',
'tif': 'image/tiff',
'visio': 'application/vnd.visio',
'word': 'application/msword',
'word_x': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
'xml': 'application/xml',
}
"""
app_url = 'https://login.salesforce.com'
browser_list = []
browser_obj_map = {}
download_to = os.getcwd()

class FileThread(threading.Thread):
    def __init__(self, file_Id, fileName, sharedwithtext):
        threading.Thread.__init__(self)
        self.file_Id = file_Id
        self.fileName = fileName
        self.download_path = os.path.join(download_to,"sforcedownloads")
        self.tgt_path = os.path.join(self.download_path, file_Id)
        self.file_download_path = os.path.join(self.download_path, self.fileName)
        self.sharedwithtext = sharedwithtext

    def run(self):
        while self.downloading():
            time.sleep(1)
        # as soon as the downloading is over return
        self._ensure_path(self.tgt_path)
        files = os.listdir(self.download_path)
        actual_files = [f for f in files if self.fileName in f]
        if len(actual_files)>1:
            print("found more files even after waiting for download", ','.join(actual_files))

        actual_file = [f for f in actual_files if ".part" not in f]
        if not os.path.exists(os.path.join(self.tgt_path, actual_file[0])):
            shutil.move(
                    os.path.join(
                        self.download_path, actual_file[0]
                        ), self.tgt_path
                    )

            # write the shared with info to a file
            outfile = open(os.path.join(self.tgt_path,'sharedwith.txt'), 'wb')
            outfile.writelines(self.sharedwithtext)
            outfile.close()

            # clean up the current download
            archive_path = os.path.join(os.path.dirname(self.download_path), 
                    "download_archive")
            self._ensure_path(archive_path)
            shutil.move(self.tgt_path, archive_path)

        return True

    def downloading(self):
        return os.path.exists(
                os.path.join(
                    self.download_path, self.fileName+".part"
                    )
                )

    def _ensure_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

class Browser():
    def __init__(self):
        self.profile = FirefoxProfile()
        self.profile.set_preference("browser.download.folderList",2)
        self.profile.set_preference(
                "browser.download.manager.showWhenStarting",False
                )
        self.download_path = os.path.join(download_to, "sforcedownloads")
        self._ensure_path(self.download_path)
        self.profile.set_preference("browser.download.dir", self.download_path)
        self.profile.set_preference(
                "browser.helperApps.neverAsk.saveToDisk", ','.join(content_types)
                )
        self.binary = FirefoxBinary(firefox_path=binary_path)
        self.driver = webdriver.Firefox(
                firefox_profile=self.profile, firefox_binary=self.binary
                )
        self.threadfilenames= []
        self.filesinprogress = []
        self._login()

    def _ensure_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _login(self):
        self.driver.get(app_url)
        username = 'salesforceusername'
        password = 'xxxxx'
        self.driver.find_element_by_id('username').send_keys(username)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('Login').click()
        Hometab = WebDriverWait( self.driver, 20 ).until(
                EC.presence_of_element_located((By.LINK_TEXT,'Home')))

        Hometab.click()
        # just after login prepare note down the url
        self.baseUrl = self.driver.current_url
        print ("Downloading all that is there in the csv.")

    def navigate_to_file(self, file_Id):
        fileUrl = self.baseUrl
        fileUrl = fileUrl.replace("home/home.jsp","")
        fileUrl += file_Id
        # navigating to the file in the browser
        self.driver.get(fileUrl)


    def start_download(self, file_Id):
        if file_Id:
            self.navigate_to_file(file_Id)
            try:
                # wait for the download link to appear
                download_link = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//a[contains(@title,'Download')]")
                            )
                        )
                # file title - browser downloads the file with the same name
                fileName = self.driver.find_element_by_id("fileTitle").text.strip()

                screenshot_path = os.path.join(self.download_path, file_Id)
                # take the screenshot
                self._ensure_path(screenshot_path)
                self.driver.get_screenshot_as_file(
                        os.path.join(screenshot_path, fileName+".jpg")
                        )
                download_link.click()
                # import ipdb;ipdb.set_trace()
                # noting down addtional info about the file from the UI
                sharewithdiv = self.driver.find_element_by_xpath(
                        "//div[contains(@class,'sharedWithSummaryList')]"
                        )

                self._prepare_and_wait_for_download(
                        file_Id, fileName, sharewithdiv.text
                        )

            except Exception, e:
                print(e)

    def _prepare_and_wait_for_download(self, file_Id, fileName, sharedwithtext):
        files = os.listdir(self.download_path)
        time.sleep(30) # waiting for 30 seconds for every file
        actual_files = [f for f in files if fileName in f]
        if len(actual_files)>1: # possibly the download is still in progress
            print("found more files after 30 seconds", ','.join(actual_files))

        # if the file is not already downloaded/getting downloaded
        if fileName not in self.threadfilenames:
            filethread = FileThread(file_Id, fileName, sharedwithtext)
            filethread.start()
            self.filesinprogress.append(filethread)
            self.threadfilenames.append(fileName)

    # close all file downloading threads
    def close(self):
        for t in self.filesinprogress:
            t.join()
        self.driver.close()
        self.driver.quit()



def main():
    browser = Browser() # need to do in single login
    with open('All_files100.csv','rb') as inputfile:
        fileid_rows = csv.reader(inputfile)
        for row in fileid_rows:
            file_Id = row[0].strip()
            browser.start_download(file_Id)

    if browser:
        browser.close()

    print ("Completed the download.... .")

if __name__ == "__main__":
    main()
