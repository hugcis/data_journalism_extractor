import os
from jinja2 import Environment
from python_modules.exceptions import IntegrityError
from .unary_operation import UnaryOperation


class Split(UnaryOperation):
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.field = module.get('field')
        if self.field is None:
            raise ValueError(
                "No fields provided in projection module {}".format(module))

        self.template_path = os.path.join(self.template_path,
                                          'scala_split.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        source_length = len(
            self.named_modules.get(self.source).get_out_type())
        projection_tuple = ','.join(
            ['set._{}'.format(i + 1) if i != self.field - 1 else
             'set._{}.toLowerCase.split(" ")'.format(i + 1) for i
             in range(source_length)]
        )
        return self.template.render(
            name=self.name,
            source=self.source,
            projection_tuple=projection_tuple
        ), ''

    def get_out_type(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        return_type = []
        for i, s_type in enumerate(source_type):
            if i == self.field - 1:
                return_type.append("Array[{}]".format(s_type))
            else:
                return_type.append(s_type)
        return return_type

    def check_integrity(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        if source_type[self.field - 1] != "String":
            raise IntegrityError(
                "Trying to splint incorrect type for module {}. {} not \
splittable".format(self.name, source_type[self.field - 1]))
