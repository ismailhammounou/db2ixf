# coding=utf-8
"""Contains some encoders used to output data in some formats."""
import base64
import chardet
import json
from datetime import date, datetime, time
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle python date, time and datetime objects."""

    def default(self, o):
        if isinstance(o, (date, time, datetime)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, bytes):
            try:
                encoding = chardet.detect(o)["encoding"]
                if encoding:
                    return o.decode(encoding)
                return base64.b64encode(o).decode('utf-8')
            except UnicodeDecodeError:
                return base64.b64encode(o).decode('utf-8')
        return super().default(o)
