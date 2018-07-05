from abc import ABC, abstractmethod
from . import BaseModule


class FileOutput(BaseModule, ABC):
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

        self.template_path = 'outputs'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass
