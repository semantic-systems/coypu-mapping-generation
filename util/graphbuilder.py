from steiner_tree.bank import BankNode, BankGraph, BankEdge

from semanticlabeling.labeledcolumn import LabeledColumn
from util.file import InputFile


class SemanticLabelNode(BankNode):
    def __init__(self, identifier: str, labeled_column: LabeledColumn):
        super().__init__(identifier)
        self.labeled_column = labeled_column


def build(processed_input_file: InputFile):
    graph = BankGraph()

    # init nodes
    for column in processed_input_file.columns:
        column_id = column.column_name  # assuming it's unique --> FIXME
        node = SemanticLabelNode(column_id, column)
        graph.add_node(node)

    # init edges
    edge_counter = 0
    for column in processed_input_file.columns:
        source_node_id = column.column_name
        for link_name, target_columns in column.links.items():
            # E.g.:
            # 'altLabel': [<semanticlabeling.labeledcolumn.TextColumn object at 0x117c39100>],
            for target_column in target_columns:
                target_node_id = target_column.column_name
                edge = BankEdge(
                    id=edge_counter,
                    source=source_node_id,
                    target=target_node_id,
                    key=link_name,
                    n_edges=1,
                    weight=1
                )

                graph.add_edge(edge)
                edge_counter += 1

    return graph
