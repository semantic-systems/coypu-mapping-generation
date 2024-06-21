from abc import ABC
from typing import List

from steiner_tree.bank import BankGraph

import util.graphbuilder
from semanticlabeling.labeledcolumn import LabeledColumn
from util.knowledgesource import KnowledgeSource
from util.file import InputFile


class SemanticLabelInferencer(ABC):
    def __init__(self, input_file: InputFile, ontologies: List[KnowledgeSource]):
        self.input_file = input_file
        self.ontologies = ontologies

    def get_labeled_columns(self) -> List[LabeledColumn]:
        return self.input_file.columns

    def get_graph(self) -> BankGraph:
        return util.graphbuilder.build(self.input_file.columns)

    def print_summary(self):
        pass  # TODO
        raise NotImplementedError()
