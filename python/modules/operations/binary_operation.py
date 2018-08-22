""" The abstract class for binary operation modules.
"""
from typing import Tuple
from abc import ABC, abstractmethod
from graphviz import Digraph
from modules.utils import format_types
from modules.base_module import BaseModule


class BinaryOperation(BaseModule, ABC):
    """ The abstract base module for all binary operations
    (Operations that take two data flows as input).

    Args:
        module (dict): The module dict must have the two
        fields ``source1`` and ``source2`` that contain the names
        of the two input flows.
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
    def rendered_result(self) -> Tuple[str, str]:
        pass

    def add_to_graph(self, graph: Digraph):
        super().add_to_graph(graph)

        graph.edge(
            self.named_modules.get(self.source1).to_graph_repr(),
            self.to_graph_repr(),
            label=format_types(
                self.named_modules.get(self.source1).get_out_type())
        )
        graph.edge(
            self.named_modules.get(self.source2).to_graph_repr(),
            self.to_graph_repr(),
            label=format_types(
                self.named_modules.get(self.source2).get_out_type())
        )
