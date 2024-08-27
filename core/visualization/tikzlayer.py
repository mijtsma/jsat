import networkx as nx
from typing import TextIO, Tuple

import core.networkdata as nd
from core.utils.tikzutils import TikzUtils

class LayeredTikzVisualizer:
    ''' A class for creating tikz visualizations of a NetworkModel with
        layers based on node type.
    '''

    @staticmethod
    def visualize(
        model: nd.NetworkModel, 
        path: str,
        node_positions: dict[str, Tuple[float, float]] = None,
        node_layers: dict[type, int] = TikzUtils.default_tikz_node_layers(),
        node_size: float = 0.3,
        font_size: str = "tiny",
        line_weight: float = 0.5,
        pos_precision: int = 3,
        layer_size: Tuple[float,float] = (5,3),
        margin: float = None
    ):
        ''' Generates a tikz visualization of a specified NetworkModel layered
            by node type and outputs it to a specified file path.
            If no node_positions dict is specified, it is generated with
            a spring physics sim.
            All node types present in model must have an entry in node_layers,
            otherwise an exception is thrown.
            font_size accepts any LATEX font size. (tiny, scriptsize,
            small, etc.)
            pos_precision specifies the number of decimal places given 
            node coordinates will be rounded to to make the resulting
            file cleaner.
            layer_size specifies the (width, height) of a layer in the graph
            margin specifies a border margin where no nodes will be placed 
            within a layer of the graph. This is node_size by default.
        '''
        if node_positions is None:
            node_positions = TikzUtils.generate_positions(model)

        if margin is None:
            margin = node_size

        LayeredTikzVisualizer.__fill_layers(
            model, 
            node_positions, 
            layer_size,
            margin
        )

        with open(path, "w") as output:
            TikzUtils.add_file_header(output, True)

            #style
            output.write("\\SetPlaneWidth{" + str(layer_size[0]) + "}\n")
            output.write("\\SetPlaneHeight{" + str(layer_size[1]) + "}\n")
            output.write("\\SetLayerDistance{-" + str(layer_size[1]) + "}\n")
            output.write("\\SetVertexStyle[FillColor=white]")

            #layers
            for name, number in node_layers.items():
                output.write("\\Plane[layer=" + str(number) + "]\n")
                output.write("\\Text[layer=" + 
                    str(number) + 
                    ",position=above right,rotation=90]{" +
                    name.__name__ +
                    "}\n")

            #nodes
            for node_id in model.get_node_ids():
                node_type: type = type(model.get_node(node_id))
                layer_str: str = "layer=" + str(node_layers[node_type])
                TikzUtils.add_node_line(
                    model.get_node(node_id),
                    output,
                    node_positions,
                    node_size,
                    font_size,
                    pos_precision,
                    layer_str
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

            #key
            x_pos = 1.5 * node_size
            y_pos = layer_size[1] * len(node_layers) * -0.8
            TikzUtils.add_key(model, output, x_pos, y_pos, node_size, line_weight)

            TikzUtils.add_file_footer(output)

    @staticmethod
    def __fill_layers(
        model: nd.NetworkModel, 
        node_positions: dict[str, Tuple[float, float]],
        layer_size: Tuple[float,float],
        margin: float
    ):
        ''' Modifies node_positions so that each layer is filled.
        '''
        #get current layer bounds
        layer_bounds: dict[type, dict[str,Tuple[float,float]]] = {}
        for node_id in model.get_node_ids():
            LayeredTikzVisualizer.__adjust_layer_bounds(
                model, 
                node_positions, 
                node_id, 
                layer_bounds
            )
        #move bounds to specified layer size
        for node_id in model.get_node_ids():
            LayeredTikzVisualizer.__shift_node(
                model, 
                node_positions,
                node_id,
                layer_bounds,
                layer_size,
                margin
            )

    @staticmethod
    def __adjust_layer_bounds(
        model: nd.NetworkModel, 
        node_positions: dict[str, Tuple[float, float]],
        node_id: str,
        layer_bounds: dict[type, dict[str,Tuple[float,float]]]
    ):
        ''' updates layer bounds based on the position of the passed node
        '''
        current_type = type(model.get_node(node_id))
        if current_type not in layer_bounds:
            new_bounds: dict[str,Tuple[float,float]] = {}
            new_bounds["min"] = node_positions[node_id].copy()
            new_bounds["max"] = node_positions[node_id].copy()
            layer_bounds[current_type] = new_bounds
            return
        min_x_pos: float = layer_bounds[current_type]["min"][0]
        min_y_pos: float = layer_bounds[current_type]["min"][1]
        max_x_pos: float = layer_bounds[current_type]["max"][0]
        max_y_pos: float = layer_bounds[current_type]["max"][1]
        current_x_pos: float = node_positions[node_id][0]
        current_y_pos: float = node_positions[node_id][1]
        if current_x_pos < min_x_pos:
            layer_bounds[current_type]["min"][0] = current_x_pos
        if current_x_pos > max_x_pos:
            layer_bounds[current_type]["max"][0] = current_x_pos
        if current_y_pos < min_y_pos:
            layer_bounds[current_type]["min"][1] = current_y_pos
        if current_y_pos > max_y_pos:
            layer_bounds[current_type]["max"][1] = current_y_pos

    @staticmethod
    def __shift_node(
        model: nd.NetworkModel, 
        node_positions: dict[str, Tuple[float, float]],
        node_id: str,
        layer_bounds: dict[type, dict[str,Tuple[float,float]]],
        layer_size: Tuple[float,float],
        margin: float
    ):
        ''' shifts the specified node's position into the layer bounds
        '''
        current_type = type(model.get_node(node_id))
        for index in range(2):
            old_min: float = layer_bounds[current_type]["min"][index]
            old_max: float = layer_bounds[current_type]["max"][index]
            old_diff: float = old_max - old_min
            if old_diff == 0: 
                node_positions[node_id][index] = layer_size[index] / 2
            else:
                old_pos: float = node_positions[node_id][index]
                new_range: float = layer_size[index]
                node_positions[node_id][index] = ((old_pos - old_min) *
                (new_range - 2 * margin) / old_diff) + margin
                