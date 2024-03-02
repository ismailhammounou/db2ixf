# coding=utf-8
"""Test db2ixf package"""
import pytest
from db2ixf import IXFParser
from tests import RESOURCES_DIR


def test_pkg_parser(test_output_dir):
    """Test the parser."""
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    with open(ixf_file, mode="rb") as fo:
        parser = IXFParser(fo)
        rows = []
        for row in parser.get_row():
            rows.append(row)
            assert row

    assert len(rows) >= 0


def test_pkg_json_conversion(test_output_dir):
    """Test json conversion."""
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    with open(ixf_file, mode="rb") as fo:
        parser = IXFParser(fo)
        output = test_output_dir / "result.json"
        with open(output, mode="wt", encoding="utf-8") as out:
            assert parser.to_json(out) is True

    assert output.exists()
    assert output.is_file()


def test_pkg_jsonline_conversion(test_output_dir):
    """Test json line conversion."""
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    with open(ixf_file, mode="rb") as fo:
        parser = IXFParser(fo)
        output = test_output_dir / "result.jsonl"
        with open(output, mode="wt", encoding="utf-8") as out:
            assert parser.to_jsonline(out) is True

    assert output.exists()
    assert output.is_file()


@pytest.mark.parametrize("separator, size", [("$", None), ("#", 1000)])
def test_pkg_csv_conversion(test_output_dir, separator, size):
    """Test csv conversion."""
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    with open(ixf_file, mode="rb") as fo:
        parser = IXFParser(fo)
        output = test_output_dir / "result.csv"
        with open(output, mode="wt", encoding="utf-8") as out:
            assert parser.to_csv(out, sep=separator, batch_size=size) is True

    assert output.exists()
    assert output.is_file()

# parquet_param_data = [
#     ("1.0", None), ("2.4", None), ("2.6", None),
#     ("1.0", 100), ("2.4", 100), ("2.6", 100),
#     ("1.0", 500), ("2.4", 500), ("2.6", 500),
#     ("1.0", 1000), ("2.4", 1000), ("2.6", 1000),
# ]
#
#
# @pytest.mark.parametrize("parquet_version, size", parquet_param_data)
# def test_pkg_parquet_conversion(test_output_dir, parquet_version, size):
#     """Test parquet conversion."""
#     ixf_file = RESOURCES_DIR / "data" / "sample.ixf"
#
#     with open(ixf_file, mode="rb") as fo:
#         parser = IXFParser(fo)
#         output = test_output_dir / "result.parquet"
#         with open(output, mode="wb") as out:
#             assert parser.to_parquet(
#                 out,
#                 batch_size=size,
#                 parquet_version=parquet_version
#             ) is True
#
#     assert output.exists()
#     assert output.is_file()
#
#
# _size = [None, 10, 100, 1000, 10000, 100000, 1000000]
#
#
# @pytest.mark.parametrize("size", _size)
# def test_pkg_deltalake_conversion(test_output_dir, size):
#     """Test deltalake conversion."""
#     ixf_file = RESOURCES_DIR / "data" / "sample.ixf"
#
#     with open(ixf_file, mode="rb") as fo:
#         parser = IXFParser(fo)
#         output = test_output_dir / "deltalake"
#         assert parser.to_deltalake(output, batch_size=size) is True
#
#     assert output.exists()
#     assert output.is_dir()
