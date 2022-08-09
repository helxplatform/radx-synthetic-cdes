import networkx as nx

class Register:
    udfs = {}
    relationships = {}
    @classmethod
    def register_udf(cls, name, func):
        cls.udfs[name] = func
    @classmethod
    def register_relationship(cls, name, udf, dependencies, modifies):
        cls.relationships[name] = {
            "name": name,
            "dependencies": dependencies,
            "modifies": modifies,
            "udf": udf
        }
    @classmethod
    def _get_relationship(cls, yaml_spec):
        name = yaml_spec["name"]
        args = yaml_spec.get("args", [])
        kwargs = yaml_spec.get("kwargs", {})

        relationship = cls.relationships[name]

        relationship["args"] = args
        relationship["kwargs"] = kwargs

        return relationship
        
    @classmethod
    def invoke_udf(cls, udf_name, *args, **kwargs):
        return cls.udfs[udf_name](
            *args,
            **kwargs
        )
    @classmethod
    def invoke_relationship(cls, relationship, full_record):
        name = relationship["name"]
        dependencies = relationship["dependencies"]
        modifies = relationship["modifies"]
        ret_val = cls.invoke_udf(
            relationship["udf"],
            {variable: full_record[variable] for variable in full_record if variable in dependencies},
            *relationship.get("args", []),
            **relationship.get("kwargs", {})
        )
        if ret_val is not None:
            for variable in ret_val:
                if variable not in modifies:
                    raise Exception(f'Attempted modification of variable "{variable}" in relationship "{name}" but not listed under its `modifies` field.')
        return ret_val
        
    @classmethod
    def plan(cls, relationships):
        """
        Generate a plan (path) of generation for the relationships.
            E.g. there are two relationships:
            1) requires nih_disability -> modifies nih_blind
            2) requires nih_blind -> modifies nih_diabetes (nonsense example)
        Then the plan needs to handle relationship 1 before relationship 2.
        """
        relationships = [cls._get_relationship(relationship) for relationship in relationships]
        plan, G = cls._plan(relationships)
        return plan
    @classmethod
    def _plan(cls, relationships):
        """
        Use a DAG to plan relationship order.

        This could probably be implemented more efficiently (without including a large dependency like networkx)
        but it doesn't really seem worth the effort to implement a tree dependency planner by hand.
        """
        G = nx.DiGraph()
        for relationship in relationships:

            dependencies = relationship["dependencies"]
            modifies = relationship["modifies"]

            # is_modified_by = [
            #     relationship for relationship in relationships
            #     if any([dependency for dependency in dependencies if dependency in relationship["modifies"]])
            # ]
            # modified_relationships = [
            #     relationship for relationship in relationships
            #     if any([modified for modified in modifies if modified in relationship["dependencies"]])
            # ]


            for dependency_variable in dependencies:
                # for response in dependencies[dependency_variable]:
                for modified_variable in modifies:
                    # modified_response = modifies[modified_variable]
                    G.add_edge(
                        f"{dependency_variable}",
                        f"{modified_variable}"
                    )

        # Not super familiar with this area of network/graph theory and constructing & traversing dependency trees.
        # I think that this is the proper implementation in networkx, but I haven't tested it very thoroughly.
        dependency_path = list(nx.topological_sort(G))
        plan = []
        for dependency in dependency_path:
            variable_name = dependency
            # variable_name = dependency.split(":")[0]
            # response_name = dependency.split(":")[1]
            for relationship in relationships:
                if (
                    variable_name in relationship["dependencies"]
                    # response_name in relationship["dependencies"][variable_name]
                ):
                    plan.append(relationship)
        #     [
        #         relationship for relationship in relationships
        #         if (
        #             dependency_node["variable_name"] in relationship["dependencies"] and
        #             dependency_node["response_name"] in relationship["dependencies"][dependency_node["variable_name"]]
        #         )
        #     ] for dependency_node in dependency_path
        # ]

        return plan, G

"""
A UDF is used as an escape hatch in response_value_generator for more sophisticated generation.
Relationships also use self-registered UDFs. 
"""
def udf(name):
    def decorator(func):
        Register.register_udf(
            name,
            func
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

"""
A relationship is a means of post-processing related fields after initial record generation.
Essentially, a UDF to modify a field which is dependent on another (ex: education affects employment).
"""
def relationship(name, dependencies, modifies):
    def decorator(func):
        udf_name = f"__relationship_udf:{name}__"
        Register.register_udf(
            udf_name,
            func
        )
        Register.register_relationship(
            name,
            udf_name,
            dependencies,
            modifies
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

def debug_planning(file):
    # Debug planning process.
    import matplotlib.pyplot as plt
    import ruamel.yaml as yaml

    with open(file, "r") as f:
        relationships = yaml.round_trip_load(f)["relationships"]
    plan, G = Register._plan([Register._get_relationship(rel) for rel in relationships])

    fig, axes = plt.subplots(nrows=2, ncols=1)
    ax = axes.flatten()

    nx.draw(G, nx.drawing.nx_pydot.graphviz_layout(G, prog="twopi"), with_labels=True, ax=ax[0])
    ax[0].set_axis_off()

    G_plan = nx.DiGraph()
    for i, dependency in enumerate(plan):
        if i != len(plan) - 1:
            next = plan[i + 1]
            print(dependency["name"], "->", next["name"])
            G_plan.add_edge(dependency["name"], next["name"])

    nx.draw(G_plan, with_labels=True, ax=ax[1])
    ax[1].set_axis_off()
    print([x["name"] for x in plan])
    plt.show()