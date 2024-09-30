# Joint Strategy Analysis Toolkit (JSAT)

JSAT contains a program for generating network graphs of work strategies for human-machine teams in Python. 

## Getting Started

Simply clone this repository and work in your favorite IDE. If using this toolkit to conduct your own analyses, we suggest adding this repository as a git submodule to your own repository.

```
cd <your target folder>
git init
git submodule add https://github.com/mijtsma/jsat.git libs/jsat
```

You can then copy the ``data`` folder and the script file of your choice (such as ``userapps/COPYME/script.py``) from ``libs/jsat`` to your main directory, and you have your own repository.

All of the required Python packages are listed in `requirements.txt`.

To install the required packages:
```
pip install -r requirements.txt
```

You also need to add the project directory or submodule directory to your PYTHONPATH. This can be done manually as seen [here](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). Most IDEs should also support project-based PYTHONPATH additions through environments or launch configurations, which is a good practice if you wish to keep PYTHONPATH uncluttered.

## Usage

### Running Example Python Script
A simple example project script can be found at `cytoapp/script.py`. This script demonstrates examples of the various core modules in action.

This script also creates a visualization which runs on a web application powered by Dash. The files responsible for this app include `cytoapp/cytoscapeapp.py`, which runs the app, and `cytoapp/datahandler.py`, which keeps track of the network models.

Running `cytoapp/script.py` will print some statistics, then the following message will appear.
```
Dash is running on http://127.0.0.1:8050/
```
Follow this link to the server the application is running on. 

The visualization produced is a directed network of function and resource nodes. This application is interactive and has the following capabilities:
1. Toggle the visualization style between a layered, standard, and allocation-based formats
2. Toggle the layout between the dagre, code-bilkent, and concentric positioning algorithms
3. Drag nodes/groups to fine-tune the layout
4. Download the current state of the graph as a .jpg, .png, or .svg image
5. View statistics based on the entire graph, the most recently clicked node, or the modularity of the current visualization

### Creating User Projects
User projects are stored in the `userapps` directory. To get started, copy and rename `userapps/COPYME` to your name. This will be your personal directory, where you can create any projects you would like. An example `script.py` is provided for convenience. Note that because of the way Python handles directories, you will need a file named `__init__.py` in any sub-directory you create.

An elaborate example of a user project can be found at `userapps/robot_example/script.py`. A tutorial for this example can be found at `userapps/robot_example/README.md`.

### Data Files
Network information is stored in JSON data files, located in `data/JSON`. Standards for this format are located in `JSONStandards.txt`.

### Networkx
[Networkx](https://networkx.org/documentation/stable/index.html) is used to represent node and edge relationships as a part of the `NetworkModel` class, located at `core\networkdata\networkmodel.py`. This allows for easy computation of various graph statistics using the Networkx package, as seen in `core/calculation/basicstats.py`.

### Dash
[Dash](https://dash.plotly.com/) is Plotly's framework for building data visualization applications and is written on top of Flask. Visualizing the networks in a web application allows for more flexibility and interaction with the user. Each interactive item on the page is a "dash core component" and from the `dash_core_components` module. There is also a `dash_html_components` module that allows you to control the arrangement of core components on the page.

**add more about callbacks

### Dash Cytoscape
The [Dash Cytoscape](https://dash.plotly.com/cytoscape) graphing library is used to create interactive visualizations of the networks. This library is an extension of [Cytoscape](https://js.cytoscape.org/), and features support for Dash apps and callbacks. Network models can  be converted to Dash Cytoscape format using the visualizers in `core/visualization`.

**add core description

## Future Work
Currently, the networks that these programs generate are manually inspected to identify key interdependencies between human and robotic teammates in the work environment. This is done by looking for certain patterns in the work environment that can indicate a specific opportunistic interdependency. For example, when two different agents are completing related work simultaneously, this presents an opportunity for one agent to update the other on their progress.

We believe that this inspection might be automated by modifying the program to search for these patterns in the network, generating suggestions for opportunistic interdependencies that might be present in the work environment.

## Authors

Cadence Hagenauer   hagenauer.1@osu.edu

Dr. Martijn IJtsma  ijtsma.1@osu.edu

Katie Albert    albert.224@osu.edu

James Bartman   jbartman47@berkeley.edu

