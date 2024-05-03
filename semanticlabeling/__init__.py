import dataclasses
from enum import Enum


class ColumnType(Enum):
    Str = 'string'
    AtomicToken = 'atomic token'  # must not contain white spaces
    Int = 'integer'
    Real = 'real'
    Boolean = 'boolean'
    Byte = 'byte'
    Date = 'date'
    DateTime = 'date time'
    DateTimeStamp = 'date time stamp'
    Time = 'time'
