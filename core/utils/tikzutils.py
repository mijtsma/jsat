from typing import Tuple, TextIO
import networkx as nx

import core.networkdata as nd
from core.utils.colorgen import ColorGenerator

class TikzUtils:
    ''' A class for common tikz visualization operations.
    '''

    @staticmethod
    def default_tikz_node_layers() -> dict[type, int]:
        ''' Returns the dict specifying the default layer order in a tikz
            picture.
        '''
        return{
            nd.BaseEnvironmentResource: 4,
            nd.DistributedWorkFunction: 3,
            nd.CoordinationGroundingResource: 2,
            nd.SynchronyFunction: 1
        }

    @staticmethod
    def add_file_header(output: TextIO, is_multilayer: bool = False): 
        ''' Prints the header of a tikz file to the given output
        '''
        output.write("\\documentclass{standalone}\n")
        output.write("\\usepackage{tikz-network}\n")
        output.write("\\begin{document}\n")
        output.write("\\begin{tikzpicture}")
        if(is_multilayer):
            output.write("[multilayer=3d]")
        output.write("\n")

    @staticmethod
    def add_file_footer(output: TextIO):
        ''' Prints the footer of a tikz file to the given output
        '''
        output.write("\\end{tikzpicture}\n")
        output.write("\\end{document}\n")

    @staticmethod
    def generate_positions(model: nd.NetworkModel):
        ''' Generates node positions of a NetworkModel using a physics sim.
        '''
        print("\nGenerating node positions...\n")
        graph: nx.DiGraph = model.get_graph()
        node_positions = nx.spring_layout(
            graph,
            pos=nx.kamada_kawai_layout(graph), 
            iterations = 5000, 
            scale=5
        )
        print("Sim complete!\n")
        return node_positions

    @staticmethod
    def add_node_line(
        node: nd.Node,
        output: TextIO,
        node_positions: dict[str, Tuple[float, float]],
        node_size: float,
        font_size: str,
        pos_precision: int,
        custom_properties: str = ""
    ):
        ''' Adds a line for the given node to the given .tex file.
        '''
        x_pos = round(node_positions[node.id][0], pos_precision)
        y_pos = round(node_positions[node.id][1], pos_precision)
        action_modifier = ""
        if issubclass(node.__class__, nd.ActionNode):
            if node.has_authorized_agent():
                agent: nd.Agent = node.get_authorized_agent()
                action_modifier = ("shape=rectangle,RGB,color=" + 
                    ColorGenerator.get_pastel_tikz_color(agent.id))
            else:
                action_modifier = "shape=rectangle"

        output.write("\\Vertex[x=" + 
            str(x_pos) +
            ",y=" + 
            str(y_pos) + 
            ",size=" +
            str(node_size)+
            ",label=" +
            node.id +
            ",fontsize=\\" +
            font_size +
            "," +
            custom_properties + 
            "," +
            action_modifier +
            "]{" + node.id + "}" + "\n"
        )

    @staticmethod
    def add_edge_line(
        source_id: str,
        target_id: str,
        model: nd.NetworkModel, 
        output: TextIO,
        line_weight: float
    ):
        ''' Adds a line for the given edge to the given .tex file.
        '''
        org_modifier: str = ""
        source_type: type = type(model.get_node(source_id))
        target_type: type = type(model.get_node(target_id))
        if source_type == target_type:
            org_modifier = ",style={dashed}"
        output.write("\\Edge[Direct,lw=" + 
            str(line_weight) +
            "pt" +
            org_modifier +
            "](" + 
            source_id + 
            ")(" +
            target_id+
            ")" + "\n"
        )

    @staticmethod
    def add_key(
        model: nd.NetworkModel,
        output: TextIO,
        x_pos: float,
        y_pos: float,
        node_size: float,
        line_weight: float
    ):
        ''' Adds a key detailing agents and edges to the given .tex file.
        '''
        index = 0
        for agent_id in model.agents:
            node_id = "agent"+str(index+1)
            output.write(
                "\\Vertex[x=" +
                str(round(x_pos,3)) +
                ",y=" +
                str(round(y_pos - node_size * 1.5 * index,3)) +
                ",size=" +
                str(node_size) + 
                ",shape=rectangle,RGB,color=" +
                ColorGenerator.get_pastel_tikz_color(agent_id) +
                ",label=" +
                agent_id +
                ",position=0]{"+
                node_id +
                "}\n"
            )
            index += 1
        output.write(
            "\\Vertex[x=0,y=" +
            str(round(y_pos - node_size * 1.5 * index,3)) +
            ",size=0]{e11}\n" +
            "\\Vertex[x=" +
            str(round(3 * node_size,3)) + 
            ",y=" +
            str(round(y_pos - node_size * 1.5 * index,3)) +
            ",size=0,label=Organizational Dependancy,position=0]{e12}\n" +
            "\\Edge[Direct,lw=" +
            str(line_weight) +
            "pt,style={dashed}](e11)(e12)\n"
        )
        output.write(
            "\\Vertex[x=0,y=" +
            str(round(y_pos - node_size * 1.5 * (index + 1),3)) +
            ",size=0]{e21}\n" +
            "\\Vertex[x=" +
            str(round(3 * node_size,3)) + 
            ",y=" +
            str(round(y_pos - node_size * 1.5 * (index + 1),3)) +
            ",size=0,label=Action Means-End Relationship,position=0]{e22}\n" +
            "\\Edge[Direct,lw=" +
            str(line_weight) +
            "pt](e21)(e22)\n"
        )