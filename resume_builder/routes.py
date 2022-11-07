import json
import datetime

class JsonObjEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return str(o)
        elif isinstance(o, object):
            return str(o)
        else:
            return super().default(o)