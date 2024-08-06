import pytest
from rdflib import URIRef

from util.knowledgesource import KnowledgeSource


EX = 'http://example.org/'
XSD = 'http://www.w3.org/2001/XMLSchema#'
XSD_INT = URIRef(XSD + 'int')
CLS1 = URIRef(EX + 'Cls1')
CLS2 = URIRef(EX + 'Cls2')
CLS3 = URIRef(EX + 'Cls3')
CLS4 = URIRef(EX + 'Cls4')
CLS5 = URIRef(EX + 'Cls5')
CLS6 = URIRef(EX + 'Cls6')
CLS7 = URIRef(EX + 'Cls7')

OBJ_PROP1 = URIRef(EX + 'objProp1')
OBJ_PROP2 = URIRef(EX + 'objProp2')
OBJ_PROP3 = URIRef(EX + 'objProp3')
OBJ_PROP4 = URIRef(EX + 'objProp4')
OBJ_PROP5 = URIRef(EX + 'objProp5')
OBJ_PROP6 = URIRef(EX + 'objProp6')
OBJ_PROP7 = URIRef(EX + 'objProp7')
OBJ_PROP8 = URIRef(EX + 'objProp8')
OBJ_PROP9 = URIRef(EX + 'objProp9')

DTYPE_PROP1 = URIRef(EX + 'dtypeProp1')
DTYPE_PROP2 = URIRef(EX + 'dtypeProp2')
DTYPE_PROP3 = URIRef(EX + 'dtypeProp3')
DTYPE_PROP4 = URIRef(EX + 'dtypeProp4')
DTYPE_PROP5 = URIRef(EX + 'dtypeProp5')
DTYPE_PROP6 = URIRef(EX + 'dtypeProp6')


@pytest.fixture
def ontology():
    knowledge_source_file_path = 'tests/util/test_ontology.ttl'
    ont = KnowledgeSource(knowledge_source_file_path=knowledge_source_file_path)

    return ont


def test_class_processing(ontology):
    assert ontology.classes == {CLS1, CLS2, CLS3, CLS4, CLS5, CLS6, CLS7}


def test_subclass_processing(ontology):
    assert ontology.subclasses == {
        CLS1: {CLS2, CLS3, CLS4, CLS5, CLS6, CLS7},
        CLS2: {CLS4, CLS5},
        CLS3: {CLS6, CLS7},
        CLS4: set(),
        CLS5: set(),
        CLS6: set(),
        CLS7: set()
    }


def test_superclass_processing(ontology):
    assert ontology.superclasses == {
        CLS1: set(),
        CLS2: {CLS1},
        CLS3: {CLS1},
        CLS4: {CLS2, CLS1},
        CLS5: {CLS2, CLS1},
        CLS6: {CLS3, CLS1},
        CLS7: {CLS3, CLS1}
    }


def test_object_property_processing(ontology):
    assert ontology.object_properties == {
        OBJ_PROP1,
        OBJ_PROP2,
        OBJ_PROP3,
        OBJ_PROP4,
        OBJ_PROP5,
        OBJ_PROP6,
        OBJ_PROP7,
        OBJ_PROP8,
        OBJ_PROP9
    }


def test_datatype_property_processing(ontology):
    assert ontology.datatype_properties == {
        DTYPE_PROP1,
        DTYPE_PROP2,
        DTYPE_PROP3,
        DTYPE_PROP4,
        DTYPE_PROP5,
        DTYPE_PROP6
    }


def test_datatype_property_range_processing(ontology):
    assert ontology.range_to_datatype_property == \
           {XSD_INT: {DTYPE_PROP2, DTYPE_PROP4, DTYPE_PROP6}}

    assert ontology.datatype_property_ranges == {
        DTYPE_PROP2: {XSD_INT},
        DTYPE_PROP4: {XSD_INT},
        DTYPE_PROP6: {XSD_INT}
    }


def test_datatype_property_domain_processing(ontology):
    assert ontology.domain_to_datatype_property == \
           {CLS1: {DTYPE_PROP1, DTYPE_PROP2, DTYPE_PROP6}, CLS3: {DTYPE_PROP5}}

    assert ontology.datatype_property_domains == {
        DTYPE_PROP1: {CLS1},
        DTYPE_PROP2: {CLS1},
        DTYPE_PROP5: {CLS3},
        DTYPE_PROP6: {CLS1}
    }


def test_object_property_range_processing(ontology):
    assert ontology.range_to_object_property == {
        CLS2: {OBJ_PROP4, OBJ_PROP5},
        CLS7: {OBJ_PROP3, OBJ_PROP6},
        CLS1: {OBJ_PROP7}
    }

    assert ontology.object_property_ranges == {
        OBJ_PROP4: {CLS2},
        OBJ_PROP5: {CLS2},
        OBJ_PROP3: {CLS7},
        OBJ_PROP6: {CLS7},
        OBJ_PROP7: {CLS1}
    }


def test_object_property_domain_processing(ontology):
    assert ontology.domain_to_object_property == \
           {CLS1: {OBJ_PROP3, OBJ_PROP6}, CLS7: {OBJ_PROP7}}

    assert ontology.object_property_domains == \
           {OBJ_PROP3: {CLS1}, OBJ_PROP6: {CLS1}, OBJ_PROP7: {CLS7}}


def test_unknown_property_domains(ontology):
    assert ontology.unknown_property_domains == dict()
    assert ontology.unknown_property_ranges == dict()


def test_functional_property_processing(ontology):
    assert ontology.functional_properties == {OBJ_PROP1}


def test_inverse_functional_property_processing(ontology):
    assert ontology.inverse_functional_properties == {OBJ_PROP2}


def test_subproperty_processing(ontology):
    assert ontology.subproperties == \
           {OBJ_PROP3: {OBJ_PROP6}, DTYPE_PROP2: {DTYPE_PROP6}}
