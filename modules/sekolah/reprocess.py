import os
import sys
from copy import deepcopy

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from library.log.lib import LoggerLib
from library.config.lib import get_config
from model.workspace import WorkspaceModel
from model.sekolah import SekolahModel
from model.sekolah.model import SekolahModel as Model
from model.city import CityModel


class ReprocessModules:
    def __init__(self, database=None):
        self.logger = LoggerLib('sekolah_modules')
        self.config = get_config('config.conf')
        self.model = WorkspaceModel(self.get_parameter(self.config).get('database'), self.logger)
        self.model_school = SekolahModel(self.get_parameter(self.config).get('database'), self.logger)
        self.object = Model()
        self.data = self.get_parameter(self.config)
        self.db = self.model.mongo.get_database(
            self.model.mongo,
            'temporary',
            self.config.get('mongo', 'mongo_url')
        )

        self.db = {k: v for k, v in self.db.items() if k == database} if database is not None else self.db

    def run(self):
        for x in self.db:
            temp = [x.get('id') for x in self.model.get_data('mapping', where={'city_code': x, 'type': 'kemdiknas'}).get('data')]

            if len(temp) > 0:
                where = {
                    '$or': [{'kode_wilayah_induk_kabupaten': temp[0]}, {'kode_wilayah_induk_kecamatan': temp[0]}]
                }

                for item in self.model_school.get_school(where=where).get('data'):
                    temp = dict()
                    informasi = {}
                    fasilitas = {}
                    kontak = {}

                    temp.update({'nama': item.get('nama')})
                    temp.update({'alamat': item.get('')})

                    if 'kontak' in item.get('info_sekolah'):
                        kontak = list(filter(
                            lambda y: y.get('key') == 'kontak utama', item.get('info_sekolah').get('kontak')
                        ))[0]

                        location = self.get_latitude(deepcopy(kontak))
                        alamat = self.get_alamat(deepcopy(kontak))
                        temp.update({'alamat': alamat})
                        temp.update({'location': {'type': 'Point', 'coordinates': location}})
                        temp.update({'latlng': location})

                    if 'info' in item.get('info_sekolah'):
                        informasi = item.get('info_sekolah').get('info')

                    fasilitas = self.get_fasilitas(item)
                    kontak = self.get_kontak(item)

                    temp.update({'informasi': informasi})
                    temp.update({'fasilitas': fasilitas})
                    temp.update({'kontak': kontak})

                    item = Model(data=temp)
                    model = CityModel(database=self.db[x], logger=self.logger)
                    model.search_data(item.get_dict().get('nama'), item.get_dict())

    @staticmethod
    def get_alamat(data):
        alamat = data.get('value')
        alamat.pop("lintang")
        alamat.pop("bujur")
        alamat.pop("dusun")
        return ', '.join(['{} {}'.format(k, v) for k, v in alamat.items()]).replace('alamat ', '')

    @staticmethod
    def get_latitude(data):
        location = {'{}'.format('lat' if k == 'lintang' else 'lng'): v for k, v in data.get('value').items() if k == 'lintang' or k == 'bujur'}
        location['lng'] = '0' if location.get('lng') == '' else location.get('lng')
        location['lat'] = '0' if location.get('lat') == '' else location.get('lat')
        return [float(location.get('lng')), float(location.get('lat'))]

    @staticmethod
    def get_fasilitas(item):
        fasilitas = dict()
        fasilitas.update({'ruang_kelas': item.get('jml_rk')})
        fasilitas.update({'ruang_lab': item.get('jml_lab')})
        fasilitas.update({'perpustakaan': item.get('jml_perpus')})

        if 'profil' in item.get('info_sekolah'):
            temp = list(filter(
                lambda y: y.get('key') == 'data pelengkap', item.get('info_sekolah').get('profil')
            ))[0]

            fasilitas.update({'BOS': temp.get('value').get('status bos')})
            fasilitas.update({'akses_internet': temp.get('value').get('akses internet')})

        return fasilitas

    @staticmethod
    def get_kontak(item):
        if 'kontak' in item.get('info_sekolah'):
            kontak = list(filter(
                lambda y: y.get('key') == 'kontak yang bisa dihubungi', item.get('info_sekolah').get('kontak')
            ))[0]

            return kontak.get('value')
        else:
            return {}

    @staticmethod
    def get_parameter(config):
        return {
            'database': {
                'db': config.get('mongo', 'mongo_database_config'),
                'host': config.get('mongo', 'mongo_url'),
                'port': config.get('mongo', 'mongo_port'),
                'workspace': config.get('mongo', 'mongo_database_workspace'),
            }
        }

if __name__ == '__main__':
    a = ReprocessModules()
    a.run()
