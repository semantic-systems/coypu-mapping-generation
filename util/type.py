from typing import Set, Dict

from rdflib import URIRef

from util import datatypeinferencer
from semanticlabeling.labeledcolumn import TypedIDColumn, LabeledColumn


class TypeHandler:
    def __init__(self, type_iri: URIRef, type_id: str):
        self.iri = type_iri
        self.id_ = type_id

        self.id_column = TypedIDColumn(type_id)
        self.instances: Set[URIRef] = set()
        self.is_datatype = False
        self.values = []

    def get_id_column(self) -> TypedIDColumn:
        if not self.is_datatype and self.id_column.min_id_length is None:
            self.id_column.update_stats()

        return self.id_column

    def get_column(self) -> LabeledColumn:
        if not self.is_datatype and self.id_column.min_id_length is None:
            self.id_column.update_stats()

        if self.is_datatype:
            return datatypeinferencer.get_column(self)

        else:
            return self.id_column


class TypesHandler:
    def __init__(self):
        self.types: Dict[URIRef, TypeHandler] = dict()

        # property ID -> TypeHandler
        self.datatypes: Dict[str, TypeHandler] = dict()

        self._iri_to_type_id: Dict[URIRef, str] = dict()
        self._type_id_to_iri: Dict[str, URIRef] = dict()
        self._iri_to_property_id: Dict[URIRef, str] = dict()
        self._property_id_to_iri: Dict[str, URIRef] = dict()

        self.class_iris: Set[URIRef] = set()
        self.subclasses_of: Dict[URIRef, Set[URIRef]] = dict()
        self.superclasses_of: Dict[URIRef, Set[URIRef]] = dict()

    def _get_type_id(self, type_iri: URIRef) -> str:
        type_id: str = self._iri_to_type_id.get(type_iri)

        if type_id is None:
            local_part = type_iri.split('/')[-1].split('#')[-1]
            tmp = local_part[:]
            cntr = 0
            while tmp in self._type_id_to_iri.keys():
                cntr += 1
                tmp = local_part + f'_{cntr}'

            type_id = tmp
            self._iri_to_type_id[type_iri] = type_id
            self._type_id_to_iri[type_id] = type_iri

        return type_id

    def _get_property_id(self, property_iri: URIRef) -> str:
        property_id: str = self._iri_to_property_id.get(property_iri)

        if property_id is None:
            local_part = property_iri.split('/')[-1].split('#')[-1]
            tmp = local_part[:]
            cntr = 0
            while tmp in self._property_id_to_iri.keys():
                cntr += 1
                tmp = local_part + f'_{cntr}'

            property_id = tmp
            self._iri_to_property_id[property_iri] = property_id
            self._property_id_to_iri[property_id] = property_iri

        return property_id

    def add_type(self, type_iri: URIRef) -> None:
        if type_iri not in self.types:
            self.class_iris.add(type_iri)
            type_id: str = self._get_type_id(type_iri)
            type_ = TypeHandler(type_iri=type_iri, type_id=type_id)

            self.types[type_iri] = type_

    def add_datatype(self, property_iri: URIRef, datatype_iri: URIRef):
        property_id: str = self._get_property_id(property_iri)

        if datatype_iri in self.class_iris:
            self.class_iris.remove(datatype_iri)
            datatype_ = self.types.pop(datatype_iri)
            datatype_.id_ = property_id

        else:
            datatype_ = TypeHandler(type_iri=datatype_iri, type_id=property_id)

        datatype_.is_datatype = True
        self.datatypes[property_id] = datatype_

    def get_type(self, type_iri: URIRef) -> TypeHandler:
        type_ = self.types.get(type_iri)

        if type_ is None:
            self.add_type(type_iri)
            type_ = self.types.get(type_iri)

        return type_

    def get_datatype(self, property_iri: URIRef, datatype_iri: URIRef) -> TypeHandler:
        property_id = self._get_property_id(property_iri)

        datatype_ = self.datatypes.get(property_id)

        if datatype_ is None:
            self.add_datatype(property_iri, datatype_iri)
            datatype_ = self.datatypes.get(property_id)

        return datatype_

    def add_instance_of_type(self, instance: URIRef, type_iri: URIRef) -> None:
        type_ = self.types.get(type_iri)

        if type_ is None:
            self.add_type(type_iri)
            type_ = self.get_type(type_iri)

        type_.instances.add(instance)

    def get_typed_id_column_for_instance(self, instance: URIRef) -> TypedIDColumn | None:
        typed_id_columns = []
        for type_ in self.types.values():
            if instance in type_.instances:
                typed_id_columns.append(type_.get_id_column())

        assert len(typed_id_columns) <= 1

        if typed_id_columns:
            return typed_id_columns[0]
        else:
            return None

    def get_type_for_instance(self, instance: URIRef) -> TypeHandler | None:
        types = []
        for type_ in self.types.values():
            if instance in type_.instances:
                types.append(type_)

        if types:
            return types[0]  # FIXME
        else:
            return None

    def add_subclass(self, superclass_iri: URIRef, subclass_iri: URIRef):
        if superclass_iri not in self.class_iris:
            self.add_type(superclass_iri)

        if subclass_iri not in self.class_iris:
            self.add_type(subclass_iri)

        if superclass_iri not in self.superclasses_of:
            self.superclasses_of[superclass_iri] = set()

        if superclass_iri not in self.subclasses_of:
            self.subclasses_of[superclass_iri] = set()
        self.subclasses_of[superclass_iri].add(subclass_iri)

        if subclass_iri not in self.subclasses_of:
            self.subclasses_of[subclass_iri] = set()

        if subclass_iri not in self.superclasses_of:
            self.superclasses_of[subclass_iri] = set()

        self.superclasses_of[subclass_iri].add(superclass_iri)

        # get the superclasses of superclass and assign the subclass to them
        # as well
        for sup_cls in self.superclasses_of[superclass_iri]:
            self.subclasses_of[sup_cls].add(subclass_iri)
            self.superclasses_of[subclass_iri].add(sup_cls)

        # get the subclasses of subclass and assign superclass to them as well
        for sub_cls in self.subclasses_of[subclass_iri]:
            self.superclasses_of[sub_cls].add(superclass_iri)
            self.subclasses_of[superclass_iri].add(sub_cls)
