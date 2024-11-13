from typing import Set, Dict

from rdflib import URIRef, Literal
from rdflib.term import Node

from util import datatypeinferencer
from util.property import PropertiesHandler
from util.type import TypeHandler, TypesHandler

PropertyIRI = URIRef
ResourceIRI = URIRef
ClassIRI = URIRef


class NotFullyTypedStatementsHandler:
    def __init__(self):
        self.untyped_resources: Set[ResourceIRI] = set()
        self.domain_instances: Dict[PropertyIRI, Set[ResourceIRI]] = dict()
        self.range_instances: Dict[PropertyIRI, Set[ResourceIRI]] = dict()
        self.range_values: Dict[URIRef, Set[Literal]] = dict()

    def update_untyped_resource(
            self,
            resource: ResourceIRI,
            type_iri: ClassIRI,
            types_handler: TypesHandler,
            properties_handler: PropertiesHandler
    ):
        for property_iri, domain_instances in self.domain_instances.items():
            if resource in domain_instances:
                domain_instances.remove(resource)
                property_domains = properties_handler.get_property(property_iri).domains
                is_redundant = False

                for p_dom in property_domains:
                    superclasses = types_handler.superclasses_of.get(p_dom.iri)

                    if superclasses is not None and type_iri in superclasses:
                        is_redundant = True
                        break

                if not is_redundant:
                    domain: TypeHandler = types_handler.get_type(type_iri)
                    properties_handler.get_property(property_iri).add_domain(domain)

        for property_iri, range_instances in self.range_instances.items():
            if resource in range_instances:
                range_instances.remove(resource)

                property_ranges = properties_handler.get_property(property_iri).ranges
                is_redundant = False

                for p_range in property_ranges:
                    superclasses = types_handler.superclasses_of.get(p_range.iri)

                    if superclasses is not None and type_iri in superclasses:
                        is_redundant = True
                        break

                if not is_redundant:
                    rnge: TypeHandler = types_handler.get_type(type_iri)
                    properties_handler.get_property(property_iri).add_range(rnge)

        if resource in self.untyped_resources:
            self.untyped_resources.remove(resource)

    def add_statement(
            self,
            s: ResourceIRI,
            p: PropertyIRI,
            o: Node,
            types: TypesHandler,
            properties: PropertiesHandler
    ):
        s_type: TypeHandler = types.get_type_for_instance(s)
        property_ = properties.get_property(p)

        if s_type is None:
            self.untyped_resources.add(s)
            p_dom_instances = self.domain_instances.get(p)

            if p_dom_instances is None:
                self.domain_instances[p] = set()
                p_dom_instances = self.domain_instances.get(p)

            p_dom_instances.add(s)

        else:
            property_.domains.add(s_type)

        if isinstance(o, Literal):
            if property_.is_object_property:
                # since property cannot be an object property and a datatype
                # property at the same time, we make it a general property
                property_.is_object_property = False
            else:
                property_.is_datatype_property = True

            type_iri = datatypeinferencer.get_literal_type(o)
            o_type = types.get_datatype(p, type_iri)

            o_type.values.append(o.value)
            property_.ranges.add(o_type)

        else:  # object property
            if property_.is_datatype_property:
                # since property cannot be a datatype property and an object
                # property at the same time, we make it a general property
                property_.is_datatype_property = False
            else:
                property_.is_object_property = True

            assert isinstance(o, URIRef)
            o_type = types.get_type_for_instance(o)
            if o_type is None:
                p_range_instances = self.range_instances.get(p)

                if p_range_instances is None:
                    self.range_instances[p] = set()
                    p_range_instances = self.range_instances.get(p)

                p_range_instances.add(o)

            else:
                property_.ranges.add(o_type)
