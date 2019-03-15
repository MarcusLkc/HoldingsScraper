import pytest
from file_reader import AsciiFileReader


@pytest.fixture
def file_reader():
    xml_reader = AsciiFileReader('13f-HR',
                                 'https://www.sec.gov/Archives/edgar/data/1364742/000108636410008916/0001086364-10-008916.txt', '2010-02-12', 'black')

    return xml_reader


def test_save_returns_false(file_reader):
    assert False == file_reader.save()


def test_collected_data(file_reader):
    file_reader.collect_data()
    assert file_reader.holdings
