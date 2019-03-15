This Web scraper was built for the purpose of Scraping 13-F Company Holdings from the Sec website
You can go here and enter a tiker value such as blk in the fast search section for examples
https://www.sec.gov/edgar/searchedgar/companysearch.html

# Demo

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/26131181/54400152-db042a00-4697-11e9-9834-f79609eed0c5.gif)

## Steps

This is how I stepped through the problem.

1. Visit the search results page from the Edgar website based on a customized search
   pattern I created by repeatedly making different searches. I personally customized the search url to only search for 13-F files
2. format my results page url with a ticker number to search different tickers
3. Used BeautifulSoup to parse the html data after making a requests to the webserver.
4. Parse the table data row by row since each row contained a filing report urls
5. Use Filing Report Urls to get to filing Urls page which contains 2-5 links in a table.
6. I always decided to get the last row of that table since it contained the full version of the text file that can also be read by BeautifulSoup

## Dealing with different formats

7. Get the Date of the filing report because it decides whether we are going to use AsciiFileReader or XmlFileReader
8. I learned about the format changes after reading up on this website https://www.sec.gov/divisions/investment/13ffaq.htm (I got really interested in it SEC did good)
9. Reading from XML file formats were alot easier than reading from text based file format especially for someone like me who thinks about using text files
   later on.. by just loading them into dataframes but they must be correctly formatted.
10. Formatted Ascii looked alot harder at first since for many different websites their were many different formats and missing multiple columns and values prior to 2013.
11. Decided to go with regex matching for the ascii text file. Grabbing all elements inebtween the <BODY> tags of the filing data.
12. Implemented one save method for both reader classes which simply wrote to the file row for row!
    Having two differnt filereader classes really helped alot and knowing about the SEC and file format change was really interesting to me.

# Example

if you wanted to run it by Yourself

```python
from holidings_collector import HoldingsScraper
scraper = Scraper('0001350694) # blackrock cik
scraper.initiate_variables() # You can pass in an optional numeric argument which decides how many reports to get
scrape.generate_report()

```

## If you just want it automated

```python
python3 main.py
```

### To run this either be in a virtual environment or you're own if you want to mess up your environment

To use this pip install -r requirements.txt

### Notes

Jupyter Notebooks were just my attempts at protyping and playing with the data quickly before doing the same with my vs code debugger..

### To run tests

just use pytest on the command line from the top level of the directory pytest will find it

```python
pytest
```

### Tickers worth trying

'blk' -> blackrock

'0001166559' -> Bill and Melinda Gates Foundation

'0001132699' -> Vestor Capital
