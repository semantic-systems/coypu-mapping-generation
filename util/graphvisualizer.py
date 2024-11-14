import logging
from typing import List

from pyvis.network import Network
from steiner_tree.bank import BankGraph

from util.graphbuilder import SemanticLabelNode
from semanticlabeling.labeledcolumn import IDColumn, TextColumn, \
    CategoriesColumn, FloatColumn, WGS84LatitudeColumn, WGS84LongitudeColumn, \
    DateTimeColumn


logger = logging.getLogger(__name__)

# color mapping for different column types
# semantically similar columns have similar colors
color_mapping = {
    'LabeledColumn': '#FF6347',          # Tomato Red
    'IDColumn': '#FFFFFF',               # White
    'TextColumn': '#4682B4',             # Steel Blue
    'CategoriesColumn': '#5F9EA0',       # Cadet Blue
    'FloatColumn': '#32CD32',            # Lime Green
    'WGS84CoordinateColumn': '#FFD700',  # Gold
    'WGS84LatitudeColumn': '#FFA500',    # Orange
    'WGS84LongitudeColumn': '#FF8C00',   # Dark Orange
    'DateTimeColumn': '#8A2BE2',         # Blue Violet
    'Default': '#BBBBBB'                 # Gray (selected if the column type is not in the mapping)
}


name_mapping = {
    'LabeledColumn': 'Labeled Column',
    'IDColumn': 'ID',
    'TextColumn': 'Text',
    'CategoriesColumn': 'Categories',
    'FloatColumn': 'Float',
    'WGS84CoordinateColumn': 'WGS84 Coordinate',
    'WGS84LatitudeColumn': 'WGS84 Latitude',
    'WGS84LongitudeColumn': 'WGS84 Longitude',
    'DateTimeColumn': 'Date Time',
    'Default': 'Unknown Type'
}


shape_mapping = {
    'LabeledColumn': 'dot',
    'IDColumn': 'square',
    'TextColumn': 'dot',
    'CategoriesColumn': 'dot',
    'FloatColumn': 'dot',
    'WGS84CoordinateColumn': 'dot',
    'WGS84LatitudeColumn': 'dot',
    'WGS84LongitudeColumn': 'dot',
    'DateTimeColumn': 'dot',
    'Default': 'dot'
}


def _get_column_type(node: SemanticLabelNode) -> str:
    """
    Get the type of the column of a SemanticLabelNode.
    - node: SemanticLabelNode
    """

    labeled_column = node.labeled_column

    return labeled_column.__class__.__name__


def _get_column_name(node: SemanticLabelNode) -> str:
    """
    Get the name of the column of a SemanticLabelNode.
    - node: SemanticLabelNode
    """

    labeled_column = node.labeled_column

    return labeled_column.column_name


