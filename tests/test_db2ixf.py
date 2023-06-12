# coding=utf-8
"""Test db2ixf package"""


def test_parser(test_output_dir, parser):
    rows = []
    for row in parser.parse():
        rows.append(row)
        assert row

    assert len(rows) == 4891

# def test_json_conversion(test_output_dir, parser):
#     output = test_output_dir / 'result.json'
#
#     with open(output, mode='wt', encoding='utf-8') as out:
#         assert parser.to_json(out) == 0
#         assert output.exists()
#         assert output.is_file()
#
#
# def test_csv_conversion(test_output_dir, parser):
#     output = test_output_dir / 'result.csv'
#
#     with open(output, mode='wt', encoding='utf-8') as out:
#         assert parser.to_csv(out) == 0
#         assert output.exists()
#         assert output.is_file()
#
#
# def test_parquet_conversion(test_output_dir, parser):
#     output = test_output_dir / 'result.parquet'
#
#     with open(output, mode='wb') as out:
#         assert parser.to_parquet(out, parquet_version='1.0') == 0
#         assert output.exists()
#         assert output.is_file()
