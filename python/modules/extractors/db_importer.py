""" The Database loader operation module
"""
import os
from typing import Tuple
import graphviz
from jinja2 import Environment
from modules.base_module import BaseModule
from modules.utils import quote, format_types

DB_DRIVERS = {
    'postgresql': 'org.postgresql.Driver'
}


class DbImporter(BaseModule):
    """ Main database loader operation module class.

    Args:
        module (dict): The module dict must have:

            * A ``dbUrl`` field with the database entrypoint for JDBC. (e.g
              for a Postgres db named test running on localhost
              ``"jdbc:postgresql://localhost/test"``).
            * A ``dataType`` field with the input data types (Ex:
              ``["String", "Int", "Double"]``).
            * The names of the desired columns in ``fieldNames``
              (Ex: ``["age", "date", "name"]``).
            * The ``query`` to be interpreted by the db.


            Other optional fields are:
                * ``filterNull`` a boolean value for filtering null values from
                  the db output.

    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.db_url = module.get('dbUrl')
        self.db_type = self._get_db_type()

        if module.get('dataType') is None:
            raise ValueError(
                "No dataType provided for module {}".format(module))

        self.data_type = module.get('dataType')
        self.field_names = module.get('fieldNames')
        self.query = module.get('query')
        self.filter_null = module.get('filterNull', False)
        self.driver = DB_DRIVERS.get(self.db_type)
        if self.driver is None:
            raise ValueError(
                "No known driver for this\
 database type : {}".format(self.module_type))

        self.template_path = os.path.join('importers',
                                          'scala_db_loader.template')
        self.template_ext_path = os.path.join('importers',
                                              'scala_db_loader_ext.template')
        self.template = self.env.get_template(self.template_path)
        self.template_ext = self.env.get_template(self.template_ext_path)

    def rendered_result(self) -> Tuple[str, str]:
        return self.template.render(
            name=self.name,
            field_types=['createTypeInformation[{}]'.format(i) for
                         i in self.data_type],
            field_names=[quote(i) for i in self.field_names],
            data_type=format_types(self.data_type),
            driver=self.driver,
            db_url=self.db_url,
            query=self.query,
            filter_null=self.filter_null,
            filter_fields=['t._{} != null'.format(i + 1) for i
                           in range(len(self.data_type))]
        ), self.template_ext.render()

    def get_out_type(self):
        return self.data_type

    def check_integrity(self):
        pass

    def add_to_graph(self, graph: graphviz.Digraph):
        graph.node(str(hash(self)),
                   label=self.to_graph_repr(),
                   fillcolor='green',
                   style='filled',
                   shape='cylinder')

    def _get_db_type(self):
        return self.db_url.split(':')[1]
