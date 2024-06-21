from rdflib import URIRef

from util.knowledgesource import KnowledgeSource


def test_ontology_processing():
    ontology_file_path = 'tests/util/test_ontology.ttl'
    ex = 'http://example.org/'
    xsd = 'http://www.w3.org/2001/XMLSchema#'

    xsd_int = URIRef(xsd + 'int')

    cls1 = URIRef(ex + 'Cls1')
    cls2 = URIRef(ex + 'Cls2')
    cls3 = URIRef(ex + 'Cls3')
    cls4 = URIRef(ex + 'Cls4')
    cls5 = URIRef(ex + 'Cls5')
    cls6 = URIRef(ex + 'Cls6')
    cls7 = URIRef(ex + 'Cls7')

    obj_prop1 = URIRef(ex + 'objProp1')
    obj_prop2 = URIRef(ex + 'objProp2')
    obj_prop3 = URIRef(ex + 'objProp3')
    obj_prop4 = URIRef(ex + 'objProp4')
    obj_prop5 = URIRef(ex + 'objProp5')
    obj_prop6 = URIRef(ex + 'objProp6')
    obj_prop7 = URIRef(ex + 'objProp7')
    obj_prop8 = URIRef(ex + 'objProp8')
    obj_prop9 = URIRef(ex + 'objProp9')

    dtype_prop1 = URIRef(ex + 'dtypeProp1')
    dtype_prop2 = URIRef(ex + 'dtypeProp2')
    dtype_prop3 = URIRef(ex + 'dtypeProp3')
    dtype_prop4 = URIRef(ex + 'dtypeProp4')
    dtype_prop5 = URIRef(ex + 'dtypeProp5')
    dtype_prop6 = URIRef(ex + 'dtypeProp6')

    ontology = KnowledgeSource(knowledge_source_file_path=ontology_file_path)
    # FIXME
    # assert ontology.classes == {cls1, cls2, cls3, cls4, cls5, cls6, cls7}

    assert ontology.subclasses == {
        cls1: {cls2, cls3, cls4, cls5, cls6, cls7},
        cls2: {cls4, cls5},
        cls3: {cls6, cls7},
        cls4: set(),
        cls5: set(),
        cls6: set(),
        cls7: set()
    }

    assert ontology.superclasses == {
        cls1: set(),
        cls2: {cls1},
        cls3: {cls1},
        cls4: {cls2, cls1},
        cls5: {cls2, cls1},
        cls6: {cls3, cls1},
        cls7: {cls3, cls1}
    }

    # FIXME
    # assert ontology.object_properties == \
    #        {
    #            obj_prop1,
    #            obj_prop2,
    #            obj_prop3,
    #            obj_prop4,
    #            obj_prop5,
    #            obj_prop6,
    #            obj_prop7,
    #            obj_prop8,
    #            obj_prop9
    #        }

    assert ontology.datatype_properties == \
           {
               dtype_prop1,
               dtype_prop2,
               dtype_prop3,
               dtype_prop4,
               dtype_prop5,
               dtype_prop6
           }

    assert ontology.range_to_datatype_property == \
           {xsd_int: {dtype_prop2, dtype_prop4, dtype_prop6}}

    assert ontology.datatype_property_ranges == \
           {
               dtype_prop2: {xsd_int},
               dtype_prop4: {xsd_int},
               dtype_prop6: {xsd_int}
           }

    assert ontology.domain_to_datatype_property == \
           {cls1: {dtype_prop1, dtype_prop2, dtype_prop6}, cls3: {dtype_prop5}}

    assert ontology.datatype_property_domains == \
           {
               dtype_prop1: {cls1},
               dtype_prop2: {cls1},
               dtype_prop5: {cls3},
               dtype_prop6: {cls1}
           }

    assert ontology.range_to_object_property == {
        cls2: {obj_prop4, obj_prop5},
        cls7: {obj_prop3, obj_prop6},
        cls1: {obj_prop7}
    }

    assert ontology.object_property_ranges == \
           {
               obj_prop4: {cls2},
               obj_prop5: {cls2},
               obj_prop3: {cls7},
               obj_prop6: {cls7},
               obj_prop7: {cls1}
           }

    assert ontology.domain_to_object_property == \
           {cls1: {obj_prop3, obj_prop6}, cls7: {obj_prop7}}

    assert ontology.object_property_domains == \
           {obj_prop3: {cls1}, obj_prop6: {cls1}, obj_prop7: {cls7}}

    assert ontology.unknown_property_domains == dict()
    assert ontology.unknown_property_ranges == dict()
    # FIXME
    # assert ontology.functional_properties == {obj_prop1}
    # FIXME
    assert ontology.inverse_functional_properties == {obj_prop2}

    assert ontology.subproperties == \
           {obj_prop3: {obj_prop6}, dtype_prop2: {dtype_prop6}}
