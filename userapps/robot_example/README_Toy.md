### 🤖 Analyzing Joint Cognitive System Architectures

This Python script analyzes and compares two different **architectures** (ways of distributing tasks) in a **multi-agent joint cognitive system** using graph theory.

Go through the steps provided in the comments of toy_script.py to preparte the code, then we will begin an analysis of two system architectures!
We will be comparing Architecture 1 (Cook does everything) with Architecture 2 (work is split), observing how **node centrality** changes for different task functions, revealing shifts in the system's structure and coordination needs.

### Step 2: Choose and Run Architecture 1 (Baseline)

# This architecture assigns **all tasks** to the **Cook**, establishing a baseline for analysis.

1.  **Locate the `DEFINE ARCHITECTURE` section** in the script.
2.  **Ensure Architecture 1 is uncommented** and Architecture 2 is commented out, as shown below:

```python
     ##### Architecture 1: The Cook does everything ######
     agent_assignments = { # <-- ENSURE THIS BLOCK IS UNCOMMENTED
         "Cook": [
             "IngredientPreparing",
             "HeatAdjusting",
             "IngredientCombining",
             "ToolFetching",
             "IngredientUnpacking",
             "ItemsMoving",
         ],
         "Assistant": []
     }

     ##### Architecture 2: Cook splits original work with Assistant 50/50... ######
      agent_assignments = {  <-- ENSURE THIS BLOCK IS COMMENTED OUT
           # ... tasks
      }
     ```
3.  **Run the script** from the VS Code Integrated Terminal:
     ```bash
     python your_script_name.py
     ```
4.  The script will automatically open a web browser showing the Cytoscape visualization.

### Task 1: Record Stats
Graph Stats: Go to the bottom of the web app and click the "Graph Stats" tab. Record the total number of nodes and the total number of edges for Architecture 1.
Node Centrality (Tool/Ingredient): Click on the "Tool" resource node, then switch to the "Node Stats" tab at the bottom. Record its centrality value. Repeat this for the "Ingredient" resource node.

### Step 3: Choose and Run Architecture 2 (Coordinated)
This architecture splits the "original tasks" between the cook and assistant equally, but therefore also introduces new coordination functions.

1.  Locate the `DEFINE ARCHITECTURE` section** in the script.
2.  Ensure Architecture 2 is uncommented** and Architecture 1 is commented out, as shown below:

     ##### Architecture 1: The Cook does everything ######
    #   agent_assignments = { # <-- ENSURE THIS BLOCK IS COMMENTED OUT
    #       # ... tasks
    #   }

     ##### Architecture 2: Cook splits original work with Assistant 50/50... ######
     ##### Uncomment only one agent_assignments block at a time ######
     agent_assignments = { # <-- ENSURE THIS BLOCK IS UNCOMMENTED
         "Cook": [
             "IngredientPreparing",
             "HeatAdjusting",
             "IngredientCombining",
             "Asking for tool",      # NEW coordination task
             "Asking for ingredient",# NEW coordination task
             "Directing items",      # NEW coordination task
         ],
         "Assistant": [
             "ToolFetching",
             "IngredientUnpacking",
             "ItemsMoving",
         ],
     }
     ```
    **Run the script again:**
    ```bash
     python your_script_name.py
     ```
4.  The visualization will refresh with the new architecture.

### Analysis Task 2: Record New Stats

Graph Stats: Go to the bottom and click the "Graph Stats" tab. Notice how the total number of nodes and edges may have increased due to the addition of coordination tasks.
Node Centrality (Tool/Ingredient): Click on the "Tool" resource node and record its new centrality value from the "Node Stats" tab. Repeat for "Ingredient" resource node.

### Step 4: Compare Centrality Changes
Focus on the original tasks that were present in Architecture 1.
Compare the centrality scores of "Tool" and "Ingredient" between Architecture 1 and Architecture 2.

Key Observation: The original tasks may see an increase in centrality as the dependencies on some nodes increase as a result of needing to coordinate with other agents. This demonstrates how coordination functions create new dependencies in the system as it moves from a single agent (architecture 1) to a coordinated multi-agent structure (architecture 2).