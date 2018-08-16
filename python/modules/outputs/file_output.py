""" The base class for file output modules
"""
import os
from abc import ABC, abstractmethod
from graphviz import Digraph
from modules.utils import format_types
from modules.base_module import BaseModule


class FileOutput(BaseModule, ABC):
    """ A file output module has a source and a path to a
    file.
    """
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.file_path = module.get('path')
        self.source = module.get('source')

        if self.file_path is None:
            raise ValueError(
                'filePath not provided in module {}'.format(module))
        if self.source is None:
            raise ValueError(
                'source not provided in module {}'.format(module))

        self.file_path = os.path.expanduser(self.file_path)

        self.template_path = 'outputs'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass

    def add_to_graph(self, graph: Digraph):
        super().add_to_graph(graph)

        graph.edge(
            self.named_modules.get(self.source).to_graph_repr(),
            self.to_graph_repr(),
            label=format_types(
                self.named_modules.get(self.source).get_out_type())
        )
