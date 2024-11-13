from typing import Dict, Set, Tuple

from rdflib import URIRef

from util.type import TypesHandler, TypeHandler


class PropertyHandler:
    def __init__(self, property_iri: URIRef, property_id: str):
        self.iri: URIRef = property_iri
        self.id_: str = property_id

        self.domains: Set[TypeHandler] = set()
        self.ranges: Set[TypeHandler] = set()

        self.is_object_property = False
        self.is_datatype_property = False
        self.is_functional = False
        self.is_inverse_functional = False

    def get_column_name(self):
        return self.id_

    def add_range(self, rnge: TypeHandler):
        self.ranges.add(rnge)

    def add_domain(self, domain: TypeHandler):
        self.domains.add(domain)


class PropertiesHandler:
    def __init__(self, types_handler: TypesHandler):
        self.properties: Dict[str, PropertyHandler] = dict()
        self.types = types_handler

        self._iri_to_property_id: Dict[URIRef, str] = dict()
        self._property_id_to_iri: Dict[str, URIRef] = dict()

        self.subproperties: Dict[URIRef, Set[URIRef]] = dict()
        self.inverse_properties: Set[Tuple[URIRef, URIRef]] = set()

    def _compute_and_add_property_id(self, iri: URIRef):
        property_id = self._iri_to_property_id.get(iri)

        if property_id is None:
            local_part = iri.split('/')[-1].split('#')[-1]
            tmp = local_part[:]
            cntr = 0
            while tmp in self._property_id_to_iri.keys():
                cntr += 1
                tmp = local_part + str(cntr)

            property_id = tmp

            self._iri_to_property_id[iri] = property_id
            self._property_id_to_iri[property_id] = iri

        return property_id

    def add_property(self, property_iri: URIRef) -> None:
        assert \
            property_iri not in self._iri_to_property_id.keys(), \
            'Property was already added'

        property_id = self._compute_and_add_property_id(property_iri)

        property_ = PropertyHandler(property_iri, property_id)

        self.properties[property_iri] = property_

    def add_datatype_property(self, property_iri: URIRef) -> None:
        property_ = self.get_property(property_iri)

        if property_.is_object_property:
            # downgrade to general property to stay consistent
            property_.is_object_property = False
        else:
            property_.is_datatype_property = True

        for rnge in property_.ranges:
            self.types.add_datatype(property_iri, rnge.iri)

    def add_object_property(self, property_iri: URIRef) -> None:
        property_ = self.get_property(property_iri)

        assert \
            not property_.is_datatype_property, \
            'Property cannot be an object property and data property ' \
            'at the same time'

        property_.is_object_property = True

    def add_functional_property(self, property_iri: URIRef) -> None:
        property_ = self.get_property(property_iri)
        property_.is_functional = True

    def add_inverse_functional_property(self, property_iri: URIRef):
        property_ = self.get_property(property_iri)
        property_.is_inverse_functional = True

        assert \
            not property_.is_datatype_property, \
            'Property cannot be an inverse functional property and data ' \
            'property at the same time'

        property_.is_object_property = True

    def get_property(self, property_iri: URIRef) -> PropertyHandler:
        property_ = self.properties.get(property_iri)

        if property_ is None:
            self.add_property(property_iri)
            property_ = self.properties.get(property_iri)

        return property_

    def get_column_name_for_property(self, property_iri: URIRef):
        property_ = self.get_property(property_iri)

        return property_.id_

    def get_object_property_iris(self) -> Set[URIRef]:
        return \
            {
                op.iri
                for op
                in self.properties.values()
                if op.is_object_property
            }

    def get_datatype_property_iris(self) -> Set[URIRef]:
        return \
            {
                dp.iri
                for dp
                in self.properties.values()
                if dp.is_datatype_property
            }

    def get_functional_datatype_property_iris(self):
        return \
            {
                dp.iri
                for dp
                in self.properties.values()
                if dp.is_datatype_property and dp.is_functional
            }

    def get_functional_object_property_iris(self) -> Set[URIRef]:
        return \
            {
                op.iri
                for op
                in self.properties.values()
                if op.is_object_property and op.is_functional
            }

    def get_inverse_functional_object_property_iris(self) -> Set[URIRef]:
        return \
            {
                op.iri
                for op
                in self.properties.values()
                if op.is_object_property and op.is_inverse_functional
            }

    def add_property_range(self, property_iri: URIRef, range_iri: URIRef) -> None:
        property_ = self.get_property(property_iri)

        if property_.is_datatype_property:
            type_ = self.types.get_datatype(
                property_iri=property_iri,
                datatype_iri=range_iri
            )

        else:
            type_ = self.types.get_type(range_iri)

        property_.ranges.add(type_)

    def add_property_domain(self, property_iri: URIRef, domain: URIRef) -> None:
        property_ = self.get_property(property_iri)
        type_ = self.types.get_type(domain)
        property_.domains.add(type_)

    def add_subproperty(self, superproperty: URIRef, subproperty: URIRef):
        assert isinstance(subproperty, URIRef)
        assert isinstance(superproperty, URIRef)

        if superproperty not in self.subproperties:
            self.subproperties[superproperty] = set()
        self.subproperties[superproperty].add(subproperty)
