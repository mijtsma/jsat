import networkx as nx
from typing import TextIO, Tuple

import core.networkdata as nd
from core.utils.tikzutils import TikzUtils

class StandardTikzVisualizer:
    ''' A class for creating tikz visualizations of a NetworkModel with
        no grouping.
    '''

    @staticmethod
    def visualize(
        model: nd.NetworkModel, 
        path: str,
        node_positions: dict[str, Tuple[float, float]] = None,
        node_size: float = 0.3,
        font_size: str = "tiny",
        line_weight: float = 0.5,
        pos_precision: int = 3
        ):
        ''' Generates a tikz visualization of a specified NetworkModel and
            outputs it to a specified file path.
            If no node_positions dict is specified, it is generated with
            a spring physics sim.
            font_size accepts any LATEX font size. (tiny, scriptsize,
            small, etc.)
            pos_precision specifies the number of decimal places given 
            node coordinates will be rounded to to make the resulting
            file cleaner.
        '''
        if node_positions is None:
            node_positions = TikzUtils.generate_positions(model)

        with open(path, "w") as output:
            TikzUtils.add_file_header(output)

            #style
            output.write("\\SetVertexStyle[FillColor=white]")

            #nodes
            for node_id in model.get_node_ids():
                TikzUtils.add_node_line(
                    model.get_node(node_id),
                    output,
                    node_positions,
                    node_size,
                    font_size,
                    pos_precision
                )

            #edges
            for source_id, target_id in model.get_edge_ids():
                TikzUtils.add_edge_line(
                    source_id,
                    target_id,
                    model,
                    output,
                    line_weight
                )

            TikzUtils.add_file_footer(output)

   