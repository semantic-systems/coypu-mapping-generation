import pytest
from rdflib import URIRef, FOAF

from semanticlabeling.labeledcolumn import ColumnName, IntegerColumn, \
    LabeledColumn, TypedIDColumn
from util.knowledgesource import KnowledgeSource


EX = 'http://example.org/'
XSD = 'http://www.w3.org/2001/XMLSchema#'
XSD_INT = URIRef(XSD + 'int')
XSD_STR = URIRef(XSD + 'string')

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


PERSON_CLS = URIRef(EX + 'Person')
BASS_GUITAR_CLS = URIRef(EX + 'BassGuitar')
PICK_UP_SETTING_CLS = URIRef(EX + 'PickupSetting')

HAS_NAME_DTYPE_PROP = URIRef(EX + 'hasName')
PLAYS_OBJ_PROP = URIRef(EX + 'plays')
HAS_PICKUP_SETTING_PBJ_PROP = URIRef(EX + 'hasPickupSetting')


@pytest.fixture
def ontology():
    knowledge_source_file_path = 'tests/util/test_ontology.ttl'
    ont = KnowledgeSource(
        knowledge_source_file_path=knowledge_source_file_path,
        sample_portion=1
    )

    return ont


@pytest.fixture
def knowledge_source():
    knowledge_source_file_path = 'tests/util/test_knowledge_source.ttl'
    ks = KnowledgeSource(
        knowledge_source_file_path=knowledge_source_file_path,
        sample_portion=1
    )

    return ks


def test_class_processing(ontology):
    assert ontology.get_classes() == {CLS1, CLS2, CLS3, CLS4, CLS5, CLS6, CLS7}


def test_subclass_processing(ontology):
    assert {CLS2, CLS3, CLS4, CLS5, CLS6, CLS7} == ontology.get_subclasses_of(CLS1)
    assert {CLS4, CLS5} == ontology.get_subclasses_of(CLS2)
    assert {CLS6, CLS7} == ontology.get_subclasses_of(CLS3)
    assert set() == ontology.get_subclasses_of(CLS4)
    assert set() == ontology.get_subclasses_of(CLS5)
    assert set() == ontology.get_subclasses_of(CLS6)
    assert set() == ontology.get_subclasses_of(CLS7)


def test_superclass_processing(ontology):
    assert set() == ontology.get_superclasses_of(CLS1)
    assert {CLS1} == ontology.get_superclasses_of(CLS2)
    assert {CLS1} == ontology.get_superclasses_of(CLS3)
    assert {CLS2, CLS1} == ontology.get_superclasses_of(CLS4)
    assert {CLS2, CLS1} == ontology.get_superclasses_of(CLS5)
    assert {CLS3, CLS1} == ontology.get_superclasses_of(CLS6)
    assert {CLS3, CLS1} == ontology.get_superclasses_of(CLS7)


