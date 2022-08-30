import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import matplotlib.pyplot as plt
import ruamel.yaml as yaml
from importlib.machinery import SourceFileLoader
from relationships import *

def debug_planning(files):
    # Debug planning process.
    relationships = []
    for file in files:
        with open(file, "r") as f:
            rel_file = yaml.round_trip_load(f)
            relationships += rel_file["relationships"]
            
            bindings_file = rel_file["file"]
            SourceFileLoader(
                bindings_file,
                os.path.join(os.path.dirname(file), bindings_file)
            ).load_module()
    plan, G = Register._plan([Register._get_relationship(rel) for rel in relationships])

    fig, axes = plt.subplots(nrows=1, ncols=1)
    # ax = axes.flatten()

    nx.draw(
        G,
        nx.drawing.nx_pydot.graphviz_layout(G, prog="twopi"),
        with_labels=True,
        # ax=ax[0]
    )
    # ax[0].set_axis_off()

    """ This isn't a network! I don't know why I thought it was a good idea to display it as a network... (I guess it may be kinda useful). """
    # G_plan = nx.DiGraph()
    # for i, dependency in enumerate(plan):
    #     if i != len(plan) - 1:
    #         next = plan[i + 1]
    #         print(dependency["name"], "->", next["name"])
    #         G_plan.add_edge(dependency["name"], next["name"])

    # nx.draw(G_plan, with_labels=True, ax=ax[1])
    # ax[1].set_axis_off()
    # print([x["name"] for x in plan])
    print("Relationship processing plan:", [rel["name"] for rel in plan])
    plt.show()

if __name__ == "__main__":
    import sys
    import os
    if len(sys.argv) == 1:
        print("Please provide the path to one or more config files as positional arguments.")
        sys.exit(1)
    relationship_files = [os.path.join(os.path.dirname(__file__), f) for f in sys.argv[1:]]
    debug_planning(relationship_files)