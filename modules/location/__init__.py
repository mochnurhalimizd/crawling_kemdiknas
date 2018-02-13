import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.log.lib import LoggerLib
from library.config.lib import get_config
from library.request.lib import RequestLib
from library.thread.lib import ThreadLib
from library.general.lib import merge_two_dict, tic, toc

from model.location import LocationModel
from model.workspace import WorkspaceModel


class LocationModules:
    def __init__(self):
        self.logger = LoggerLib('location_modules')
        self.request = RequestLib(self.logger)
        self.config = get_config('config.conf')
        self.model = LocationModel(self.get_parameter(self.config).get('database'), self.logger)
        self.workspace_model = WorkspaceModel(self.get_parameter(self.config).get('database'), self.logger)
        self.data = self.get_parameter(self.config)

    def run(self):
        workspace = [self.reformat(item, 'city') for item in self.workspace_model.get_data('master').get('data')]
        kecamatan = [self.reformat(item, 'location') for item in self.model.get_data().get('data')]

        result = self.merge_lists(kecamatan, workspace, 'name')
        result = list(filter(lambda x: 'city_code' in x, result))
        result = list(map(lambda x: self.default(x) if 'id' not in x else x, result))

        for item in result:
            self.workspace_model.search_data(item.get('city_code'), item)

    @staticmethod
    def reformat(x, mode):
        temp = dict()
        if mode == 'location':
            temp.update({'name': x.get('nama').replace('Kec.', 'KECAMATAN').replace('Kab.', 'KABUPATEN').upper()})
            temp.update({'type': 'kemdiknas'})
            temp.update({'id': x.get('kode_wilayah')})
        elif mode == 'city':
            temp = {'city_code': x.get('id'), 'name': x.get('name')}
        return temp

    @staticmethod
    def default(value):
        value.update({'id': None})
        return value

    @staticmethod
    def merge_lists(l1, l2, key):
        merged = {}
        for item in l1 + l2:
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item
        return [val for (_, val) in merged.items()]

    @staticmethod
    def get_parameter(config):
        return {
            'url': config.get('url', 'get_location'),
            'parameter': {
                'id_level_wilayah': config.get('level', 'kecamatan'),
                'semester_id': 20171
            },
            'database': {
                'db': config.get('mongo', 'mongo_database_config'),
                'host': config.get('mongo', 'mongo_url'),
                'port': config.get('mongo', 'mongo_port'),
                'workspace': config.get('mongo', 'mongo_database_workspace'),
            }
        }

if __name__ == '__main__':
    a = LocationModules()
    a.run()
