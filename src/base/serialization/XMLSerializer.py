from typing import Optional, TypeVar, Type

from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

T = TypeVar("T")


class XMLSerializer:
    __xml_deserializer = XmlParser(config=ParserConfig(fail_on_unknown_properties=True))
    __xml_serializer = XmlSerializer()

    def __new__(cls):
        raise TypeError('Static classes cannot be instantiated')

    @staticmethod
    def Serialize(source):
        return XMLSerializer.__xml_serializer.render(source)

    @staticmethod
    def Deserialize(source: str, clazz: Optional[Type[T]] = None):
        return XMLSerializer.__xml_deserializer.from_string(source, clazz)
