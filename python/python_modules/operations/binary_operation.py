from abc import ABC, abstractmethod
from . import BaseModule


class BinaryOperation(BaseModule, ABC):
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
