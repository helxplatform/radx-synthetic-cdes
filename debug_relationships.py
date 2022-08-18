import matplotlib.pyplot as plt
import ruamel.yaml as yaml
from relationships import *

def debug_planning(file):
    # Debug planning process.

    with open(file, "r") as f:
        relationships = yaml.round_trip_load(f)["relationships"]
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
    try:
        relationship_file = os.path.join(os.path.dirname(__file__), sys.argv[1])
    except:
        print("Please provide the path to a relationships config file as the first positional argument.")
        sys.exit(1)
    debug_planning(relationship_file)