import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.log.lib import LoggerLib
from library.config.lib import get_config
from library.request.lib import RequestLib
from library.thread.lib import ThreadLib
from library.general.lib import merge_two_dict, tic, toc

from model.kabupaten import KabupatenModel


class KabupatenModules:
    def __init__(self):
        self.logger = LoggerLib('kabupaten_modules')
        self.request = RequestLib(self.logger)
        self.config = get_config('config.conf')
        self.model = KabupatenModel(self.get_parameter(self.config).get('database'), self.logger)
        self.data = self.get_parameter(self.config)

    def run(self):
        kabupaten = self.model.get_data().get('data')
        data = [merge_two_dict(self.get_request_parameter(), {'kode_wilayah': x.get('kode_wilayah')}) for x in kabupaten]

        for parameter in data:
            thread = ThreadLib(1, 'hello', callback=self.request_api, param=parameter)
            thread.start()

    def request_api(self, parameter):
        tic(tag='fetch url')
        response = self.request.get_method(url=self.data.get('url'), parameter=parameter)
        if response.get('status') == 200:
            data = response.get('data')
            data = list(map(lambda key: {k: v.strip() if isinstance(v, str) else v for k, v in key.items()}, data))
            return self.reprocess(data)
        toc(tag='fetch url')

    def reprocess(self, data):
        for item in data:
            self.model.search_data(item.get('kode_wilayah'), item)

    @staticmethod
    def get_parameter(config):
        return {
            'url': config.get('url', 'get_location'),
            'parameter': {
                'id_level_wilayah': config.get('level', 'kabupaten'),
                'semester_id': 20171
            },
            'database': {
                'db': config.get('mongo', 'mongo_database_config'),
                'host': config.get('mongo', 'mongo_url'),
                'port': config.get('mongo', 'mongo_port')
            } 
        }

    def get_request_parameter(self):
        param = self.data.get('parameter')
        return param

if __name__ == '__main__':
    a = KabupatenModules()
    a.run()
