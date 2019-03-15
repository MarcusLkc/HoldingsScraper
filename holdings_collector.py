"""Web scraper for the Sec website
This Module Contains The webscraper used to move page by page on the Edgar website
starting at the results page then moving all the way to document file
"""

import requests
from bs4 import BeautifulSoup
import datetime
import time
from file_reader import XmlFileReader, AsciiFileReader


class HoldingsScraper(object):
    """Webscraper for navigating through the

    Raises:
        Exception: Raise exception when there is no valid CIK or ticker symbol entered this
        can be easily handled with an exception
    Attributes:
        base_url (str): The base Url for searching for our ticker value. Needs to be formatted
        domain_url (str): Domain Url of the sec.gov website which will be used for appending file paths
        ticker (str): Symbol or CIK of stock we are interested in
        number_of_reports (int, optional): Defaults to 1. The number of reports that we would like to generate
        results_page_url (str) : The Url of our results page after formating with ticker value
        results_page_html (soup): Default None. The results page of our html in Beautiful Soup Format
                     needs to be a beautifulSoup object. can be instantiated with initiate_variables()

    Notes:
        If we completely want to skip 13F-N files and just aim for 13F files we can switch our type parameter in base_url to be
        &type=13F-HR
    """

    base_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=13F&dateb=&owner=exclude&count=100'
    domain_url = 'https://www.sec.gov'

    def __init__(self, ticker, number_of_reports=1):

        self.ticker = ticker
        self.number_of_reports = number_of_reports
        self._DATE_OF_FORMAT_CHANGE = '2013-05-20'
        self.results_page_url = self.base_url.format(ticker)
        self.results_page_html_ = None

    def initiate_varibles(self):
        """Initializes our results_page_html_ variable
        and any other future variables we have not created yet
        """

        self.results_page_html_ = self.generate_html(self.results_page_url)

    def generate_html(self, url):
        """Generates a Beautiful Soup Html object
        for further parsing

        Args:
            url (str): url of webpage we would like to get

        Returns:
            BeautifulSoup Html Object
        """
        resp = requests.get(url)
        return BeautifulSoup(resp.text, "html.parser")

    def generate_report(self):
        """Main function for generating and saving reports
        Controls what type
        """

        details = self.filing_details()
        for file_type, filings_url, filing_date in details:
            filings_html = self.generate_html(filings_url)
            holdings_file_url = self.report_url(filings_html)

            report = self.generate_employee_reader(
                file_type, holdings_file_url, filing_date, self.ticker)

            print(holdings_file_url)

            report.collect_data()
            report.save()
            del report

    def generate_employee_reader(self, file_type, holdings_file_url, filing_date, ticker):
        """Generates Employee Reader based on the filing date of the report 
        We Compare filing date with the date of format_change to see whether Ascii or XmlReader is needed
        Visit here to read about https://www.sec.gov/divisions/investment/13ffaq.htm the formatting changes
        from Ascii to XML 

        Args:
            file_type (str): string representing name of 13f form 
            holdings_file_url (str): url of our holdings file
            filing_date (str): date our file was created
            ticker (str): ticker symbol or cik of our 13f

        Returns:
            object: Returns either an AscciFileREader or XmlFileReader Object
        """

        if time.strptime(filing_date, "%Y-%m-%d") < time.strptime(self._DATE_OF_FORMAT_CHANGE, "%Y-%m-%d"):
            print("This is an ascii style file")
            return AsciiFileReader(file_type,
                                   holdings_file_url, filing_date, self.ticker)
        else:
            print("this is a xml styled file")
            return XmlFileReader(file_type,
                                 holdings_file_url, filing_date, self.ticker)

    def filing_details(self):
        """Cleans the table of our results page and 
        gathers links and details to our filings

        Raises:
            Exception: Raises exception when no results are obtained from
            the Edgar Website

        Returns:
            :obj:`list` of :obj:`tuple`: Returns a list of tuples containing strings file_type, file_url, filing_date
        """
        # All indexes refer to the specific index of our data the table indexs do not change
        URL_INDEX = 1
        DATE_INDEX = 3
        table = self.results_page_html_.find('table', class_='tableFile2')
        if not table:
            raise Exception(
                'There does not seem to be any reports for that CIK or ticker symbol please try again.')
        table_rows = table.find_all('tr')[1:]

        # Find the Link for our 13F from the second column of our table
        # Skip the first index of table row and get until our number of records wanted
        details = []
        for row in table_rows[:self.number_of_reports]:
            file_type = row.find('td').text
            filings_url = self.domain_url + \
                row.find_all('td')[URL_INDEX].find('a')['href']
            date = row.find_all('td')[DATE_INDEX].text.strip()
            details.append((file_type, filings_url, date))

        return details

    def report_url(self, soup):
        """Parses our soup html object to find the table which 
        has the links to the FilingReport
        Args:
            soup (:obj: bs4) : BeautifulSoup4 html object

        Returns:
            str: The url link to the Filings Report
        """
        table = soup.find('table', class_='tableFile')
        last_row = table.find_all('tr')[-1]
        path_to_report = last_row.find_all('td')[2].find('a')['href']
        holdings_file_url = self.domain_url + path_to_report
        return holdings_file_url
