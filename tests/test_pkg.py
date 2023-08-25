# coding=utf-8
"""Test db2ixf package"""
import pytest
from db2ixf import IXFParser
from tests import RESOURCES_DIR


def test_pkg_parser(test_output_dir):
    """Test the parser."""

    ixf_file = RESOURCES_DIR / 'data' / 'sample.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    rows = []
    for row in parser.parse():
        rows.append(row)
        assert row

    assert len(rows) == 2


def test_pkg_json_conversion(test_output_dir):
    """Test json conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.json'

    with open(output, mode='wt', encoding='utf-8') as out:
        assert parser.to_json(out) == 0
        assert output.exists()
        assert output.is_file()


@pytest.mark.parametrize('separator', ['$', '#'])
def test_pkg_csv_conversion(test_output_dir, separator):
    """Test csv conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.csv'

    with open(output, mode='wt', encoding='utf-8') as out:
        assert parser.to_csv(out, sep=separator) == 0
        assert output.exists()
        assert output.is_file()


parquet_param_data = [
    ('1.0', 100), ('2.4', 100), ('2.6', 100),
    ('1.0', 500), ('2.4', 500), ('2.6', 500),
    ('1.0', 1000), ('2.4', 1000), ('2.6', 1000),
]


@pytest.mark.parametrize('parquet_version, size', parquet_param_data)
def test_pkg_parquet_conversion(test_output_dir, parquet_version, size):
    """Test parquet conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.parquet'

    with open(output, mode='wb') as out:
        assert parser.to_parquet(out,
                                 batch_size=size,
                                 parquet_version=parquet_version) == 0
        assert output.exists()
        assert output.is_file()


size_data = [10, 100, 1000, 10000, 100000, 1000000]


@pytest.mark.parametrize('size', size_data)
def test_pkg_deltalake_conversion(test_output_dir, size):
    """Test deltalake conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'deltalake'

    parser.to_deltalake(output, batch_size=size)
    assert output.exists()
    assert output.is_dir()
