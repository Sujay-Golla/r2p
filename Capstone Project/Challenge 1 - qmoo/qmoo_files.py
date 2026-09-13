import glob
import json
import importlib
import networkx as nx
from pathlib import Path


def apply_qopt_qiskit24_patch():
    """Fix layout KeyError in qopt_best_practices 0.1.0 with Qiskit >= 2.4."""
    import importlib
    import qopt_best_practices.transpilation.annotated_transpilation_passes as atp

    path = Path(atp.__file__)
    text = path.read_text(encoding="utf-8")
    old = "current_layout = Layout.generate_trivial_layout(*box_dag.qregs.values())"
    new = "current_layout = Layout({bit: idx for idx, bit in enumerate(box_dag.qubits)})"
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")

    importlib.reload(atp)
    importlib.import_module(
        "qopt_best_practices.transpilation.generate_preset_qaoa_pass_manager"
    )


def load_problem(dirfn, printtxt=True):
    graphsfn = dirfn + "problem_graph_*.json"
    anglefn = dirfn + "angles.json"
    upperfn = dirfn + "upper_bounds.json"
    lowerfn = dirfn + "lower_bounds.json"
    
    if printtxt:
        print("loading", graphsfn)

    try:
        graphs = []
        num_graphs = len(glob.glob(graphsfn))
        for i in range(num_graphs):
            f = dirfn + f"problem_graph_{i}.json"
            
            with open(f, 'r') as file:
                data = json.load(file)
                # Handle NetworkX 3.0+ compatibility: convert 'links' to 'edges'
                if 'links' in data and 'edges' not in data:
                    data['edges'] = data.pop('links')
                graphs.append(nx.node_link_graph(data))
        if len(graphs) != num_graphs:
            raise Exception

    except Exception as e:
        print("Wasn't able to load graphs from " + graphsfn + ", error:" + str(e))
        return None, None, None, None
    try:
        angles = json.load(open(anglefn, 'r'))
        if len(angles) == 0:
            raise Exception
    except Exception as e:
        print("Wasn't able to load QAOA angles from " + anglefn + ", error:" + str(e))
        return None, None, None, None
    try:
        upper = json.load(open(upperfn, 'r'))
        if len(upper) == 0:
            raise Exception
    except Exception as e:
        print("Wasn't able to load upper bounds from " + upperfn + ", error:" + str(e))
        return None, None, None, None

    try:
        lower = json.load(open(lowerfn, 'r'))
        if len(lower) == 0:
            raise Exception
    except Exception as e:
        print("Wasn't able to load lower bounds from " + lowerfn + ", error:" + str(e))
        return None, None, None, None
    return graphs, angles, upper, lower
