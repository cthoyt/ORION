import os
import argparse
import gzip
import enum

from Common.node_types import PUBLICATIONS
from io import TextIOWrapper
from Common.extractor import Extractor
from Common.utils import GetData
from Common.loader_interface import SourceDataLoader


class NODEFILECOLS(enum.IntEnum):
    ID = 0
    NAME = 1
    NODE_TYPE = 2


class EDGEFILECOLS(enum.IntEnum):
    SUBJECT_ID = 0
    PREDICATE = 1
    OBJECT_ID = 2
    TMKP_ID = 3
    ASSOCIATION_TYPE = 4
    CONFIDENCE_SCORE = 5
    SUPPORTING_STUDIES_TMKP_IDS = 6  # pipe | is used as delimiter
    PUBLICATIONS = 7  # pipe | is used as delimiter
    JSON_ATTRIBUTES = 8


class TMKPLoader(SourceDataLoader):

    source_id: str = 'TextMiningKP'
    provenance_id: str = 'infores:textminingkp'

    # this is not the right way to do this, ideally their predicates would be normalized later in the pipeline,
    # but this handles some complications with certain biolink 2 predicates (failing to) normalizing to biolink 3
    tmkp_predicate_map = {
        "biolink:contributes_to": 'RO:0002326',
        "biolink:entity_negatively_regulates_entity": 'RO:0002449',
        "biolink:entity_positively_regulates_entity": 'RO:0002450',
        "biolink:gain_of_function_contributes_to": 'biolink:contributes_to',  # could not find a better predicate
        "biolink:loss_of_function_contributes_to": 'biolink:contributes_to'  # could not find a better predicate
    }

    def __init__(self, test_mode: bool = False, source_data_dir: str = None):
        """
        :param test_mode - sets the run into test mode
        :param source_data_dir - the specific storage directory to save files in
        """
        super().__init__(test_mode=test_mode, source_data_dir=source_data_dir)

        self.tmkp_nodes_file = 'nodes.tsv.gz'
        self.tmkp_edges_file = 'edges.tsv.gz'
        self.data_files = [self.tmkp_nodes_file,
                           self.tmkp_edges_file]
        self.data_url = 'https://storage.googleapis.com/translator-text-workflow-dev-public/kgx/UniProt/'
        self.source_db: str = 'Text Mining KP'

    def get_latest_source_version(self) -> str:
        # TODO retrieve the actual version
        return "1.0"

    def get_data(self) -> int:
        gd: GetData = GetData(self.logger.level)
        for data_file in self.data_files:
            gd.pull_via_http(f'{self.data_url}{data_file}', data_dir=self.data_path)

    def parse_data(self) -> dict:

        extractor = Extractor(file_writer=self.output_file_writer)

        tmkp_nodes_path: str = os.path.join(self.data_path, self.tmkp_nodes_file)
        with gzip.open(tmkp_nodes_path) as zf:
            extractor.csv_extract(TextIOWrapper(zf, "utf-8"),
                                  lambda line: line[NODEFILECOLS.ID.value],  # extract subject id,
                                  lambda line: None,  # extract object id
                                  lambda line: None,  # predicate extractor
                                  lambda line: {'name': line[NODEFILECOLS.NAME.value],
                                                'categories': [line[NODEFILECOLS.NODE_TYPE.value]]},  # subject props
                                  lambda line: {},  # object props
                                  lambda line: None,  # edge props
                                  delim='\t')

        tmkp_edges_path: str = os.path.join(self.data_path, self.tmkp_edges_file)
        with gzip.open(tmkp_edges_path) as zf:
            extractor.csv_extract(TextIOWrapper(zf, "utf-8"),
                                  lambda line: line[EDGEFILECOLS.SUBJECT_ID.value],  # extract subject id,
                                  lambda line: line[EDGEFILECOLS.OBJECT_ID.value],  # extract object id
                                  lambda line: self.convert_tmkp_predicate(line[EDGEFILECOLS.PREDICATE.value]),  # predicate extractor
                                  lambda line: {},  # subject props
                                  lambda line: {},  # object props
                                  lambda line: {PUBLICATIONS: line[EDGEFILECOLS.PUBLICATIONS.value].split('|')},  # edge props
                                  delim='\t')

        # return to the caller
        return extractor.load_metadata

    def convert_tmkp_predicate(self, predicate: str):
        if predicate in self.tmkp_predicate_map:
            return self.tmkp_predicate_map[predicate]
        else:
            return predicate
