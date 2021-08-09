"""Test."""
import pytest
import os.path
from formula_one import Driver, Race, FormulaOne

filename = 'ex08_example_data.txt'


# Driver class tests.
def test_get_results():
    """Test get driver results."""
    d = Driver('Mika Hakkinen', 'Mclaren-Mercedes')
    d.add_result(1, 10)
    assert len(d.get_results()) == 1
    assert d.get_results() == {1: 10}


def test_get_points():
    """Test get points."""
    d = Driver('Mika Hakkinen', 'Mclaren-Mercedes')
    d.add_result(1, 10)
    assert d.get_points() == 10
    d.add_result(2, 20)
    assert d.get_points() == 30


# Race class tests.
def test_read_file_to_list():
    """Test read file to list."""
    r = Race(filename)
    assert len(r.read_file_to_list()) == 21
    with pytest.raises(FileNotFoundError):
        Race('ex0_example_data.txt').read_file_to_list()


def test_extract_info():
    """Test extract info."""
    r = Race(filename)
    assert type(r.extract_info('Mika Hakkinen  Mclaren-Mercedes   79694  1')) == dict
    extracted = r.extract_info('Mika Hakkinen  Mclaren-Mercedes   79694  1')
    assert type(extracted['Name'] and extracted['Team']) == str and type(extracted['Time'] and extracted['Race']) == int


def test_filter_data_by_race():
    """Test filter data by race."""
    r = Race(filename)
    filtered = r.filter_data_by_race(1)
    for line in filtered:
        assert line['Race'] == 1


def test_format_time():
    """Test format time."""
    r = Race(filename)
    assert r.format_time('79694') == '1:19.694'


def test_calculate_time_difference():
    """Test calculate time difference."""
    r = Race(filename)
    assert r.calculate_time_difference(4201, 57411) == '+0:53.210'


def test_sort_data_by_time():
    """Test sort data by time."""
    r = Race(filename)
    sorted_time = r.sort_data_by_time([{'Time': 79694}, {'Time': 77690}])
    assert sorted_time == [{'Time': 77690}, {'Time': 79694}]


def test_get_results_by_race():
    """Test get results by race."""
    r = Race(filename)
    results = r.get_results_by_race(1)
    assert results[0] == {'Name': 'Jenson Button', 'Team': 'Williams-BMW', 'Time': '1:17.606', 'Diff': '', 'Place': 1,
                          'Points': 25, 'Race': 1}
    alt_results = Race('ex08_alternate_data.txt').get_results_by_race(1)
    assert alt_results[10]['Points'] == 0


def test_get_race_results():
    """Test get race results."""
    r = Race(filename)
    all_results = r.get_results()
    assert len(all_results) == 21


# FormulaOne class tests.
def test_write_race_results_to_file():
    """Test write race results to file."""
    f1 = FormulaOne(filename)
    f1.write_race_results_to_file(2)
    assert os.path.isfile('results_for_race_2.txt')


def test_write_race_results_to_csv():
    """Test write race results to csv."""
    f1 = FormulaOne(filename)
    f1.write_race_results_to_csv(3)
    assert os.path.isfile('race_3_results.csv')


def test_write_championship_to_file():
    """Test write championship to file."""
    f1 = FormulaOne(filename)
    f1.write_championship_to_file()
    assert os.path.isfile('championship_results.txt')
