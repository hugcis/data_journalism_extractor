Modules Reference
=================

Renderer
--------

.. automodule:: renderer
   :members:

Base Module
-----------

.. automodule:: modules.base_module
   :members:


.. toctree::
   :maxdepth: 3
   :caption: Module list:
   
   modules/extractors
   modules/operations
   modules/outputs

Adding Modules
--------------

To create new modules with new functionalities, one can subclass any of the
following base classes:

    * BaseModule: Works for any new module.
    * FileImporter: For extractor modules with files as input.
    * UnaryOperation: For modules that do work on one input data flow.
    * BinaryOperation: For modules that implement an operation on two separate
      inputs.
    * FileOutput: For output modules with files as output. 

When implementing a new module, one should use the following template:

.. code-block:: python

    class MyModule(BaseModule): # Any of the base classes
        """ Documentation of the module

        Args:
            module (dict): Description of the module dict to 
                be passed as argument.
        """
        def __init__(self, module, env: Environment, named_modules):
            super().__init__(module, env, named_modules)

            self.template_path = # Path to template
            self.template = self.env.get_template(self.template_path)

        def rendered_result(self) -> (str, str):
            return self.template.render(
                name=self.name,
                # Other arguments
            ), '' # or ext template if applicable

        def get_out_type(self):
            # This function should return the output type of the module
            # as a list of strings.

        def check_integrity(self):
            # This function performs integrity checks if applicable.


The module should have a scala template associated with it for generating the
corresponding code. 

.. code-block:: scala

    // ===== My module {{name}} =====

    // Insert code here
    val {{name}} = // The Flink Dataset

Once the module is defined, it can be added to the rendering engine by adding
it to the ModuleMap class directly for example. 