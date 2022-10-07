# import module
import json


# parent class
class JsonSerializer(object):
    _sortKeys = True
    __indent = 4

    # __init__ is known as the constructor
    def __init__(self):
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=self._sortKeys, indent=self.__indent)
