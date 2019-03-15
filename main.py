"""Main function for running our Edgar scraper application
allowing users to continually request reports until they are pleased
"""

from holdings_collector import HoldingsScraper
import sys


if __name__ == "__main__":

    choice = 1
    while choice != 'q':
        try:
            number_of_pages = input(
                "How Many Reports would you like? Press Enter for only the most recent ")
            cik = input("Please Enter the Cik or Stock Symbol ")

            if number_of_pages:
                number_of_pages = int(number_of_pages)
                scraper = HoldingsScraper(cik, number_of_pages)
            else:
                scraper = HoldingsScraper(cik)

            scraper.initiate_varibles()
            scraper.generate_report()
            choice = input('hit Enter to continue or q to quit ')

        except ValueError as e:
            print(e)
