#! /Users/hugo/anaconda3/bin/python
""" Main compilation module
"""
import os
import json
import argparse

from jinja2 import Environment, FileSystemLoader
from renderer import Renderer

BASE_DIR = 'scala/src/main/scala/core/'
TEMPLATE_NAME = 'MainTemplate.scala.template'

def run(spec, template_dir, output_path):
    """ Main function to compile `spec` with the templates
    located in `template_dir`.
    """
    input_file = json.load(open(spec))
    module_list = input_file.get('modules', [])
    render = Renderer(module_list, template_dir)
    render.check_integrity()

    for mod in render.named_modules:
        print(mod, render.named_modules[mod].get_out_type())

    modules, ext_modules = render.get_rendered()

    final_env = Environment(loader=FileSystemLoader(BASE_DIR))
    final = final_env.get_template(TEMPLATE_NAME)

    with open(output_path, 'w') as outfile:
        outfile.write(final.render(modules=modules, ext_modules=ext_modules))


def main():
    """ Main entrypoint to the compiler.
    """
    parser = argparse.ArgumentParser(description="""Command line interface for
        compiling JSON spec file in Scala code.""")
    parser.add_argument('-s', '--spec',
                        metavar='filename',
                        type=str,
                        help='spec filename',
                        default='spec.json')
    parser.add_argument('-t', '--template-dir',
                        metavar='dirname',
                        type=str,
                        help='template directory',
                        default='templates')
    parser.add_argument('-o', '--output',
                        metavar='output',
                        type=str,
                        help='output filename',
                        default=os.path.join(BASE_DIR, 'ScalaTempTest.scala'))

    args = parser.parse_args()
    run(args.spec, args.template_dir, args.output)

if __name__ == "__main__":
    main()
