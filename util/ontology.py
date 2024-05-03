from abc import ABC
from typing import Set, Dict, List, Tuple

from rdflib import Graph, URIRef, RDF, RDFS, OWL, IdentifiedNode, DCTERMS, BNode
from rdflib.term import Node


class Ontology:
    """
    An abstraction of an ontology mainly focusing on classes, datatypes and
    properties.
    One assumption here is, that the ontology will fit into RAM and can be
    processed as is using the rdflib.
    """
    def __init__(self, ontology_file_path: str):
        self.datatype_properties: Set[URIRef] = set()
        self.range_to_datatype_property: Dict[URIRef, Set[URIRef]] = dict()
        self.datatype_property_ranges: Dict[URIRef, Set[URIRef]] = dict()
        self.domain_to_datatype_property: Dict[IdentifiedNode, Set[URIRef]] = dict()
        self.datatype_property_domains: Dict[URIRef, Set[IdentifiedNode]] = dict()

        self.object_properties: Set[URIRef] = set()
        self.range_to_object_property: Dict[IdentifiedNode, Set[URIRef]] = dict()
        self.object_property_ranges: Dict[URIRef, Set[IdentifiedNode]] = dict()
        self.domain_to_object_property: Dict[IdentifiedNode, Set[URIRef]] = dict()
        self.object_property_domains: Dict[URIRef, Set[IdentifiedNode]] = dict()

        self.unknown_property_domains: Dict[URIRef, Set[IdentifiedNode]] = dict()
        self.unknown_property_ranges: Dict[URIRef, Set[IdentifiedNode]] = dict()

        # Not sure, we will need this
        self.functional_properties: Set[URIRef] = set()
        self.inverse_functional_properties: Set[URIRef] = set()

        self.classes: Set[IdentifiedNode] = set()
        self.subclasses: Dict[IdentifiedNode, Set[IdentifiedNode]] = dict()
        self.superclasses: Dict[IdentifiedNode, Set[IdentifiedNode]] = dict()

        self.subproperties: Dict[URIRef, Set[URIRef]] = dict()
        self.inverse_properties: Set[Tuple[URIRef, URIRef]] = set()

        self.cls_restrictions: Dict[IdentifiedNode, OWLRestriction] = {}

        g = Graph()
        g.parse(ontology_file_path)

        for s, p, o in g:
            if p == RDF.type:
                self._process_type_information(s, o)
            elif p == RDFS.label:
                continue
            elif p == RDFS.seeAlso:
                continue
            elif p == RDFS.comment:
                continue
            elif p == OWL.priorVersion:
                continue
            elif p == DCTERMS.modified:
                continue
            elif p == DCTERMS.created:
                continue
            elif p == DCTERMS.contributor:
                continue
            elif p == OWL.imports:
                continue
            elif p == URIRef('http://creativecommons.org/ns#license'):
                continue
            elif p == OWL.deprecated:
                continue
            elif p == URIRef('http://www.w3.org/2004/02/skos/core#prefLabel)'):
                continue
            elif p == URIRef('http://purl.org/vocab/vann/preferredNamespacePrefix'):
                continue
            elif p == OWL.versionInfo:
                continue
            elif p == DCTERMS.title:
                continue
            elif p == DCTERMS.creator:
                continue
            elif p == RDFS.subClassOf:
                self._process_subclass_information(s, o)
            elif p == RDFS.range:
                self._process_range(s, o)
            elif p == RDFS.domain:
                self._process_domain(s, o)
            elif p == RDFS.subPropertyOf:
                self._process_subproperty(s, o)
            elif p == OWL.inverseOf:
                assert isinstance(s, URIRef)
                assert isinstance(o, URIRef)
                self.inverse_properties.add((s, o))
            elif p == OWL.someValuesFrom:
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

            elif p == OWL.hasSelf:
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

            elif p == OWL.onProperty:
                cls_restr = self.cls_restrictions.get(s)

                if cls_restr is None:
                    cls_restr = YetUnknownOWLRestriction(s)
                    cls_restr.set_property(p)
                    self.cls_restrictions[s] = cls_restr

                else:
                    cls_restr.set_property(p)

            elif p == OWL.equivalentClass:
                self._process_subclass_information(s, o)
                self._process_subclass_information(o, s)

            elif p == OWL.intersectionOf:
                # ignored for now
                # TODO: implement
                continue

            else:
                # import pdb; pdb.set_trace()
                continue
                # raise NotImplementedError()

        assert not self.unknown_property_domains
        assert not self.unknown_property_ranges

        self._post_process_subproperties()
        self._post_process_inverse_of()

    def _move_unknown_domain_declaration(self, property_: URIRef, target: URIRef):
        domains: Set[IdentifiedNode] = self.unknown_property_domains.pop(property_)

        if target == OWL.DatatypeProperty:
            if property_ not in self.datatype_property_domains:
                self.datatype_property_domains[property_] = set()
            for domain in domains:
                self.datatype_property_domains[property_].add(domain)

                if domain not in self.domain_to_datatype_property:
                    self.domain_to_datatype_property[domain] = set()
                self.domain_to_datatype_property[domain].add(property_)

        elif target == OWL.ObjectProperty:
            if property_ not in self.object_property_domains:
                self.object_property_domains[property_] = set()
            for domain in domains:
                self.object_property_domains[property_].add(domain)

                if domain not in self.domain_to_object_property:
                    self.domain_to_object_property[domain] = set()
                self.domain_to_object_property[domain].add(property_)

        else:
            import pdb; pdb.set_trace()
            raise Exception(f'Unhandled property domain target {str(target)}')

    def _move_unknown_range_declaration(self, property_: URIRef, target: URIRef):
        ranges: Set[IdentifiedNode] = self.unknown_property_ranges.pop(property_)

        if target == OWL.DatatypeProperty:
            if property_ not in self.datatype_property_ranges:
                self.datatype_property_ranges[property_] = set()
            for rnge in ranges:
                assert isinstance(rnge, URIRef)
                self.datatype_property_ranges[property_].add(rnge)

                if rnge not in self.range_to_datatype_property:
                    self.range_to_datatype_property[rnge] = set()
                self.range_to_datatype_property[rnge].add(property_)

        elif target == OWL.ObjectProperty:
            if property_ not in self.object_property_ranges:
                self.object_property_ranges[property_] = set()
            for rnge in ranges:
                self.object_property_ranges[property_].add(rnge)

                if rnge not in self.range_to_object_property:
                    self.range_to_object_property[rnge] = set()
                self.range_to_object_property[rnge].add(property_)
        else:
            import pdb; pdb.set_trace()
            raise Exception(f'Unhandled property range target {str(target)}')

    def _post_process_inverse_of(self):
        for property_1, property_2 in self.inverse_properties:
            assert isinstance(property_1, URIRef)
            assert isinstance(property_2, URIRef)

            if property_1 not in self.object_properties:
                self.object_properties.add(property_1)

            if property_2 not in self.object_properties:
                self.object_properties.add(property_2)

            if property_1 in self.object_property_domains:
                prop_1_domains = self.object_property_domains[property_1]

                for prop_1_domain in prop_1_domains:
                    if property_2 not in self.object_property_ranges:
                        self.object_property_ranges[property_2] = set()
                    self.object_property_ranges[property_2].add(prop_1_domain)

                    if prop_1_domain not in self.range_to_object_property:
                        self.range_to_object_property[prop_1_domain] = set()
                    self.range_to_object_property[prop_1_domain].add(property_2)

            if property_1 in self.object_property_ranges:
                prop_1_ranges = self.object_property_ranges[property_1]

                for prop_1_range in prop_1_ranges:
                    if property_2 not in self.object_property_domains:
                        self.object_property_domains[property_2] = set()
                    self.object_property_domains[property_2].add(prop_1_range)

                    if prop_1_range not in self.domain_to_object_property:
                        self.domain_to_object_property[prop_1_range] = set()
                    self.domain_to_object_property[prop_1_range].add(property_2)

            # 6 21
            if property_2 in self.object_property_domains:
                prop_2_domains = self.object_property_domains[property_2]

                for prop_2_domain in prop_2_domains:
                    if property_1 not in self.object_property_ranges:
                        self.object_property_ranges[property_1] = set()
                    self.object_property_ranges[property_1].add(prop_2_domain)

                    if prop_2_domain not in self.range_to_object_property:
                        self.range_to_object_property[prop_2_domain] = set()
                    self.range_to_object_property[prop_2_domain].add(property_1)

            if property_2 in self.object_property_ranges:
                prop2_ranges = self.object_property_ranges[property_2]

                for prop_2_range in prop2_ranges:
                    if property_1 not in self.object_property_domains:
                        self.object_property_domains[property_1] = set()
                    self.object_property_domains[property_1].add(prop_2_range)

                    if prop_2_range not in self.domain_to_object_property:
                        self.domain_to_object_property[prop_2_range] = set()
                    self.domain_to_object_property[prop_2_range].add(property_1)

    def _process_subproperty(self, subproperty: Node, superproperty: Node):
        assert isinstance(subproperty, URIRef)
        assert isinstance(superproperty, URIRef)

        if superproperty not in self.subproperties:
            self.subproperties[superproperty] = set()
        self.subproperties[superproperty].add(subproperty)

    def _post_process_subproperties(self):
        for superproperty, subproperties in self.subproperties.items():
            for subproperty in subproperties:
                if superproperty in self.object_properties:
                    self.object_properties.add(subproperty)
                elif superproperty in self.datatype_properties:
                    self.datatype_properties.add(subproperty)

                if superproperty in self.object_property_domains:
                    domains = self.object_property_domains[superproperty]

                    for domain in domains:
                        if subproperty not in self.object_property_domains:
                            self.object_property_domains[subproperty] = set()
                        self.object_property_domains[subproperty].add(domain)

                        self.domain_to_object_property[domain].add(subproperty)

                elif superproperty in self.datatype_property_domains:
                    domains = self.datatype_property_domains[superproperty]

                    for domain in domains:
                        if subproperty not in self.datatype_property_domains:
                            self.datatype_property_domains[subproperty] = set()
                        self.datatype_property_domains[subproperty].add(domain)

                        self.domain_to_datatype_property[domain].add(subproperty)

                if superproperty in self.object_property_ranges:
                    ranges = self.object_property_ranges[superproperty]

                    for rnge in ranges:
                        if subproperty not in self.object_property_ranges:
                            self.object_property_ranges[subproperty] = set()
                        self.object_property_ranges[subproperty].add(rnge)

                        self.range_to_object_property[rnge].add(subproperty)

                elif superproperty in self.datatype_property_ranges:
                    ranges = self.datatype_property_ranges[superproperty]

                    for rnge in ranges:
                        if subproperty not in self.datatype_property_ranges:
                            self.datatype_property_ranges[subproperty] = set()
                        self.datatype_property_ranges[subproperty].add(rnge)

                        self.range_to_datatype_property[rnge].add(subproperty)

    def _process_type_information(self, s: Node, type_: Node):
        if type_ == OWL.DatatypeProperty:
            assert isinstance(s, URIRef)
            self.datatype_properties.add(s)
            if s in self.unknown_property_domains:
                self._move_unknown_domain_declaration(s, OWL.DatatypeProperty)
            if s in self.unknown_property_ranges:
                self._move_unknown_range_declaration(s, OWL.DatatypeProperty)

        elif type_ == OWL.ObjectProperty:
            assert isinstance(s, URIRef)
            self.object_properties.add(s)
            if s in self.unknown_property_domains:
                self._move_unknown_domain_declaration(s, OWL.ObjectProperty)
            if s in self.unknown_property_ranges:
                self._move_unknown_range_declaration(s, OWL.ObjectProperty)

        elif type_ == OWL.Class or type_ == RDFS.Class or OWL.Restriction:
            assert isinstance(s, IdentifiedNode)
            self.classes.add(s)

        elif type_ == OWL.FunctionalProperty:
            assert isinstance(s, URIRef)
            self.functional_properties.add(s)
            self.object_properties.add(s)

            if s in self.unknown_property_domains:
                self._move_unknown_domain_declaration(s, OWL.ObjectProperty)
            if s in self.unknown_property_ranges:
                self._move_unknown_range_declaration(s, OWL.ObjectProperty)

        elif type_ == OWL.InverseFunctionalProperty:
            assert isinstance(s, URIRef)
            self.inverse_functional_properties.add(s)
            self.object_properties.add(s)

            if s in self.unknown_property_domains:
                self._move_unknown_domain_declaration(s, OWL.ObjectProperty)
            if s in self.unknown_property_ranges:
                self._move_unknown_range_declaration(s, OWL.ObjectProperty)

        elif type_ == OWL.AnnotationProperty \
                or type_ == OWL.Ontology or type_ == RDFS.Datatype:
            pass

        else:
            import pdb; pdb.set_trace()
            raise NotImplementedError()

    def _process_subclass_information(self, subclass: Node, superclass: Node):
        assert isinstance(subclass, IdentifiedNode)
        assert isinstance(superclass, IdentifiedNode)

        if subclass not in self.classes:
            self.classes.add(subclass)

        if subclass not in self.subclasses:
            self.subclasses[subclass] = set()

        if subclass not in self.superclasses:
            self.superclasses[subclass] = set()
        self.superclasses[subclass].add(superclass)

        if superclass not in self.classes:
            self.classes.add(superclass)

        if superclass not in self.superclasses:
            self.superclasses[superclass] = set()

        if superclass not in self.subclasses:
            self.subclasses[superclass] = set()
        self.subclasses[superclass].add(subclass)

        # get the superclasses of superclass and assign the subclass to them
        # as well
        for sup_cls in self.superclasses[superclass]:
            self.subclasses[sup_cls].add(subclass)
            self.superclasses[subclass].add(sup_cls)

        # get the subclasses of subclass and assign superclass to them as well
        for sub_cls in self.subclasses[subclass]:
            self.superclasses[sub_cls].add(superclass)
            self.subclasses[superclass].add(sub_cls)

    def _process_range(self, property_: Node, range_: Node):
        assert isinstance(property_, URIRef)

        # IRI or blank node
        assert isinstance(range_, IdentifiedNode)

        if property_ in self.object_properties:
            assert isinstance(range_, IdentifiedNode)

            if property_ not in self.object_property_ranges:
                self.object_property_ranges[property_] = set()
            self.object_property_ranges[property_].add(range_)

            if range_ not in self.range_to_object_property:
                self.range_to_object_property[range_] = set()
            self.range_to_object_property[range_].add(property_)

        elif property_ in self.datatype_properties:
            assert isinstance(range_, URIRef)

            if property_ not in self.datatype_property_ranges:
                self.datatype_property_ranges[property_] = set()
            self.datatype_property_ranges[property_].add(range_)

            if range_ not in self.range_to_datatype_property:
                self.range_to_datatype_property[range_] = set()
            self.range_to_datatype_property[range_].add(property_)

        else:
            self.unknown_property_ranges[property_] = set()
            self.unknown_property_ranges[property_].add(range_)

    def _process_domain(self, property_: Node, domain: Node):
        assert isinstance(property_, URIRef)

        # IRI or blank node
        assert isinstance(domain, IdentifiedNode)

        if property_ in self.object_properties:
            if property_ not in self.object_property_domains:
                self.object_property_domains[property_] = set()
            self.object_property_domains[property_].add(domain)

            if domain not in self.domain_to_object_property:
                self.domain_to_object_property[domain] = set()
            self.domain_to_object_property[domain].add(property_)

        elif property_ in self.datatype_properties:
            if property_ not in self.datatype_property_domains:
                self.datatype_property_domains[property_] = set()
            self.datatype_property_domains[property_].add(domain)

            if domain not in self.domain_to_datatype_property:
                self.domain_to_datatype_property[domain] = set()
            self.domain_to_datatype_property[domain].add(property_)

        else:
            self.unknown_property_domains[property_] = set()
            self.unknown_property_domains[property_].add(domain)


class OWLRestriction(ABC):
    def __init__(self, cls_bnode: BNode):
        self.cls_bnode = cls_bnode
        self.property = None

    def set_property(self, owl_property: URIRef):
        self.property = owl_property


class YetUnknownOWLRestriction(OWLRestriction):
    def __init__(self, cls_bnode: BNode):
        super().__init__(cls_bnode)


class OWLSomeValuesFrom(OWLRestriction):
    def __init__(self, cls_bnode: BNode):
        super().__init__(cls_bnode)
        self.filler = None

    def __hash__(self):
        return hash(self.cls_bnode)

    def set_filler(self, filler: IdentifiedNode):
        self.filler = filler


class OWLHasSelf(OWLRestriction):
    def __init__(self, cls_bnode: BNode):
        super().__init__(cls_bnode)
