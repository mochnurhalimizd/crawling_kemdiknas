import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.mongo.lib import MongoLib


class LocationModel:
    collection = 'smartcity_temp_location'

    def __init__(self, database, logger):
        self.mongo = MongoLib(
            db=database.get('db'),
            host=database.get('host'),
            port=database.get('port')
        )
        self.logger = logger

    def get_data(self):
        return self.mongo.get(self.collection, field={'nama': 1, 'kode_wilayah': 1, '_id': 0}, where={'id_level_wilayah': {'$gt': 1}})

