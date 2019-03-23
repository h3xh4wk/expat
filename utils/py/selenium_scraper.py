#!/usr/bin/env python
import os

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *

import shutil
import time

class Scraper:
    """ A Simple Scraper Example using Selenium """

    def __init__(self, base_url, query_params):
        self.__take_results_backup()
        options = Options()
        options.add_argument("--headless")
        try:
            self.driver=Chrome(options=options)
        except Exception as e:
            print(f'Error occured during Chrome driver : {e}')
            self.driver=Firefox()
        self.driver.get(base_url + query_params)
        # set up the next page element
        self.nextpage_element=self.driver.find_element_by_css_selector(
                ".pager-next a")


    def __take_results_backup(self):
        if os.path.exists('outfile.csv'):
            stamp=f'outfile{time.asctime().replace(":", "-").replace(" ","_")}'
            shutil.move('outfile.csv', stamp)

    def __save_info(self, lines):
        """
        This method saves the recently collected information line from webpage
        """

        with open('outfile.csv', 'a') as f:
            for line in lines:
                f.write(line)

    def nextpage(self, css_locator):
        self.driver.find_element_by_css_selector(
                css_locator).click()

    def scrape_page(self):
        providers = self.driver.find_elements_by_css_selector(".provider-row")

        for provider in providers:
            try:
                name = provider.find_element_by_css_selector(
                        ".provider-base-info h3 a").text
                email = provider.find_element_by_css_selector(
                        ".provider-link-details .icon-mail+a").get_attribute(
                                'href').replace('mailto:','')
                website = provider.find_element_by_css_selector(
                        ".provider-link-details .website-link a").get_attribute('href')
                location = provider.find_element_by_css_selector(
                        ".provider-info__details div.list-item:nth-of-type(4)").text

                lineitem=f'{name.replace(",","-")},{email},{website},{location.replace(",","-")}'

                # append the results
                self.__save_info(lineitem + "\n")

            except NoSuchElementException:
                # skip information and continue scraping the page
                continue

            except Exception as e:
                # discontinue in case of unknown error
                raise ScrapePageError(f"Error occured during scrape page : {e}")

    def scrape(self):
        # scrape until nextpage function doesn't fail
        while True:
            print(f"scraping the website... ")
            try:
                self.scrape_page()
                self.nextpage(".pager-next a")

            except ScrapePageError as e:
                print(e)
                self.nextpage(".pager-next a")
                continue

            except Exception as e:
                print("Something went wrong: ", e)
                self.driver.close()
                break

class ScraperError(Exception):
    pass

class ScrapePageError(ScraperError):
    pass

if __name__=="__main__":
    # min and max number of employee for query params
    min_=10
    max_=49
    query_params=f"""/in/it-services/analytics?sort_by=field_pp_page_sponsor&
    field_pp_min_project_size=All&
    field_pp_hrly_rate_range=All&
    field_pp_size_people={min_}+-+{max_}&
    field_pp_cs_small_biz=&
    field_pp_cs_midmarket=&
    field_pp_cs_enterprise=&
    client_focus=&
    field_pp_if_advertising=&
    field_pp_if_automotive=&
    field_pp_if_arts=&
    field_pp_if_bizservices=&
    field_pp_if_conproducts=&
    field_pp_if_education=&
    field_pp_if_natural_resources=&
    field_pp_if_finservices=&
    field_pp_if_gambling=&
    field_pp_if_gaming=&
    field_pp_if_government=&
    field_pp_if_healthcare=&
    field_pp_if_hospitality=&
    field_pp_if_it=&
    field_pp_if_legal=&
    field_pp_if_manufacturing=&
    field_pp_if_media=&
    field_pp_if_nonprofit=&
    field_pp_if_realestate=&
    field_pp_if_retail=&
    field_pp_if_telecom=&
    field_pp_if_transportation=&
    field_pp_if_utilities=&
    field_pp_if_other=&
    industry_focus=&
    field_pp_location_country_select=All&
    field_pp_location_province=&
    field_pp_location_latlon_1%5Bpostal_code%5D=&
    field_pp_location_latlon_1%5Bsearch_distance%5D=100&
    field_pp_location_latlon_1%5Bsearch_units%5D=mile"""

    base_url = 'https://clutch.co/'
    query_params=query_params.replace("\n    ","") #TODO: change to regex
    scraper = Scraper(base_url, query_params)
    scraper.scrape()

