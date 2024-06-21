from abc import ABC
from typing import Set, Dict, Tuple

import pandas as pd
from rdflib import Graph, URIRef, RDF, RDFS, OWL, IdentifiedNode, BNode
from rdflib.term import Node, Literal

from semanticlabeling.labeledcolumn import TextColumn, LabeledColumn, YetUnknownTypeColumn, \
    UntypedIDColumn, TypedIDColumn
from util import columninferencer


class KnowledgeSource:
    """
    An abstraction of an OWL knowledge source.

    In terms of the TBox we mainly focus on classes, datatypes and
    properties.
    One assumption here is, that the ontology will fit into RAM and can be
    processed as is using the rdflib.
    """
    def __init__(self, knowledge_source_file_path: str):
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

        self.cls_restrictions: Dict[IdentifiedNode, OWLRestriction] = dict()

        self._uri_to_column_name: Dict[URIRef, str] = dict()
        self._uri_to_type_id: Dict[IdentifiedNode, str] = dict()

        # add ID 'multi-column' which has to be subdivided by rdf:type
        self.untyped_ids = UntypedIDColumn()

        self.id_columns: Dict[str, TypedIDColumn] = dict()
        self.columns: Dict[str, LabeledColumn] = dict()
        self.link_target_instances_to_source: Dict[IdentifiedNode, Set[Tuple[str, TypedIDColumn]]] = \
            dict()  # instance of target type: {(link name, source), ...}
        self.link_source_instances_to_target_instance: Dict[IdentifiedNode, Set[Tuple[str, IdentifiedNode]]] = \
            dict()  # instance of yet unknown source type: {(link name, instance of yet unknown target type), ...}

        # not needed as link source instances carry their target column in the
        # links field in self.untyped_ids
        # self.link_source_instances_to_target: Dict[IdentifiedNode, Set[Tuple[str, TypedIDColumn]]] = \
        #     dict()  # instance of source type: [(link name, target), ...]

        # add name column for rdfs:label
        self.label_column = TextColumn('name', 0, 0, 0)

        # add comment column for rdfs:comment
        self.comment_column = TextColumn('comment', 0, 0, 0)

        g = Graph()
        g.parse(knowledge_source_file_path)

        for s, p, o in g:
            assert isinstance(s, IdentifiedNode)
            assert isinstance(p, URIRef)
            assert isinstance(o, Node)

            if p == RDF.type:
                assert isinstance(o, IdentifiedNode)

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
                assert isinstance(o, IdentifiedNode)

                self._process_subclass_information(s, o)
                continue

            elif p == RDFS.range:
                assert isinstance(o, IdentifiedNode)

                self._process_range(s, o)
                continue

            elif p == RDFS.domain:
                assert isinstance(o, IdentifiedNode)

                self._process_domain(s, o)
                continue

            elif p == RDFS.subPropertyOf:
                assert isinstance(o, IdentifiedNode)

                self._process_subproperty(s, o)
                continue

            elif p == OWL.inverseOf:
                assert isinstance(s, URIRef)
                assert isinstance(o, URIRef)

                self.inverse_properties.add((s, o))
                continue

            elif p == OWL.someValuesFrom:
                assert isinstance(o, IdentifiedNode)
                assert isinstance(s, BNode)

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
                assert isinstance(s, BNode)
                assert isinstance(o, IdentifiedNode)

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
                assert isinstance(s, BNode)
                assert isinstance(o, IdentifiedNode)

                cls_restr = self.cls_restrictions.get(s)

                if cls_restr is None:
                    cls_restr = YetUnknownOWLRestriction(s)
                    cls_restr.set_property(p)
                    self.cls_restrictions[s] = cls_restr

                else:
                    cls_restr.set_property(p)

                continue

            elif p == OWL.equivalentClass:
                assert isinstance(o, IdentifiedNode)

                self._process_subclass_information(s, o)
                self._process_subclass_information(o, s)
                continue

            elif p == OWL.intersectionOf:
                # ignored for now
                # TODO: implement
                continue

            else:
                column_name = self._get_column_name(p)
                column = self._get_column(column_name)

                s_id = str(s)
                s_typed_id_column = self._get_id_type_for_iri_or_bnode(s)

                link_source_type_unknown = s_typed_id_column is None

                if isinstance(o, IdentifiedNode):
                    # object property case

                    o_id = str(o)
                    o_typed_id_column = self._get_id_type_for_iri_or_bnode(o)
                    link_target_type_unknown = o_typed_id_column is None

                    if link_source_type_unknown:
                        if link_target_type_unknown:
                            # --> temporarily store in
                            # self.link_source_instances_to_target_instance

                            #     no links added here as target column not known
                            #                                  v
                            self.untyped_ids.add_entry(s_id, dict())
                            self.untyped_ids.add_entry(o_id, dict())

                            links_from_s = \
                                self.link_source_instances_to_target_instance.get(s)

                            if links_from_s is None:
                                links_from_s = set()
                                self.link_source_instances_to_target_instance[s] = links_from_s

                            links_from_s.add((column_name, o))

                        else:
                            # link target type known
                            # --> store s in self.untyped_ids with individual link
                            self.untyped_ids.add_entry(
                                id_str=s_id,
                                # Dict[str, LabeledColumn]
                                links={column_name: o_typed_id_column}
                            )

                            o_typed_id_column.add_id(o_id)

                    else:  # link source type known
                        if link_target_type_unknown:
                            s_typed_id_column.add_id(s_id)
                            self.untyped_ids.add_entry(o, dict())

                            # temporarily store in
                            # self.link_target_instances_to_source:
                            # Dict[IdentifiedNode, Set[Tuple[str, TypedIDColumn]]]
                            # instance of target type: {(link name, source column), ...}
                            links_to_o: Set[Tuple[str, TypedIDColumn]] = \
                                self.link_target_instances_to_source.get(o)

                            if links_to_o is None:
                                self.link_target_instances_to_source[o] = set()

                            links_to_o.add((column_name, s_typed_id_column))

                        else:
                            # link target type known
                            # --> add each ID to ID column with link from s to o
                            o_typed_id_column.add_id(o_id)
                            s_typed_id_column.add_id(o_id)
                            s_typed_id_column.add_link_to_other_column(
                                column_name, o_typed_id_column)

                else:
                    # literal/datatype property case
                    column.add_value(str(o))
                continue

        assert not self.unknown_property_domains
        assert not self.unknown_property_ranges

        self._post_process_subproperties()
        self._post_process_inverse_of()

        self._post_process_unknown_columns()

    def _post_process_unknown_columns(self):
        # YetUnknownTypeColumn in self.columns
        revised_columns = dict()
        for column_name, column in self.columns.items():
            if isinstance(column, YetUnknownTypeColumn):
                series = pd.Series(column.values)

                if len(series) > 0:
                    inferred_column = columninferencer.transform_series(
                        series_name=column_name,
                        series=series
                    )

                    revised_columns[column_name] = inferred_column

                else:
                    continue

            else:
                revised_columns[column_name] = column

        self.columns = revised_columns

        # self.untyped_ids
        for id_ in self.untyped_ids.entries:
            pass
            pass
        # self.link_target_instances_to_source

        # self.link_source_instances_to_target_instance


        pass

    def _get_column(self, column_name: str):
        column = self.columns.get(column_name)

        if column is None:
            column = YetUnknownTypeColumn(column_name)
            self.columns[column_name] = column

        return column

    def _get_column_name(self, property_iri: URIRef):
        column_name = self._uri_to_column_name.get(property_iri)

        if column_name is None:
            local_part = property_iri.split('/')[-1].split('#')[-1]
            tmp = local_part[:]
            cntr = 0
            while tmp in self._uri_to_column_name.values():
                cntr += 1
                tmp = local_part + str(cntr)

            column_name = tmp
            self._uri_to_column_name[property_iri] = column_name

        return column_name

    def _get_type_id(self, type_iri_or_bnode: IdentifiedNode) -> str:
        # type_iri can also be a BNode!!!
        type_id: str = self._uri_to_type_id.get(type_iri_or_bnode)

        if type_id is None:
            local_part = type_iri_or_bnode.split('/')[-1].split('#')[-1]
            tmp = local_part[:]
            cntr = 0
            while tmp in self._uri_to_type_id.values():
                cntr += 1
                tmp = local_part + f'_{cntr}'

            type_id = tmp
            self._uri_to_type_id[type_iri_or_bnode] = type_id

        return type_id

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

    def _process_type_information(self, s: IdentifiedNode, type_: IdentifiedNode):
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

        elif type_ == OWL.Class or type_ == RDFS.Class or type_ == OWL.Restriction:
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
            id_str = str(s)
            if self.untyped_ids.contains_id(id_str):
                # this if branch is mainly to collect links to other columns
                # that were found in previous iterations where it was not yet
                # clear of which type s is
                #
                links: Set[Tuple[str, LabeledColumn]] = \
                    self.untyped_ids.get_id_links(id_str)
                self.untyped_ids.remove_entry(id_str)

                type_id = self._get_type_id(type_)
                typed_id_column = self.id_columns.get(type_id)

                if typed_id_column is None:
                    typed_id_column = TypedIDColumn(type_id, 0, 0, 0)

                typed_id_column.add_id(id_str)

                for link_name, target_column in links:
                    typed_id_column.add_link_to_other_column(link_name, target_column)

                if s in self.link_target_instances_to_source.keys():
                    # instance of target type: [(link name, source), ...]
                    for link_name, source_column in self.link_target_instances_to_source[s]:
                        source_column.add_link_to_other_column(link_name, typed_id_column)

                    self.link_target_instances_to_source.pop(s)

                if s in self.link_source_instances_to_target_instance.keys():
                    # instance of yet unknown source type: [(link name, instance of yet unknown target type), ...]
                    # --> move to self.link_target_instances_to_source
                    for link_name, target_instance in self.link_source_instances_to_target_instance[s]:
                        source_links = self.link_target_instances_to_source.get(target_instance)

                        if source_links is None:
                            source_links = set()
                            self.link_target_instances_to_source[target_instance] = source_links

                        source_links.add((link_name, typed_id_column))

                    self.link_source_instances_to_target_instance.pop(s)

                empty_entries = []
                for source_instance, instance_links in self.link_source_instances_to_target_instance.items():
                    links_to_remove = []
                    for link_name, target_instance in instance_links:
                        assert isinstance(target_instance, URIRef)
                        if s == target_instance:
                            links_to_remove.append(link_name)

                    for link_name in links_to_remove:
                        instance_links.remove((link_name, s))

                    if not instance_links:
                        empty_entries.append(source_instance)

                for instance in empty_entries:
                    self.link_source_instances_to_target_instance.pop(instance)

            else:
                typed_id_column = self._get_id_type_for_iri_or_bnode(s)

                if typed_id_column is None:
                    type_id = self._get_type_id(type_)
                    typed_id_column = TypedIDColumn(type_id, 0, 0, 0)

                typed_id_column.add_id(id_str)

                # we haven't seen s before (otherwise it would have been in
                # self.untyped_ids) so no need to add any links to other columns

    def _get_id_type_for_iri_or_bnode(
            self,
            iri_or_bnode: IdentifiedNode
    ) -> TypedIDColumn | None:

        for type_id, typed_id_column in self.id_columns:
            if typed_id_column.contains_id(str(iri_or_bnode)):
                return typed_id_column

        return None

    def _process_subclass_information(
            self,
            subclass: IdentifiedNode,
            superclass: IdentifiedNode
    ):

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


if __name__ == '__main__':
    input_file_path = '/Users/patrick/tmp/data/yago/tiny/yago-tiny.nt'
    ks = KnowledgeSource(input_file_path)
