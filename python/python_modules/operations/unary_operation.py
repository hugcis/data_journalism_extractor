from abc import ABC, abstractmethod
from . import BaseModule


class UnaryOperation(BaseModule, ABC):
    def __init__(self, module, env, named_modules):
        super().__init__(module, env, named_modules)
        self.source = module.get('source')

        if self.source is None:
            raise ValueError(
                'The source was not provided in module {}'.format(module))

        self.template_path = 'operations'

    @abstractmethod
    def rendered_result(self) -> (str, str):
        pass
