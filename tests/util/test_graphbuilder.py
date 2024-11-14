from typing import List

import pandas as pd
from steiner_tree.bank import BankGraph, BankEdge

from util import graphbuilder
from util.graphbuilder import SemanticLabelNode
from semanticlabeling.labeledcolumn import IDColumn, StringColumn, \
    DateTimeColumn, TextColumn, IntegerColumn, FloatColumn, BooleanColumn, \
    LabeledColumn


def test_build_graph_from_labeled_columns():
    graph = BankGraph()
    labeled_columns: List[LabeledColumn] = []

    #     id_col1 --------------> id_col2 -------------> id_col3
    #     /     \               /   |   \                /   \
    # str_col1 date_col1 txt_col1 id_col4 int_col1 float_col1 bool_col1

    id_col_01 = IDColumn(
        column_name='id_col1',
        min_id_length=7,
        avg_id_length=7.0,
        max_id_length=7
    )
    id_01_node = SemanticLabelNode(id_col_01.column_name, id_col_01)
    graph.add_node(id_01_node)
    labeled_columns.append(id_col_01)

    id_col_02 = IDColumn(
        column_name='id_col2',
        min_id_length=4,
        avg_id_length=4.0,
        max_id_length=4
    )
    id_02_node = SemanticLabelNode(id_col_02.column_name, id_col_02)
    graph.add_node(id_02_node)
    labeled_columns.append(id_col_02)

    id_col_03 = IDColumn(
        column_name='id_col3',
        min_id_length=7,
        avg_id_length=7.0,
        max_id_length=7
    )
    id_03_node = SemanticLabelNode(id_col_03.column_name, id_col_03)
    graph.add_node(id_03_node)
    labeled_columns.append(id_col_03)

    id_col_04 = IDColumn(
        column_name='id_col4',
        min_id_length=9,
        avg_id_length=9.0,
        max_id_length=9
    )
    id_04_node = SemanticLabelNode(id_col_04.column_name, id_col_04)
    graph.add_node(id_04_node)
    labeled_columns.append(id_col_04)

    str_col_01 = StringColumn(
        column_name='str_col1',
        min_str_length=3,
        avg_str_length=5.67,
        max_str_length=23
    )
    str_01_node = SemanticLabelNode(str_col_01.column_name, str_col_01)
    graph.add_node(str_01_node)
    labeled_columns.append(str_col_01)

    date_col_01 = DateTimeColumn(
        column_name='date_col1',
        min_date_time=pd.to_datetime('2022-02-02'),
        mean_date_time=pd.to_datetime('2022-09-30'),
        max_date_time=pd.to_datetime('2023-10-01')
    )
    date_01_node = SemanticLabelNode(date_col_01.column_name, date_col_01)
    graph.add_node(date_01_node)
    labeled_columns.append(date_col_01)

    text_col_01 = TextColumn(
        column_name='txt_col1',
        min_text_length=5,
        avg_text_length=23.45,
        max_text_length=105
    )
    text_01_node = SemanticLabelNode(text_col_01.column_name, text_col_01)
    graph.add_node(text_01_node)
    labeled_columns.append(text_col_01)

    int_col_01 = IntegerColumn(
        column_name='int_col1',
        min_value=0,
        avg_value=5.67,
        max_value=21,
        value_stddev=2.56
    )
    int_01_node = SemanticLabelNode(int_col_01.column_name, int_col_01)
    graph.add_node(int_01_node)
    labeled_columns.append(int_col_01)

    float_col_01 = FloatColumn(
        column_name='float_col1',
        min_value=0.34,
        avg_value=0.78,
        max_value=0.97,
        value_stddev=0.12
    )
    float_01_node = SemanticLabelNode(float_col_01.column_name, float_col_01)
    graph.add_node(float_01_node)
    labeled_columns.append(float_col_01)

    bool_col_01 = BooleanColumn(
        column_name='bool_col1',
        portion_true=0.7,
        portion_false=0.3
    )
    bool_01_node = SemanticLabelNode(bool_col_01.column_name, bool_col_01)
    graph.add_node(bool_01_node)
    labeled_columns.append(bool_col_01)

    id_01_to_str_01_label = 'name'
    id_col_01.add_link_to_other_column(id_01_to_str_01_label, str_col_01)
    graph.add_edge(
        BankEdge(
            0,
            source=id_col_01.column_name,
            target=str_col_01.column_name,
            key=id_01_to_str_01_label,
            n_edges=1,
            weight=1
        )
    )

    id_01_to_date_01_label = 'start'
    id_col_01.add_link_to_other_column(id_01_to_date_01_label, date_col_01)
    graph.add_edge(
        BankEdge(
            1,
            source=id_col_01.column_name,
            target=date_col_01.column_name,
            key=id_01_to_date_01_label,
            n_edges=1,
            weight=1
        )
    )

    id_01_to_id_02_label = 'parts'
    id_col_01.add_link_to_other_column(id_01_to_id_02_label, id_col_02)
    graph.add_edge(
        BankEdge(
            2,
            source=id_col_01.column_name,
            target=id_col_02.column_name,
            key=id_01_to_id_02_label,
            n_edges=1,
            weight=1
        )
    )

    id_02_to_txt_01_label = 'description'
    id_col_02.add_link_to_other_column(id_02_to_txt_01_label, text_col_01)
    graph.add_edge(
        BankEdge(
            3,
            source=id_col_02.column_name,
            target=text_col_01.column_name,
            key=id_02_to_txt_01_label,
            n_edges=1,
            weight=1
        )
    )

    id_02_to_id_04_label = 'order'
    id_col_02.add_link_to_other_column(id_02_to_id_04_label, id_col_04)
    graph.add_edge(
        BankEdge(
            4,
            source=id_col_02.column_name,
            target=id_col_04.column_name,
            key=id_02_to_id_04_label,
            n_edges=1,
            weight=1
        )
    )

    id_02_to_int_01_label = 'pos'
    id_col_02.add_link_to_other_column(id_02_to_int_01_label, int_col_01)
    graph.add_edge(
        BankEdge(
            5,
            source=id_col_02.column_name,
            target=int_col_01.column_name,
            key=id_02_to_int_01_label,
            n_edges=1,
            weight=1
        )
    )

    id_02_to_id_03_label = 'qa'
    id_col_02.add_link_to_other_column(id_02_to_id_03_label, id_col_03)
    graph.add_edge(
        BankEdge(
            6,
            source=id_col_02.column_name,
            target=id_col_03.column_name,
            key=id_02_to_id_03_label,
            n_edges=1,
            weight=1
        )
    )

    id_03_to_float_01_label = 'score'
    id_col_03.add_link_to_other_column(id_03_to_float_01_label, float_col_01)
    graph.add_edge(
        BankEdge(
            7,
            source=id_col_03.column_name,
            target=float_col_01.column_name,
            key=id_03_to_float_01_label,
            n_edges=1,
            weight=1
        )
    )

    id_03_to_bool_01_label = 'passed'
    id_col_03.add_link_to_other_column(id_03_to_bool_01_label, bool_col_01)
    graph.add_edge(
        BankEdge(
            8,
            source=id_col_03.column_name,
            target=bool_col_01.column_name,
            key=id_03_to_bool_01_label,
            n_edges=1,
            weight=1
        )
    )

    graph_to_test = graphbuilder.build(labeled_columns=labeled_columns)

    assert graph_to_test.nodes() == graph.nodes()
    assert graph_to_test.edges() == graph.edges()

    # from util import graphvisualizer
    # graphvisualizer.visualize(graph)
