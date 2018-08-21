""" Package grouping all operation modules that perform operations
on dataflows.
"""
from modules.base_module import BaseModule

from modules.operations.join import Join
from modules.operations.extractor_link import ExtractorLink
from modules.operations.projection import Projection
from modules.operations.union import Union
from modules.operations.split import Split
from modules.operations.extractor_word_similarity import\
    ExtractorWordSimilarity
from modules.operations.map import Map
from modules.operations.count_distinct import CountDistinct
from modules.operations.string_similarity import StringSimilarity
