import random
from abc import ABC
from typing import Set, Dict

from rdflib import Graph, URIRef, RDF, RDFS, OWL, IdentifiedNode
from rdflib.term import Node, Literal

import util.graphbuilder
from semanticlabeling.typeinferencer import TypeInferencer
from semanticlabeling.labeledcolumn import TextColumn, LabeledColumn, YetUnknownTypeColumn, \
    UntypedIDColumn


class KnowledgeSource:
    """
    An abstraction of an OWL knowledge source.

    In terms of the TBox we mainly focus on classes, datatypes and
    properties.
    One assumption here is, that the ontology will fit into RAM and can be
    processed as is using the rdflib.
    """
    def __init__(
            self,
            knowledge_source_file_path: str,
            sample_portion: float,
            min_column_rows: int = 0
    ):
        self.cls_restrictions: Dict[IdentifiedNode, OWLRestriction] = dict()

        self.min_column_rows = min_column_rows
        self.type_inferencer = TypeInferencer()
        self._uri_to_column_name: Dict[URIRef, str] = dict()
        self._column_name_to_uri: Dict[str, URIRef] = dict()
        self._uri_to_type_id: Dict[IdentifiedNode, str] = dict()
        self._type_id_to_uri: Dict[str, IdentifiedNode] = dict()

        # add ID 'multi-column' which has to be subdivided by rdf:type
        self.untyped_ids = UntypedIDColumn()
        self.tmp_id_columns: Dict[str, YetUnknownTypeColumn] = dict()

        # self.id_columns: Dict[str, TypedIDColumn] = dict()
        self.columns: Dict[str, LabeledColumn] = dict()

        # add name column for rdfs:label
        self.label_column = TextColumn('name', 0, 0, 0)

        # add comment column for rdfs:comment
        self.comment_column = TextColumn('comment', 0, 0, 0)

        g_ = Graph()
        g_.parse(knowledge_source_file_path)
        g = g_.skolemize()
        del g_

        for s, p, o in g:
            assert isinstance(s, URIRef)
            assert isinstance(p, URIRef)
            assert isinstance(o, Node)

            if p == RDF.type:
                assert isinstance(o, URIRef)

                self._process_type_information(s, o)

            elif p == RDFS.label:
                assert isinstance(o, Literal)

                label_length = len(str(o))
                self.label_column.update_stats(label_length)
                continue

            elif p == RDFS.seeAlso:
                continue

            elif p == RDFS.comment:
                assert isinstance(o, Literal)

                comment_length = len(str(o))
                self.comment_column.update_stats(comment_length)
                continue

            elif p == OWL.priorVersion:
                continue

            elif p == OWL.imports:
                continue

            elif p == OWL.deprecated:
                continue

            elif p == URIRef('http://purl.org/vocab/vann/preferredNamespacePrefix'):
                continue

            elif p == OWL.versionInfo:
                continue

            elif p == RDFS.subClassOf:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_subclass(o, s)
                continue

            elif p == RDFS.range:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_property_range(s, o)
                continue

            elif p == RDFS.domain:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_property_domain(s, o)
                continue

            elif p == RDFS.subPropertyOf:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_subproperty(o, s)
                continue

            elif p == OWL.inverseOf:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_inverse_properties(s, o)
                continue

            elif p == OWL.someValuesFrom:
                assert isinstance(o, URIRef)

                partially_initialized_restriction = self.cls_restrictions.get(s)

                # In case the OWL.onProperty triple was processed before (at
                # that time not knowing whether it belongs to an existential,
                # universal or other kind of restriction) it was temporarily
                # stored as YetUnknownOWLRestriction
                if partially_initialized_restriction is not None:
                    assert isinstance(
                        partially_initialized_restriction, YetUnknownOWLRestriction
                    )

                    restriction = OWLSomeValuesFrom(s)
                    restriction.set_property(
                        partially_initialized_restriction.property)
                    restriction.set_filler(o)
                    self.cls_restrictions[s] = restriction
                    del partially_initialized_restriction

                else:
                    restriction = OWLSomeValuesFrom(s)
                    restriction.set_filler(o)
                    self.cls_restrictions[s] = restriction

                continue

            elif p == OWL.hasSelf:
                assert isinstance(o, Literal)

                partially_initialized_restriction = self.cls_restrictions.get(s)

                # In case the OWL.onProperty triple was processed before (at
                # that time not knowing whether it belongs to an existential,
                # universal or other kind of restriction) it was temporarily
                # stored as YetUnknownOWLRestriction
                if partially_initialized_restriction is not None:
                    assert isinstance(
                        partially_initialized_restriction, YetUnknownOWLRestriction
                    )

                    restriction = OWLHasSelf(s)
                    restriction.set_property(
                        partially_initialized_restriction.property)
                    self.cls_restrictions[s] = restriction
                    del partially_initialized_restriction

                else:
                    restriction = OWLHasSelf(s)
                    self.cls_restrictions[s] = restriction

                continue

            elif p == OWL.onProperty:
                assert isinstance(o, URIRef)

                cls_restr = self.cls_restrictions.get(s)

                if cls_restr is None:
                    cls_restr = YetUnknownOWLRestriction(s)
                    cls_restr.set_property(p)
                    self.cls_restrictions[s] = cls_restr

                else:
                    cls_restr.set_property(p)

                continue

            elif p == OWL.equivalentClass:
                assert isinstance(o, URIRef)

                self.type_inferencer.add_subclass(s, o)
                self.type_inferencer.add_subclass(o, s)
                continue

            elif p == OWL.intersectionOf:
                # ignored for now
                # TODO: implement
                continue

            else:
                if random.random() <= sample_portion:
                    self.type_inferencer.add_statement(s, p, o)

        self._post_process_subproperties()
        self._post_process_inverse_of()
        self._post_process_columns()

        del g

    def get_object_properties(self) -> Set[URIRef]:
        return self.type_inferencer.get_object_property_iris()

    def get_datatype_properties(self) -> Set[URIRef]:
        return self.type_inferencer.get_datatype_property_iris()

    def get_inverse_functional_properties(self) -> Set[URIRef]:
        return self.type_inferencer.get_inverse_functional_object_property_iris()

    def get_functional_object_properties(self) -> Set[URIRef]:
        return self.type_inferencer.get_functional_object_property_iris()

    def get_property_domains(self, property_iri: URIRef) -> Set[URIRef]:
        return self.type_inferencer.get_property_domain_iris(property_iri)

    def get_property_ranges(self, property_iri: URIRef) -> Set[URIRef]:
        return self.type_inferencer.get_property_range_iris(property_iri)

    def get_classes(self) -> Set[URIRef]:
        return self.type_inferencer.get_classes()

    def get_subproperties_of(self, superproperty: URIRef) -> Set[URIRef]:
        return self.type_inferencer.get_subproperties_of(superproperty)

    def get_superclasses_of(self, subclass: URIRef) -> Set[URIRef]:
        return self.type_inferencer.get_superclasses_of(subclass)

    def get_subclasses_of(self, superclass: URIRef) -> Set[URIRef]:
        return self.type_inferencer.get_subclasses_of(superclass)

    def _get_column(self, column_name: str):
        column = self.columns.get(column_name)

        if column is None:
            column = YetUnknownTypeColumn(column_name)
            self.columns[column_name] = column

        return column

    def _post_process_inverse_of(self):
        for property_1_iri, property_2_iri in self.type_inferencer.get_inverse_properties():
            assert isinstance(property_1_iri, URIRef)
            assert isinstance(property_2_iri, URIRef)

            property_1 = self.type_inferencer.get_property(property_1_iri)
            property_2 = self.type_inferencer.get_property(property_2_iri)

            if not property_1.is_object_property:
                property_1.is_object_property = True

            if not property_2.is_object_property:
                property_2.is_object_property = True

            property_2.ranges = property_2.ranges.union(property_1.domains)
            property_2.domains = property_2.domains.union(property_1.ranges)

            property_1.ranges = property_1.ranges.union(property_2.domains)
            property_1.domains = property_1.domains.union(property_2.ranges)

    def _post_process_subproperties(self):
        for superproperty_iri, subproperty_iris in self.type_inferencer.get_subproperties().items():
            superproperty = self.type_inferencer.get_property(superproperty_iri)
            for subproperty_iri in subproperty_iris:
                subproperty = self.type_inferencer.get_property(subproperty_iri)

                if superproperty.is_object_property:
                    assert not subproperty.is_datatype_property
                    subproperty.is_object_property = True

                elif superproperty.is_datatype_property:
                    assert not subproperty.is_object_property
                    subproperty.is_datatype_property = True

                subproperty.domains = subproperty.domains.union(superproperty.domains)
                subproperty.ranges = subproperty.ranges.union(superproperty.ranges)

    @staticmethod
    def _resource_to_id(iri: URIRef):
        return str(iri)

    def _process_typed_instance(self, instance: URIRef, type_: URIRef):
        """
        Called, e.g., whenever a triple was processed that assigns a type to a
        resource, which is not part of the standard vocabularies, i.e.

            :res01 rdf:type :MyCustomCls .

        """
        self.type_inferencer.add_instance_of_type(
            instance_iri=instance,
            type_iri=type_
        )

    def _process_type_information(self, s: URIRef, type_: URIRef):
        if type_ == OWL.DatatypeProperty:
            self.type_inferencer.add_data_property(s)

        elif type_ == OWL.ObjectProperty:
            self.type_inferencer.add_object_property(s)

        elif type_ == OWL.Class or type_ == RDFS.Class or type_ == OWL.Restriction:
            self.type_inferencer.add_type(s)

        elif type_ == OWL.FunctionalProperty:
            self.type_inferencer.add_functional_property(s)

        elif type_ == OWL.InverseFunctionalProperty:
            self.type_inferencer.add_inverse_functional_property(s)

        elif type_ == OWL.AnnotationProperty \
                or type_ == OWL.Ontology or type_ == RDFS.Datatype:

            pass

        else:  # a type not part of the RDF/RDFS/OWL vocabulary
            self._process_typed_instance(s, type_)

    def _post_process_columns(self):
        for id_, column in self.type_inferencer.get_columns(min_instances=self.min_column_rows):
            self.columns[id_] = column

    def get_graph(self):
        columns = list(self.columns.values())

        return util.graphbuilder.build(columns)


class OWLRestriction(ABC):
    def __init__(self, cls_bnode: IdentifiedNode):
        self.cls_bnode = cls_bnode
        self.property = None

    def set_property(self, owl_property: URIRef):
        self.property = owl_property


class YetUnknownOWLRestriction(OWLRestriction):
    def __init__(self, cls_bnode: IdentifiedNode):
        super().__init__(cls_bnode)


class OWLSomeValuesFrom(OWLRestriction):
    def __init__(self, cls_bnode: IdentifiedNode):
        super().__init__(cls_bnode)
        self.filler = None

    def __hash__(self):
        return hash(self.cls_bnode)

    def set_filler(self, filler: IdentifiedNode):
        self.filler = filler


class OWLHasSelf(OWLRestriction):
    def __init__(self, cls_bnode: IdentifiedNode):
        super().__init__(cls_bnode)
