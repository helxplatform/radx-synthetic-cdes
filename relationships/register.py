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
        dependencies = relationship["dependencies"]
        ret_val = cls.invoke_udf(
            relationship["udf"],
            full_record,
            *relationship.get("args", []),
            **relationship.get("kwargs", {})
        )
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
        return cls._plan(relationships)
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

        return plan

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