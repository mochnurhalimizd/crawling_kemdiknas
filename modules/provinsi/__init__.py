import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.request.lib import RequestLib
from library.log.lib import LoggerLib
from library.config.lib import get_config


class ProvinsiModules:
    def __init__(self):
        self.logger = LoggerLib('provinsi_modules')
        self.request = RequestLib(self.logger)
        self.config = get_config('config.conf')
        self.data = self.get_parameter(self.config)

    def run(self):
        response = self.request.get_method(url=self.data.get('url'), parameter=self.data.get('parameter'))
        if response.get('status') == 200:
            data = response.get('data')
            data = list(map(lambda key: {k: v.strip() if isinstance(v, str) else v for k, v in key.items()}, data))
            return self.reprocess(data)

    def reprocess(self, data):
        print(data)

    @staticmethod
    def get_parameter(config):
        return {
            'url': config.get('url', 'get_location'),
            'parameter': {
                'id_level_wilayah': config.get('level', 'provinsi'),
                'semester_id': 20171
            }
        }

if __name__ == '__main__':
    a = ProvinsiModules()
    a.run()