def construct_node_title(node: SemanticLabelNode) -> str:
    """
    Construct the title of a node for visualization.
    - node: SemanticLabelNode
    """

    labeled_column = node.labeled_column

    column_name = _get_column_name(node)
    column_type = _get_column_type(node)

    match column_type:
        case 'LabeledColumn':
            title = f'{column_name} (Labeled Column)'

        case 'IDColumn':
            assert isinstance(labeled_column, IDColumn)
            title = \
                f'{column_name} (ID)\n' \
                f'Min Length: {labeled_column.min_id_length}\n' \
                f'Avg Length: {labeled_column.avg_id_length}\n' \
                f'Max Length: {labeled_column.max_id_length}'

        case 'TextColumn':
            assert isinstance(labeled_column, TextColumn)
            title = \
                f'{column_name} (Text)\n' \
                f'Min Length: {labeled_column.min_text_length}\n' \
                f'Avg Length: {labeled_column.avg_text_length}\n' \
                f'Max Length: {labeled_column.max_text_length}'

        case 'CategoriesColumn':
            assert isinstance(labeled_column, CategoriesColumn)
            title = \
                f'{column_name} (Categories)\n' \
                f'#Categories: {len(labeled_column.categories)}'

        case 'FloatColumn':
            assert isinstance(labeled_column, FloatColumn)
            title = \
                f'{column_name} (Float)\n' \
                f'Min: {labeled_column.min_value}\n' \
                f'Avg: {labeled_column.avg_value}\n' \
                f'Max: {labeled_column.max_value}\n' \
                f'Stddev: {labeled_column.value_stddev}'

        case 'WGS84CoordinateColumn':
            raise RuntimeError(
                f'{labeled_column} cannot be of abstract type '
                f'WGS84CoordinateColumn'
            )

        case 'WGS84LatitudeColumn':
            assert isinstance(labeled_column, WGS84LatitudeColumn)
            title = \
                f'{column_name} (WGS84 Latitude)\n' \
                f'Min: {labeled_column.min_value}\n' \
                f'Avg: {labeled_column.avg_value}\n' \
                f'Max: {labeled_column.max_value}\n' \
                f'Stddev: {labeled_column.value_stddev}'

        case 'WGS84LongitudeColumn':
            assert isinstance(labeled_column, WGS84LongitudeColumn)
            title = \
                f'{column_name} (WGS84 Longitude)\n' \
                f'Min: {labeled_column.min_value}\n' \
                f'Avg: {labeled_column.avg_value}\n' \
                f'Max: {labeled_column.max_value}\n' \
                f'Stddev: {labeled_column.value_stddev}'

        case 'DateTimeColumn':
            assert isinstance(labeled_column, DateTimeColumn)
            title = \
                f'{column_name} (Date Time)\n' \
                f'Min: {labeled_column.min_date_time}\n' \
                f'Mean: {labeled_column.mean_date_time}\n' \
                f'Max: {labeled_column.max_date_time}'
        case _:
            title = f'{column_name} (Unknown Type)'

    return title


def visualize(graph: BankGraph, save_path: str = 'graph.html') -> None:
    # initialize the network
    net = Network(
        height='879px',
        width='100%',
        bgcolor='#222222',
        font_color='white',
        notebook=True,
        select_menu=True
    )

    for node in graph.nodes():
        assert isinstance(node, SemanticLabelNode)

    nodes: List[SemanticLabelNode] = graph.nodes()
    logger.info(f'Graph has {len(nodes)} nodes')
    edges = graph.edges()
    logger.info(f'Graph has {len(edges)} edges')

    # create the nodes
    for node in nodes:
        # first we get the parameters of the node
        node_column_type = _get_column_type(node)
        node_column_name = _get_column_name(node)

        node_color = color_mapping.get(node_column_type, color_mapping['Default'])

        # the label is the name of the column
        node_label = f'{node_column_name}'

        # the shape is determined by the column type
        node_shape = shape_mapping.get(node_column_type, shape_mapping['Default'])

        # the title is the name and type of the column
        node_title = construct_node_title(node)

        # here we add the node to the network
        # the node id is the id of the SemanticLabelNode
        # the node label is the name of the column
        net.add_node(n_id=node.id,
                     label=node_label,
                     color=node_color,
                     shape=node_shape,
                     title=node_title
                     )

    # create the edges
    for edge in edges:
        net.add_edge(edge.source, edge.target)

    # show all options
    # net.show_buttons()

    # show only physics options
    # net.show_buttons(filter_=['physics'])

    # set options
    net.set_options('''const options = {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 6,
        "opacity": 1
      },
      "edges": {
        "arrows": {
          "to": {
            "enabled": true
          }
        },
        "color": {
          "inherit": true
        },
        "selfReference": {
          "angle": 0.7853981633974483
        }
      },
      "physics": {
        "barnesHut": {
          "damping": 0.22
        },
        "minVelocity": 0.1,
        "maxVelocity": 0.2
      }
    }''')

    net.show(save_path)
