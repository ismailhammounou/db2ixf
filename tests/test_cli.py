# coding=utf-8
"""Test db2ixf CLI (cli.py)."""
import subprocess
from tests import RESOURCES_DIR


def test_cli_db2ixf_conversion_to_json(test_output_dir):
    """Test CLI db2ixf conversion to json."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    # Output in json
    output_file = test_output_dir / 'result.json'

    # Run the db2ixf CLI command
    command = [
        'db2ixf',
        'json',
        str(ixf_file),
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()


def test_cli_db2ixf_conversion_to_csv(test_output_dir):
    """Test CLI db2ixf conversion to csv."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    # Output in csv
    output_file = test_output_dir / 'result.csv'

    # Run the db2ixf CLI command
    command = [
        'db2ixf',
        'csv',
        str(ixf_file),
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()


def test_cli_db2ixf_conversion_to_parquet(test_output_dir):
    """Test CLI db2ixf conversion to parquet."""
    # Input file in IXF
    ixf_file = RESOURCES_DIR / 'data' / 'sample-confidential.ixf'

    # Output in parquet
    output_file = test_output_dir / 'result.parquet'

    # Run the db2ixf CLI command
    command = [
        'db2ixf',
        'parquet',
        str(ixf_file),
        str(output_file),
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # Assert the expected output or behavior
    assert result.returncode == 0  # Successful execution
    assert output_file.exists()
    assert output_file.is_file()
