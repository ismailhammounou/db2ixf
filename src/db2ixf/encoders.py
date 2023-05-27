# coding=utf-8
import json
from datetime import date, datetime, time


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, time, datetime)):
            return o.isoformat()
        return super().default(o)
