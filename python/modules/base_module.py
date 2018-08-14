""" The module containing the abstract base class for all operation modules
used throughout the rest of the code.
"""
from abc import ABC, abstractmethod
from jinja2 import Environment
from graphviz import Digraph


class BaseModule(ABC):
    """ The abstract base class for modules. All modules are subclasses
    of ``BaseModule``

    Every module object passed to the constructor must contain the
    ``type`` and ``name`` fields.

    All modules expose the following common API.

    Args:
        module (dict): The ``dict`` containing the specification of
            the module.
        env (jinja2.Environment): The jinja environment where the
            templates can be retrieved.
        named_modules (List[BaseModule]): A list of all the other modules
            of the DAG.
    """
    def __init__(self, module: dict, env: Environment, named_modules):
        self.env = env
        self.type = module.get('type')
        self.name = module.get('name')
        if self.name is None:
            raise ValueError('Name not provided in module {}'.format(module))

        self.named_modules = named_modules

    def __str__(self):
        return self.name

    def to_graph_repr(self):
        """ Generate the representation of the node in the form

        ``Name
        Type: $type``

        Used for pdf graph generation
        """
        return self.__str__() + '\nType {}'.format(self.type)

    def add_to_graph(self, graph: Digraph):
        """ A method for adding the module to a graphviz graph
        instance.

        Args:
            graph (graphviz.dot.Digraph): A graphviz Digraph object
        """
        graph.node(self.to_graph_repr())

    @abstractmethod
    def rendered_result(self) -> (str, str):
        """ Returns a pair of strings containing the
        rendered lines of codes and external classes or objects
        definitions.
        """
        pass

    @abstractmethod
    def get_out_type(self):
        """ Returns the output type of the module
        as a list of strings.
        """
        pass

    @abstractmethod
    def check_integrity(self):
        """ Performs some check on the upstream
        modules and types when necessary to ensure the
        integrity of the DAG.
        """
        pass
