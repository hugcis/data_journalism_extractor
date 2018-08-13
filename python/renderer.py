""" Module containing the render engine
"""
from jinja2 import Environment, FileSystemLoader
from graphviz import Digraph
from modules.base_module import BaseModule
from modules.extractors import (CsvImporter,
                                JsonImporter,
                                DbImporter,
                                MongoImporter)
from modules.operations import (Join,
                                ExtractorLink,
                                Projection,
                                Union,
                                Split,
                                ExtractorWordSimilarity,
                                Map,
                                CountDistinct)
from modules.outputs import CsvOutput
from extractor_exceptions import UnknownModuleError, IntegrityError


class ModuleMap:
    """ The main mapping that links modules
    to their name through the ``get`` method.

    (Essentially an enum or dictionary)
    """
    # Wrapped in a class for clarity
    # pylint: disable=R0903

    module_map = {
        # Importers
        'csvImporter': CsvImporter,
        'jsonImporter': JsonImporter,
        'dbImporter': DbImporter,
        'mongoImporter': MongoImporter,
        # Binary ops
        'join': Join,
        'extractorLink': ExtractorLink,
        'extractorWordSim': ExtractorWordSimilarity,
        # Unary ops
        'projection': Projection,
        'union': Union,
        'split': Split,
        'map': Map,
        'countDistinct': CountDistinct,
        # Outputs
        'csvOutput': CsvOutput,
    }

    @classmethod
    def get(cls, module_type: str) -> BaseModule:
        """ Returns the module corresponding to the name
        passed in argument.

        Args:
            module_type (str): The desired module type.
        """
        return cls.module_map.get(module_type)


class Renderer:
    """ The render engine that can build the DAG, check the integrity of
    the operation graph and generate the rendered Scala code.

    Args:
        module_list (List[dict]): The list of module specifications to be
            parsed and added to the operation graph.
        template_dir (str): The path to the template directory.
    """
    def __init__(self, module_list, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.name_list = []
        self.named_modules = {}
        for module in module_list:
            self._add_module(module)

        if len(self.name_list) != len(set(self.name_list)):
            raise IntegrityError("Some modules have the same name")

    def check_integrity(self):
        """ Check the integrity of the graph. Should be called
        after all the modules have been added to the graph (i.e. after
        initialization).
        """
        for module in self.named_modules:
            self.named_modules[module].check_integrity()

    def get_rendered(self):
        """ Get the rendered code from the module list.
        """
        rendered = []
        rendered_ext = []

        for name in self.name_list:
            mod = self.named_modules.get(name)
            if mod is not None:
                rend, rend_ext = mod.rendered_result()
                rendered.append(rend)
                if rend_ext:
                    rendered_ext.append(rend_ext)

        # Ensure that we don't write general purpose external
        # helpers multiple times
        rendered_ext = list(set(rendered_ext))
        return rendered, rendered_ext

    def render_pdf_graph(self):
        """ Create the `graphviz <https://graphviz.gitlab.io/>`_ Digraph
        and render the pdf output graph.
        """
        graph = Digraph('compiled', graph_attr={'rankdir': 'LR'})
        for mod in self.name_list:
            self.named_modules.get(mod).add_to_graph(graph)
        graph.render('compiled.gv')

    def _add_module(self, module):
        name = module.get('name')
        self.name_list.append(name)

        base_module = ModuleMap.get(
            module.get('type'))

        if base_module is None:
            raise UnknownModuleError(
                "Module is {}".format(module.get('type')))

        self.named_modules[name] = base_module(module,
                                               self.env,
                                               self.named_modules)
