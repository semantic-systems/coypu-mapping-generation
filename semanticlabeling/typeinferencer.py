from typing import Set, Tuple, Dict, List

import pandas as pd

from rdflib import URIRef
from rdflib.term import Node

from util import columninferencer
from util import datatypeinferencer
from semanticlabeling.labeledcolumn import ColumnName, TypedIDColumn, LabeledColumn
from util.statement import NotFullyTypedStatementsHandler
from util.property import PropertiesHandler, PropertyHandler
from util.type import TypesHandler, TypeHandler


class TypeInferencer:
    """
    Main object to collect type-related information and infer type-structures
    """

    def __init__(self):
        self.types_handler = TypesHandler()
        self.properties_handler = PropertiesHandler(self.types_handler)
        self.statements_handler = NotFullyTypedStatementsHandler()

    def add_type(self, type_iri: URIRef) -> None:
        self.types_handler.add_type(type_iri)

    def get_type(self, type_iri: URIRef) -> TypeHandler:
        return self.types_handler.get_type(type_iri)

    def add_instance_of_type(self, instance_iri: URIRef, type_iri: URIRef) -> None:
        self.types_handler.add_instance_of_type(instance_iri, type_iri)
        self.statements_handler.update_untyped_resource(
            instance_iri,
            type_iri,
            self.types_handler,
            self.properties_handler
        )

    def add_property(self, property_iri: URIRef) -> None:
        self.properties_handler.add_property(property_iri)

    def add_data_property(self, data_property_iri: URIRef) -> None:
        self.properties_handler.add_datatype_property(data_property_iri)

    def add_object_property(self, object_property_iri: URIRef) -> None:
        self.properties_handler.add_object_property(object_property_iri)

    def add_functional_property(self, property_iri: URIRef) -> None:
        self.properties_handler.add_functional_property(property_iri)

    def add_inverse_functional_property(self, property_iri: URIRef) -> None:
        self.properties_handler.add_inverse_functional_property(property_iri)

    def get_property(self, property_iri: URIRef) -> PropertyHandler | None:
        return self.properties_handler.get_property(property_iri)

    def get_object_property_iris(self) -> Set[URIRef]:
        return self.properties_handler.get_object_property_iris()

    def get_datatype_property_iris(self) -> Set[URIRef]:
        return self.properties_handler.get_datatype_property_iris()

    def get_functional_datatype_properties(self) -> Set[URIRef]:
        return self.properties_handler.get_functional_datatype_property_iris()

    def get_functional_object_property_iris(self) -> Set[URIRef]:
        return self.properties_handler.get_functional_object_property_iris()

    def get_inverse_functional_object_property_iris(self) -> Set[URIRef]:
        return self.properties_handler.get_inverse_functional_object_property_iris()

    def add_property_range(self, property_iri: URIRef, range_: URIRef) -> None:
        self.properties_handler.add_property_range(property_iri, range_)

    def add_property_domain(self, property_iri: URIRef, domain: URIRef) -> None:
        self.properties_handler.add_property_domain(property_iri, domain)

    def get_column_name_for(self, property_iri: URIRef) -> ColumnName:
        return self.properties_handler.get_property(property_iri).get_column_name()

    def get_typed_id_column_for_instance(self, instance: URIRef) -> TypedIDColumn | None:
        return self.types_handler.get_typed_id_column_for_instance(instance)

    def add_statement(self, s: URIRef, p: URIRef, o: Node) -> None:
        self.statements_handler.add_statement(
            s,
            p,
            o,
            self.types_handler,
            self.properties_handler
        )

    def get_property_domain_iris(self, property_iri: URIRef) -> Set[URIRef]:
        return set(
            map(
                lambda d: d.iri,
                self.get_property(property_iri).domains
            )
        )

    def get_property_range_iris(self, property_iri: URIRef) -> Set[URIRef]:
        return set(
            map(
                lambda r: r.iri,
                self.get_property(property_iri).ranges
            )
        )

    def add_inverse_properties(self, property_1: URIRef, property_2: URIRef):
        self.properties_handler.inverse_properties.add((property_1, property_2))

    def get_inverse_properties(self) -> Set[Tuple[URIRef, URIRef]]:
        return self.properties_handler.inverse_properties

    def add_subproperty(self, superproperty_iri: URIRef, subproperty_iri: URIRef):
        self.properties_handler.add_subproperty(superproperty_iri, subproperty_iri)

    def get_subproperties(self) -> Dict[URIRef, Set[URIRef]]:
        return self.properties_handler.subproperties

    def get_subproperties_of(self, superproperty_iri: URIRef) -> Set[URIRef]:
        subproperties = self.properties_handler.subproperties.get(superproperty_iri)

        if subproperties is None:
            return set()

        else:
            return subproperties

    def get_classes(self) -> Set[URIRef]:
        return self.types_handler.class_iris

    def add_subclass(self, superclass_iri: URIRef, subclass_iri: URIRef):
        self.types_handler.add_subclass(superclass_iri, subclass_iri)

    def get_subclasses_of(self, superclass_iri: URIRef) -> Set[URIRef]:
        subclasses = self.types_handler.subclasses_of.get(superclass_iri)

        if subclasses is None:
            return set()

        else:
            return subclasses

    def get_superclasses_of(self, subclass_iri: URIRef) -> Set[URIRef]:
        superclasses = self.types_handler.superclasses_of.get(subclass_iri)

        if superclasses is None:
            return set()

        else:
            return superclasses

    def get_columns(self, min_instances: int = 0) -> List[Tuple[ColumnName, LabeledColumn]]:
        return_columns: List[Tuple[ColumnName, LabeledColumn]] = []

        for datatype_id, datatype in self.types_handler.datatypes.items():
            if 0 < len(datatype.values) < min_instances:
                continue

            dtype_column = datatypeinferencer.get_column(datatype)

            if dtype_column is None:
                dtype_column = columninferencer.transform_series(
                    pd.Series(datatype.values),
                    datatype_id
                )

            return_columns.append((datatype_id, dtype_column))

        for type_iri in self.types_handler.types.keys():
            type_: TypeHandler = self.get_type(type_iri)

            if 0 < len(type_.values) < min_instances:
                continue

            column: TypedIDColumn = type_.get_id_column()

            superclasses_iris = self.types_handler.superclasses_of.get(type_iri)

            for prop in self.properties_handler.properties.values():
                type_is_in_property_domain = False
                if type_ in prop.domains:
                    type_is_in_property_domain = True

                elif superclasses_iris is not None:
                    for superclass_iri in superclasses_iris:
                        superclass_type = self.get_type(superclass_iri)

                        if superclass_type in prop.domains:
                            type_is_in_property_domain = True
                            break

                if type_is_in_property_domain:
                    for rnge in prop.ranges:
                        if 0 < len(rnge.values) < min_instances:
                            continue

                        range_column = rnge.get_column()
                        if range_column is not None:
                            column.add_link_to_other_column(prop.id_, range_column)

            return_columns.append((type_.iri, column))

        return return_columns
