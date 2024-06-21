import dataclasses
from enum import Enum


class ColumnType(Enum):
    Str = 'string'
    AtomicToken = 'atomic token'  # must not contain white spaces
    Categories = 'categories'
    Int = 'integer'
    Real = 'real'
    Float = 'float'
    Boolean = 'boolean'
    Byte = 'byte'
    Date = 'date'
    DateTime = 'date time'
    DateTimeStamp = 'date time stamp'
    Text = 'text'
    Time = 'time'
    ID = 'ID'
    Lat = 'lat'
    Lon = 'lon'
    Unknown = 'unknown'
