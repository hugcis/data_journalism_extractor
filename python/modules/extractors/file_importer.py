""" The file importer operation module base class
"""
import os
from abc import ABC, abstractmethod
from extractor_exceptions import IntegrityError
from modules.base_module import BaseModule


class FileImporter(BaseModule, ABC):
    """ File Importer is an abstract class that is used for
    building modules that read files on disk.

    **It cannot be used by as is because it is an abstract class**.

    Args:
        module (dict): The module dict must have a ``path`` field
            that contains the path to the file to be read by the module
            (Ex: ``~/project/file.csv``).
    """
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.file_path = module.get('path')

        if self.file_path is None:
            raise ValueError(
                'path not provided in module {}'.format(module))
        self.file_path = os.path.expanduser(self.file_path)

        self.template_path = 'importers'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass

    def check_integrity(self):
        if not os.path.exists(self.file_path):
            raise IntegrityError("File {} not in path".format(self.file_path))
