import csv
import re
import requests
from bs4 import BeautifulSoup


class FileReader(object):
    def __init__(self, file_type, link, date, ticker):
        """Template class for reading reports of different kinds from sec website

        Args:
            file_type (str): the file_type of our report either 13f-HR or 13f-N or 13f-HR-Amended/Combined
            link (str): url to our file that will be read
            date (str): our date in string format will be save to our filename
            ticker (str): ticker symbol or CIK of company who filed the report
        """

        self.link = link
        self.date = date
        self.ticker = ticker
        self.file_type = file_type
        self.holdings = []

    def generate_document(self):
        pass

    def collect_data(self):
        pass

    def save(self):
        """Utility function for saving all of our holding data

        Returns:
            bool: Returns True if saving our data was successful otherwise False
        """

        if not self.holdings:
            print("There is nothing to save")
            return False
        file_name = self.ticker + '-' + self.file_type + self.date + '.txt'

        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(self.holdings)
        print("Saving File")

        return True


class XmlFileReader(FileReader):

    def generate_document(self):
        """Generates a document to be read by our XmlFileReader Object
            based on self.link

        Returns:
            obj: beautifulsoup object returned parsed by xml
        """

        resp = requests.get(self.link)
        return BeautifulSoup(resp.text, 'xml')

    def collect_data(self):
        """Collects our holdings data from the generated html document using beautifulsoup
        and saves it to self.holdings if there is any
        """

        soup = self.generate_document()
        information_table = soup.find('informationTable')
        if not information_table:
            print("This Document does not contain any Holdings data")
            return
        info_tables = information_table.find_all('infoTable')
        self.columns_ = [child.name for child in info_tables[0].findChildren()]
        self.holdings.append(self.columns_)
        for info_table in info_tables:
            holding = []
            for child in info_table.findChildren():
                if child.name:
                    holding.append(child.find(
                        text=True, recursive=False).strip())
            self.holdings.append(holding)


class AsciiFileReader(FileReader):

    def generate_document(self):
        """Generates an Ascii text document to be further analyzed

        Returns:
            str: string representation of our html document pulled from the web
        """

        resp = requests.get(self.link)
        return resp.text.strip()

    def collect_data(self):
        """Cleans our ascii text data by using regular expression matching and appends what is found to holdings
        """

        document = self.generate_document()

        # Use Regular Expression matching to get all data in between TABLE tags
        matchObj = re.findall(r'<TABLE>(.*?)</TABLE>',
                              document, re.M | re.I | re.S)
        try:
            for line in matchObj[0].splitlines():
                line = line.strip()
                if line:
                    row = re.split(r'\s{3,}', line)
                    self.holdings.append(row)
        except IndexError:
            print


if __name__ == "__main__":
    file_gen = XmlFileReader('13f-HR',
                             'https://www.sec.gov/Archives/edgar/data/1132699/000113269918000004/0001132699-18-000004.txt', '2018-05-12', 'bill&melinda')
    file_gen.collect_data()
    file_gen.save()

    url = 'https://www.sec.gov/Archives/edgar/data/1166559/000104746912001032/0001047469-12-001032.txt'
    ascii_file = AsciiFileReader('13f-hr', url, '2010-9-5', 'Bill&Melinda')
    ascii_file.collect_data()
    ascii_file.save()
