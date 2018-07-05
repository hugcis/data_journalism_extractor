import os
from abc import ABC, abstractmethod
from . import BaseModule
from python_modules.exceptions import IntegrityError


class FileImporter(BaseModule, ABC):
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.file_path = module.get('path')

        if self.file_path is None:
            raise ValueError(
                'path not provided in module {}'.format(module))

        self.template_path = 'importers'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass

    def check_integrity(self):
        if not os.path.exists(self.file_path):
            raise IntegrityError("File {} not in path".format(self.file_path))
