import pytest
import os
from bs4 import BeautifulSoup
from holdings_collector import HoldingsScraper
from file_reader import XmlFileReader, AsciiFileReader


@pytest.fixture
def scraper():
    """Our fixture Item for generating a scraper object equivalent to unitest setup"""
    return HoldingsScraper('0001364742', 1)


def test_correct_reader_type(scraper):
    """Test if we get correct reader based on dates passed to holdings"""
    file_type = '13f-HR'
    holdings_file_url = 'https://www.sec.gov/Archives/edgar/data/1364742/000108636418000095/0001086364-18-000095.txt'
    ticker = 'blk'
    filing_date_ascii = '2010-05-12'
    filing_date_xml = '2015-06-12'
    reader = scraper.generate_employee_reader(
        file_type, holdings_file_url, filing_date_ascii, ticker)

    assert isinstance(reader, AsciiFileReader)

    reader = scraper.generate_employee_reader(
        file_type, holdings_file_url, filing_date_xml, ticker)

    assert isinstance(reader, XmlFileReader)

    assert not isinstance(reader, AsciiFileReader)


def test_report_url(scraper):
    """Testing report url using a downloaded html file"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    correct_url = 'https://www.sec.gov/Archives/edgar/data/1364742/000108636418000095/0001086364-18-000095.txt'
    with open(dir_path + '/resource/filings_page.html') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    holdings_file_url = scraper.report_url(soup)
    print(holdings_file_url[:40])
    assert holdings_file_url == correct_url


def test_filing_details(scraper):
    """Test to see if our scraper can get the correct filing details from the table"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/resource/filing_details.html') as f:
        html = f.read()

    scraper.results_page_html_ = BeautifulSoup(html, 'html.parser')
    file_type = '13F-HR'
    file_url = 'https://www.sec.gov/Archives/edgar/data/1364742/000108636418000095/0001086364-18-000095-index.htm'
    filing_date = '2018-11-09'

    details = scraper.filing_details()[0]

    assert file_type == details[0]
    assert file_url == details[1]
    assert filing_date == details[2]
