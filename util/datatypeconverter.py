from typing import Set

from rdflib import XSD, URIRef

from semanticlabeling import ColumnType


class UnknownDatatypeException(Exception):
    pass


known_datatypes = {
    # see: http://www.w3.org/TR/xmlschema11-2/#ID
    XSD.ID: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#IDREF
    XSD.IDREF: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#IDREFS
    XSD.IDREFS: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#NCName
    XSD.NCName: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#NMTOKEN
    XSD.NMTOKEN: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#NMTOKENS
    XSD.NMTOKENS: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#NOTATIONNOTATION cannot be used directly in a schema; rather a type
    XSD.NOTATION: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#Name
    XSD.Name: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#QName
    XSD.QName: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#anyURI
    XSD.anyURI: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#base64Binary
    XSD.base64Binary: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#boolean
    XSD.boolean: ColumnType.Boolean,
    # see: http://www.w3.org/TR/xmlschema11-2/#byte
    XSD.byte: ColumnType.Byte,
    # see: http://www.w3.org/TR/xmlschema11-2/#date
    XSD.date: ColumnType.Date,
    # see: http://www.w3.org/TR/xmlschema11-2/#dateTime
    XSD.dateTime: ColumnType.DateTime,
    # see: http://www.w3.org/TR/xmlschema11-2/#dateTimeStamp
    XSD.dateTimeStamp: ColumnType.DateTimeStamp,
    # see: http://www.w3.org/TR/xmlschema11-2/#dayTimeDuration  -- not supported
    XSD.dayTimeDuration: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#decimal
    XSD.decimal: ColumnType.Real,
    # see: http://www.w3.org/TR/xmlschema11-2/#double
    XSD.double: ColumnType.Real,
    # see: http://www.w3.org/TR/xmlschema11-2/#duration -- not supported
    XSD.duration: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#float
    XSD.float: ColumnType.Real,
    # see: http://www.w3.org/TR/xmlschema11-2/#gDay -- not supported
    XSD.gDay: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#gMonth -- not supported
    XSD.gMonth: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#gMonthDay -- not supported
    XSD.gMonthDay: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#gYear -- not supported
    XSD.gYear: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#gYearMonth -- not supported
    XSD.gYearMonth: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#binary
    XSD.hexBinary: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#int
    XSD.int: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#integer
    XSD.integer: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#language
    XSD.language: ColumnType.AtomicToken,
    # see: http://www.w3.org/TR/xmlschema11-2/#long
    XSD.long: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#negativeInteger
    XSD.negativeInteger: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#nonNegativeInteger
    XSD.nonNegativeInteger: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#nonPositiveInteger
    XSD.nonPositiveInteger: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#normalizedString
    XSD.normalizedString: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#positiveInteger
    XSD.positiveInteger: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#short
    XSD.short: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#string
    XSD.string: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#time
    XSD.time: ColumnType.Time,
    # see: http://www.w3.org/TR/xmlschema11-2/#token
    XSD.token: ColumnType.Str,
    # see: http://www.w3.org/TR/xmlschema11-2/#unsignedByte
    XSD.unsignedByte: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#unsignedInt
    XSD.unsignedInt: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#unsignedLong
    XSD.unsignedLong: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#unsignedShort
    XSD.unsignedShort: ColumnType.Int,
    # see: http://www.w3.org/TR/xmlschema11-2/#yearMonthDuration -- not supported
    XSD.yearMonthDuration: ColumnType.Str,

    # The Seven-property Model - https://www.w3.org/TR/xmlschema11-2/#theSevenPropertyModel
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-year
    XSD.year: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-month
    XSD.month: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-day
    XSD.day: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-hour
    XSD.hour: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-minute
    XSD.minute: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-second
    XSD.second: ColumnType.Int,
    # see: https://www.w3.org/TR/xmlschema11-2/#vp-dt-timezone
    XSD.timezoneOffset: ColumnType.Int
}


def get_column_type_by_iri(iri: URIRef) -> ColumnType:
    column_type = known_datatypes.get(iri)

    if column_type is None:
        raise UnknownDatatypeException()

    return column_type


def get_datatype_by_column_type(column_type: ColumnType) -> Set[URIRef]:
    datatypes: Set[URIRef] = set()

    for k, v in known_datatypes.items():
        if v == column_type:
            datatypes.add(k)

    return datatypes
