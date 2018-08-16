""" The split operation module
"""
import os
from jinja2 import Environment
from extractor_exceptions import IntegrityError
from modules.operations.unary_operation import UnaryOperation


class Split(UnaryOperation):
    """ A module that split a given string field from an incoming
    dataflow according to a regex.
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.field = module.get('field')
        self.delimiter = module.get('delimiter', ' ').replace('\\', '\\\\')
        self.reduce = module.get('reduce')

        if self.field is None:
            raise ValueError(
                "No fields provided in projection module {}".format(module))

        if not isinstance(self.reduce, int) and self.reduce is not None:
            raise ValueError(
                "Wrong reduce parameter {}, must be Int or \
null".format(self.reduce)
            )

        self.template_path = os.path.join(self.template_path,
                                          'scala_split.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        source_length = len(
            self.named_modules.get(self.source).get_out_type())
        projection_tuple = ','.join(
            ['set._{}'.format(i + 1) if i != self.field - 1 else
             self._get_main_render(i + 1)
             for i in range(source_length)]
        )
        return self.template.render(
            name=self.name,
            source=self.source,
            projection_tuple=projection_tuple
        ), ''

    def _get_main_render(self, index):
        if self.reduce is None:
            return 'set._{}.toLowerCase.split("{}")'.format(index,
                                                            self.delimiter)
        elif self.reduce == -1:
            return 'set._{}.toLowerCase.split("{}")(set._{}.toLowerCase.split\
("{}").length - 1)'.format(index, self.delimiter, index, self.delimiter)

        return 'set._{}.toLowerCase.split("{}").length match {{ case 1\
 => set._{}.toLowerCase.split("{}")(0) case _ => set._{}.toLowerCase.\
split("{}")({})}}'.format(index, self.delimiter, index, self.delimiter, index,
                          self.delimiter, self.reduce - 1)

    def get_out_type(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        return_type = []
        for i, s_type in enumerate(source_type):
            if i == self.field - 1:
                if self.reduce is not None:
                    return_type.append(s_type)
                else:
                    return_type.append("Array[{}]".format(s_type))
            else:
                return_type.append(s_type)
        return return_type

    def check_integrity(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        if source_type[self.field - 1] != "String":
            raise IntegrityError(
                "Trying to split incorrect type for module {}. {} not \
splittable".format(self.name, source_type[self.field - 1]))
