""" The abstract class for unary operation modules.
"""
from typing import Tuple
from abc import ABC, abstractmethod
from graphviz import Digraph
from modules.utils import format_types
from modules.base_module import BaseModule


class UnaryOperation(BaseModule, ABC):
    """ The Unary operation base abstract class.

    Args:
        module (dict): The module must contain a ``source`` field
            with the name of the incoming data flow.
    """
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.source = module.get('source')

        if self.source is None:
            raise ValueError(
                'The source was not provided in module {}'.format(module))

        self.template_path = 'operations'

    @abstractmethod
    def rendered_result(self) -> Tuple[str, str]:
        pass

    def add_to_graph(self, graph: Digraph):
        super().add_to_graph(graph)

        graph.edge(
            self.named_modules.get(self.source).to_graph_repr(),
            self.to_graph_repr(),
            label=format_types(
                self.named_modules.get(self.source).get_out_type()))
