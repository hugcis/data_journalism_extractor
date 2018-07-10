from jinja2 import Environment, FileSystemLoader
from python_modules.extractors import CsvImporter, JsonImporter, DbImporter
from python_modules.operations import (Join,
                                       ExtractorLink,
                                       Projection,
                                       Union,
                                       Split,
                                       ExtractorWordSimilarity)
from python_modules.outputs import CsvOutput
from python_modules.exceptions import UnknownModuleError
from python_modules.base_module import BaseModule


class ModuleMap:
    module_map = {
        # Importers
        'csvImporter': CsvImporter,
        'jsonImporter': JsonImporter,
        'dbImporter': DbImporter,
        # Binary ops
        'join': Join,
        'extractorLink': ExtractorLink,
        'extractorWordSim': ExtractorWordSimilarity,
        # Unary ops
        'projection': Projection,
        'union': Union,
        'split': Split,
        # Outputs
        'csvOutput': CsvOutput,
    }

    @classmethod
    def get(cls, name: str) -> BaseModule:
        """ Returns the module corresponding to the name
        passed in argument.
        """
        return cls.module_map.get(name)


class Renderer:
    def __init__(self, module_list, template_dir: str):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.name_list = []
        self.named_modules = {}
        for module in module_list:
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

    def check_integrity(self):
        """ Check the integrity of the graph
        """
        for module in self.named_modules:
            self.named_modules[module].check_integrity()

    def get_rendered(self):
        """ Get the rendered code from the module list
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

        return rendered, rendered_ext
