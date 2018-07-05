import json
import sys
from graphviz import Digraph

def get_color(word):
    if 'importer' in word.lower():
        return 'green'
    elif 'output' in word.lower():
        return 'orange'
    elif 'extracteur' in word.lower():
        return 'lightblue'
    else:
        return None


def get_shape(word):
    if 'importer' in word.lower():
        return 'cds'
    elif 'output' in word.lower():
        return 'ellipse'
    else:
        return 'ellipse'

def get_margin(word):
    if 'importer' in word.lower():
        return '0.3'
    elif 'output' in word.lower():
        return '0.1'
    else:
        return '0.1'

if __name__  == '__main__':
    if len(sys.argv[1]) > 0:
        arg_fname = sys.argv[1]
    else:
        arg_fname = 'spec.json'

    json_obj = json.load(open(arg_fname))
    g = Digraph('compiled', graph_attr={'rankdir': 'LR'})

    for mod in json_obj.get('modules'):
        g.node(mod.get('name'), 
               mod.get('name') + '\n type: ' + mod.get('type'), 
               style='filled', 
               color=get_color(mod.get('type', '')),
               shape=get_shape(mod.get('type', '')),
               margin=get_margin(mod.get('type', '')))

        if mod.get('source1') is not None:
            g.edge(mod.get('source1'), mod.get('name'))

        if mod.get('source2') is not None:
            g.edge(mod.get('source2'), mod.get('name'))

    g.view()

