""" The abstract class for binary operation modules.
"""
from abc import ABC, abstractmethod
from graphviz import Digraph
from . import BaseModule


class BinaryOperation(BaseModule, ABC):
    """ An binary operation module must have two sources.
    """
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.source1 = module.get('source1')
        self.source2 = module.get('source2')

        if self.source1 is None or self.source2 is None:
            raise ValueError(
                'A source was not provided in module {}'.format(module))

        self.template_path = 'operations'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass

    def add_to_graph(self, graph: Digraph):
        super().add_to_graph(graph)

        graph.edge(self.source1, self.__str__())
        graph.edge(self.source2, self.__str__())
