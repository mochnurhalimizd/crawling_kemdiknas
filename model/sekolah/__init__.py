import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.mongo.lib import MongoLib


class SekolahModel:
    collection = 'smartcity_temp_school'

    def __init__(self, database, logger):
        self.mongo = MongoLib(
            db=database.get('db'),
            host=database.get('host'),
            port=database.get('port')
        )
        self.logger = logger

    def get_data(self):
        return self.mongo.get('smartcity_temp_location', where={'id_level_wilayah': 3})

    def search_data(self, pk, item):
        find = self.mongo.get(self.collection, where={'sekolah_id_enkrip': pk})
        if find.get('count') > 0:
            self.update_data(item, {'sekolah_id_enkrip': pk})
        else:
            self.insert_data(item, pk)

    def insert_data(self, item, pk):
        query = self.mongo.insert_one(self.collection, item)
        if query.get('code') == 200:
            self.logger.write_log(self.get_message('success', 'insert', pk), method='INFO')
        else:
            self.insert_data(item)

    def update_data(self, item, key):
        query = self.mongo.update(self.collection, item, key)
        if query.get('code') == 200:
            self.logger.write_log(self.get_message('success', 'update', key.get('sekolah_id_enkrip')), method='INFO')
        else:
            self.update_data(item, key)

    @staticmethod
    def get_message(mode, method, pk):
        result = {
            'error': lambda x: 'Error {} data : {}'.format(x.get('method'), x.get('pk')),
            'success': lambda x: 'Success {} data : {}'.format(x.get('method'), x.get('pk'))
        }

        return result.get(mode, lambda x: str('Oops key is not found'))({'method': method, 'pk': pk})
