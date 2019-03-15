import pytest
from file_reader import XmlFileReader


@pytest.fixture
def file_reader():
    xml_reader = XmlFileReader('13f-HR',
                               'https://www.sec.gov/Archives/edgar/data/1166559/000110465918068485/0001104659-18-068485.txt', '2010-05-12', 'blake')

    return xml_reader


def test_save_returns_false(file_reader):
    assert False == file_reader.save()


def test_collected_data(file_reader):
    file_reader.collect_data()
    assert file_reader.holdings