def test_object_property_processing(ontology):
    assert ontology.get_object_properties() == {
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
    assert ontology.get_datatype_properties() == {
        DTYPE_PROP1,
        DTYPE_PROP2,
        DTYPE_PROP3,
        DTYPE_PROP4,
        DTYPE_PROP5,
        DTYPE_PROP6
    }


def test_datatype_property_range_processing(ontology):
    datatype_properties = ontology.get_datatype_properties()

    assert DTYPE_PROP2 in datatype_properties
    assert {XSD_INT} == ontology.get_property_ranges(DTYPE_PROP2)

    assert DTYPE_PROP4 in datatype_properties
    assert {XSD_INT} == ontology.get_property_ranges(DTYPE_PROP4)

    assert DTYPE_PROP6 in datatype_properties
    assert {XSD_INT} == ontology.get_property_ranges(DTYPE_PROP6)


def test_datatype_property_domain_processing(ontology):
    dtype_properties = ontology.get_datatype_properties()

    assert DTYPE_PROP1 in dtype_properties
    assert {CLS1} == ontology.get_property_domains(DTYPE_PROP1)

    assert DTYPE_PROP2 in dtype_properties
    assert {CLS1} == ontology.get_property_domains(DTYPE_PROP2)

    assert DTYPE_PROP5 in dtype_properties
    assert {CLS3} == ontology.get_property_domains(DTYPE_PROP5)

    assert DTYPE_PROP6 in dtype_properties
    assert {CLS1} == ontology.get_property_domains(DTYPE_PROP6)


def test_object_property_range_processing(ontology):
    object_properties = ontology.get_object_properties()

    assert OBJ_PROP4 in object_properties
    assert {CLS2} == ontology.get_property_ranges(OBJ_PROP4)

    assert OBJ_PROP5 in object_properties
    assert {CLS2} == ontology.get_property_ranges(OBJ_PROP5)

    assert OBJ_PROP3 in object_properties
    assert {CLS7} == ontology.get_property_ranges(OBJ_PROP3)

    assert OBJ_PROP6 in object_properties
    assert {CLS7} == ontology.get_property_ranges(OBJ_PROP6)

    assert OBJ_PROP7 in object_properties
    assert {CLS1} == ontology.get_property_ranges(OBJ_PROP7)


def test_object_property_domain_processing(ontology):
    assert {CLS1} == ontology.get_property_domains(OBJ_PROP3)
    assert {CLS1} == ontology.get_property_domains(OBJ_PROP6)
    assert {CLS7} == ontology.get_property_domains(OBJ_PROP7)


def test_functional_property_processing(ontology):
    assert ontology.get_functional_object_properties() == {OBJ_PROP1}


def test_inverse_functional_property_processing(ontology):
    assert ontology.get_inverse_functional_properties() == {OBJ_PROP2}


def test_subproperty_processing(ontology):
    assert {OBJ_PROP6} == ontology.get_subproperties_of(OBJ_PROP3)
    assert {DTYPE_PROP6} == ontology.get_subproperties_of(DTYPE_PROP2)


def test_extracted_columns(ontology):
    num_id_columns = (1 +  # ex:Cls1 (TypedIDColumn)
                      1 +  # ex:Cls2 (TypedIDColumn)
                      1 +  # ex:Cls3 (TypedIDColumn)
                      1 +  # ex:Cls4 (TypedIDColumn)
                      1 +  # ex:Cls5 (TypedIDColumn)
                      1 +  # ex:Cls6 (TypedIDColumn)
                      1 +  # ex:Cls7 (TypedIDColumn)
                      # 1 +  # ex:dtypeProp1 (???)  ! not captured as range is unknown
                      1 +  # ex:dtypeProp2 (IntegerColumn)
                      # 1 +  # ex:dtypeProp3 (???)  ! not captured as range is unknown
                      1 +  # ex:dtypeProp4 (IntegerColumn)
                      # 1 +  # ex:dtypeProp5 (???)  ! not captured as range is unknown
                      # 1)  # ex:dtypeProp6 (???)  ! not captured as range is unknown
                      0)

    assert num_id_columns == len(ontology.columns)

    assert 2 == sum([isinstance(c, IntegerColumn) for c in ontology.columns.values()])
    assert 7 == sum([isinstance(c, TypedIDColumn) for c in ontology.columns.values()])


def test_extracted_columns_ks(knowledge_source):
    num_columns = (1 +  # ex:Person (TypedIDColumn)
                   1 +  # ex:BassGuitar (TypedIDColumn)
                   1 +  # ex:PickupSetting (TypedIDColumn)
                   1)  # ex:hasName (StringColumn)

    assert num_columns == len(knowledge_source.columns)

    properties_handler = knowledge_source.type_inferencer.properties_handler

    person_id_column: LabeledColumn = knowledge_source.columns.get(PERSON_CLS)
    assert isinstance(person_id_column, TypedIDColumn)

    plays_column_id: ColumnName = \
        properties_handler.get_column_name_for_property(PLAYS_OBJ_PROP)
    assert person_id_column.links.get(plays_column_id) is not None, \
        f'the {plays_column_id} link on person column to bass guitar column is not set'

    bass_guitar_id_column: LabeledColumn = knowledge_source.columns.get(BASS_GUITAR_CLS)
    assert isinstance(bass_guitar_id_column, TypedIDColumn)

    has_pickup_setting_column_id: ColumnName = \
        properties_handler.get_column_name_for_property(HAS_PICKUP_SETTING_PBJ_PROP)
    assert bass_guitar_id_column.links.get(has_pickup_setting_column_id) is not None, \
        f'the {has_pickup_setting_column_id} link on the bass guitar column to ' \
        f'pickup setting column is not set'

    pickup_setting_column: LabeledColumn = knowledge_source.columns.get(PICK_UP_SETTING_CLS)
    assert isinstance(pickup_setting_column, TypedIDColumn)


def test_class_processing_ks(knowledge_source):
    assert {PERSON_CLS, BASS_GUITAR_CLS, PICK_UP_SETTING_CLS} == knowledge_source.get_classes()


def test_subclass_processing_ks(knowledge_source):
    assert set() == knowledge_source.get_subclasses_of(PERSON_CLS)
    assert set() == knowledge_source.get_subclasses_of(BASS_GUITAR_CLS)
    assert set() == knowledge_source.get_subclasses_of(PICK_UP_SETTING_CLS)


def test_superclass_processing_ks(knowledge_source):
    assert set() == knowledge_source.get_superclasses_of(PERSON_CLS)
    assert set() == knowledge_source.get_superclasses_of(BASS_GUITAR_CLS)
    assert set() == knowledge_source.get_superclasses_of(PICK_UP_SETTING_CLS)


def test_object_property_processing_ks(knowledge_source):
    assert {
               FOAF.knows,
               HAS_PICKUP_SETTING_PBJ_PROP,
               PLAYS_OBJ_PROP
           } == knowledge_source.get_object_properties()


def test_datatype_property_processing_ks(knowledge_source):
    assert {HAS_NAME_DTYPE_PROP} == knowledge_source.get_datatype_properties()


def test_datatype_property_range_processing_ks(knowledge_source):
    datatype_properties = knowledge_source.get_datatype_properties()

    assert HAS_NAME_DTYPE_PROP in datatype_properties
    assert {XSD_STR} == knowledge_source.get_property_ranges(HAS_NAME_DTYPE_PROP)


def test_datatype_property_domain_processing_ks(knowledge_source):
    dtype_properties = knowledge_source.get_datatype_properties()

    assert HAS_NAME_DTYPE_PROP in dtype_properties
    assert {PERSON_CLS} == knowledge_source.get_property_domains(HAS_NAME_DTYPE_PROP)


def test_object_property_range_processing_ks(knowledge_source):
    object_properties = knowledge_source.get_object_properties()

    assert PLAYS_OBJ_PROP in object_properties
    assert {BASS_GUITAR_CLS} == knowledge_source.get_property_ranges(PLAYS_OBJ_PROP)

    assert HAS_PICKUP_SETTING_PBJ_PROP in object_properties

    assert {PICK_UP_SETTING_CLS} == \
           knowledge_source.get_property_ranges(HAS_PICKUP_SETTING_PBJ_PROP)


def test_object_property_domain_processing_ks(knowledge_source):
    assert {PERSON_CLS} == knowledge_source.get_property_domains(PLAYS_OBJ_PROP)

    assert {BASS_GUITAR_CLS} == \
           knowledge_source.get_property_domains(HAS_PICKUP_SETTING_PBJ_PROP)


def test_functional_property_processing_ks(knowledge_source):
    assert set() == knowledge_source.get_functional_object_properties()


def test_inverse_functional_property_processing_ks(knowledge_source):
    assert set() == knowledge_source.get_inverse_functional_properties()


def test_typeinferencer_state(knowledge_source):
    assert 0 == \
           len(knowledge_source.type_inferencer.statements_handler.untyped_resources)
