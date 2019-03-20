#!/usr/bin/env python
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

#TODO: Check if  Scraper can be a subclass of Chrome
class Scraper(object):
    """ A Simple Scraper Example using Selenium """

    def __init__(self, base_url, query_params):
        options = Options()
        options.add_argument("--headless")
        self.driver=Chrome(options=options)
        self.driver.get(base_url + query_params)

    def __writetofile(self, lines):
        with open('outfile.csv', 'a') as f:
            for line in lines:
                f.write(line)

    def nextpage(self, css_locator):
        try:
            self.driver.find_element_by_css_selector(css_locator).click()
        except Exception as e:
            print(f'During page change : {e}')

    def scrape_page(self):
        providers = self.driver.find_elements_by_css_selector(".provider-row")
        lines=[]
        for provider in providers:
            name = provider.find_element_by_css_selector(
                    ".provider-base-info h3 a").text
            email = provider.find_element_by_css_selector(
                    ".provider-link-details.icon-mail+a").get_attribute(
                            'href').replace('mailto:','')
            website = provider.find_element_by_css_selector(
                    ".provider-link-details .website-link a").get_attribute('href')
            location = provider.find_element_by_css_selector(
                    ".provider-info__details div.list-item:nth-of-type(4)").text

            lineitem=f'{name.replace(",","-")},{email},{website},{location.replace(",","-")}'
            lines.append(lineitem + "\n")

        # append the results
        self.__writetofile(lines)

    def scrape(self):
        for i in range(5):
            print(f"scraping page {i}")
            import pdb;pdb.set_trace()
            self.scrape_page()
            try:
                self.nextpage(".pager-next a")
            except Exception as e:
                print("Error while going to next page :", e)
                self.driver.close()
                break


if __name__=="__main__":

    base_url = 'https://clutch.co/'
    query_params='in/it-services/analytics?sort_by=field_pp_page_sponsor&field_pp_min_project_size=All&field_pp_hrly_rate_range=All&field_pp_size_people=0+-+50&field_pp_cs_small_biz=&field_pp_cs_midmarket=&field_pp_cs_enterprise=&client_focus=&field_pp_if_advertising=&field_pp_if_automotive=&field_pp_if_arts=&field_pp_if_bizservices=&field_pp_if_conproducts=&field_pp_if_education=&field_pp_if_natural_resources=&field_pp_if_finservices=&field_pp_if_gambling=&field_pp_if_gaming=&field_pp_if_government=&field_pp_if_healthcare=&field_pp_if_hospitality=&field_pp_if_it=&field_pp_if_legal=&field_pp_if_manufacturing=&field_pp_if_media=&field_pp_if_nonprofit=&field_pp_if_realestate=&field_pp_if_retail=&field_pp_if_telecom=&field_pp_if_transportation=&field_pp_if_utilities=&field_pp_if_other=&industry_focus=&field_pp_location_chttps://clutch.co/it-services/analytics?sort_by=field_pp_page_sponsor&field_pp_min_project_size=All&field_pp_hrly_rate_range=All&field_pp_size_people=50+-+249&field_pp_cs_small_biz=&field_pp_cs_midmarket=&field_pp_cs_enterprise=&client_focus=&field_pp_if_advertising=&field_pp_if_automotive=&field_pp_if_arts=&field_pp_if_bizservices=&field_pp_if_conproducts=&field_pp_if_education=&field_pp_if_natural_resources=&field_pp_if_finservices=&field_pp_if_gambling=&field_pp_if_gaming=&field_pp_if_government=&field_pp_if_healthcare=&field_pp_if_hospitality=&field_pp_if_it=&field_pp_if_legal=&field_pp_if_manufacturing=&field_pp_if_media=&field_pp_if_nonprofit=&field_pp_if_realestate=&field_pp_if_retail=&field_pp_if_telecom=&field_pp_if_transportation=&field_pp_if_utilities=&field_pp_if_other=&industry_focus=&field_pp_location_country_select=in&field_pp_location_province=&field_pp_location_latlon_1%5Bpostal_code%5D=&field_pp_location_latlon_1%5Bsearch_distance%5D=100&field_pp_location_latlon_1%5Bsearch_units%5D=mileountry_select=in&field_pp_location_province=&field_pp_location_latlon_1%5Bpostal_code%5D=&field_pp_location_latlon_1%5Bsearch_distance%5D=100&field_pp_location_latlon_1%5Bsearch_units%5D=mile'

    scraper = Scraper(base_url, query_params)
    scraper.scrape()

