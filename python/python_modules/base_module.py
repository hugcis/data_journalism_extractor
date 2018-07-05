from abc import ABC, abstractmethod
from jinja2 import Environment
from graphviz import Digraph


class BaseModule(ABC):
    def __init__(self, module, env: Environment, named_modules):
        self.env = env
        self.type = module.get('type')
        self.name = module.get('name')
        if self.name is None:
            raise ValueError('Name not provided in module {}'.format(module))

        self.named_modules = named_modules

    def __str__(self):
        return self.name

    def add_to_graph(self, graph: Digraph):
        graph.node(self.__str__())

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass

    @abstractmethod
    def get_out_type(self):
        pass

    @abstractmethod
    def check_integrity(self):
        pass
