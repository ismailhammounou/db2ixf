# coding=utf-8
"""Contains some encoders used to output data in some formats."""
import json
from datetime import date, datetime, time


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle python date, time and datetime objects."""

    def default(self, o):
        if isinstance(o, (date, time, datetime)):
            return o.isoformat()
        return super().default(o)
