# coding=utf-8
"""Test db2ixf package"""
from db2ixf import IXFParser
from tests import RESOURCES_DIR


def test_parser(test_output_dir):
    """Test the parser."""

    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    rows = []
    for row in parser.parse():
        rows.append(row)
        assert row

    assert len(rows) == 4891


def test_json_conversion(test_output_dir):
    """Test json conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.json'

    with open(output, mode='wt', encoding='utf-8') as out:
        assert parser.to_json(out) == 0
        assert output.exists()
        assert output.is_file()


def test_csv_conversion(test_output_dir):
    """Test csv conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.csv'

    with open(output, mode='wt', encoding='utf-8') as out:
        assert parser.to_csv(out) == 0
        assert output.exists()
        assert output.is_file()


def test_parquet_conversion(test_output_dir):
    """Test parquet conversion."""
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    with open(ixf_file, mode='rb'):
        parser = IXFParser(ixf_file)

    output = test_output_dir / 'result.parquet'

    with open(output, mode='wb') as out:
        assert parser.to_parquet(out) == 0
        assert output.exists()
        assert output.is_file()
