from typing import List

from steiner_tree.bank import BankNode, BankGraph, BankEdge

from semanticlabeling.labeledcolumn import LabeledColumn


class SemanticLabelNode(BankNode):
    def __init__(self, identifier: str, labeled_column: LabeledColumn):
        super().__init__(identifier)
        self.labeled_column = labeled_column

    def __eq__(self, other):
        if not isinstance(other, SemanticLabelNode):
            return False

        return self.id == other.id \
            and self.labeled_column == other.labeled_column


def build(labeled_columns: List[LabeledColumn]):
    graph = BankGraph()

    # init nodes
    for column in labeled_columns:
        if column is not None:
            column_id = column.column_name  # assuming it's unique --> FIXME
            node = SemanticLabelNode(column_id, column)
            graph.add_node(node)

    # init edges
    edge_counter = 0
    for column in labeled_columns:
        if column is None:
            continue

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
