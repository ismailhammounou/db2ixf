# coding=utf-8
"""Test db2ixf CLI (cli.py)."""
import pytest
import subprocess
from tests import RESOURCES_DIR


def test_cli_conversion_to_json(test_output_dir):
    """Test CLI db2ixf conversion to json."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    # Output in json
    output_file = test_output_dir / "result.json"

    # Run the db2ixf CLI command
    command = [
        "db2ixf",
        "json",
        str(ixf_file),
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()


def test_cli_conversion_to_jsonline(test_output_dir):
    """Test CLI db2ixf conversion to json line."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    # Output in json line
    output_file = test_output_dir / "result.jsonl"

    # Run the db2ixf CLI command
    command = [
        "db2ixf",
        "jsonline",
        str(ixf_file),
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()


@pytest.mark.parametrize("separator, size", [("$", None), ("#", 1000)])
def test_cli_conversion_to_csv(test_output_dir, separator, size):
    """Test CLI db2ixf conversion to csv."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / "data" / "sample.ixf"

    # Output in csv
    output_file = test_output_dir / "result.csv"

    # Run the db2ixf CLI command
    if size:
        command = [
            "db2ixf",
            "csv",
            "--sep",
            separator,
            "--batch-size",
            str(size),
            str(ixf_file),
            str(output_file)
        ]
    else:
        command = [
            "db2ixf",
            "csv",
            "--sep",
            separator,
            str(ixf_file),
            str(output_file)
        ]

    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()

# parquet_param_data = [
#     ("1.0", None), ("2.4", None), ("2.6", None),
#     ("1.0", 100), ("2.4", 100), ("2.6", 100),
#     ("1.0", 500), ("2.4", 500), ("2.6", 500),
#     ("1.0", 1000), ("2.4", 1000), ("2.6", 1000),
# ]
#
#
# @pytest.mark.parametrize("parquet_version, size", parquet_param_data)
# def test_cli_conversion_to_parquet(
#     test_output_dir,
#     parquet_version,
#     size
# ):
#     """Test CLI db2ixf conversion to parquet."""
#     # Input file in IXF
#     ixf_file = RESOURCES_DIR / "data" / "sample.ixf"
#
#     # Output in parquet
#     output_file = test_output_dir / "result.parquet"
#
#     # Run the db2ixf CLI command
#     if size:
#         command = [
#             "db2ixf",
#             "parquet",
#             "--parquet-version",
#             parquet_version,
#             "--batch-size",
#             str(size),
#             str(ixf_file),
#             str(output_file)
#         ]
#     else:
#         command = [
#             "db2ixf",
#             "parquet",
#             "--parquet-version",
#             parquet_version,
#             str(ixf_file),
#             str(output_file)
#         ]
#
#     result = subprocess.run(command, capture_output=True, text=True)
#
#     # Assert the expected output or behavior
#     assert result.returncode == 0  # Successful execution
#     assert output_file.exists()
#     assert output_file.is_file()
