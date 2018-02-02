from pymongo.mongo_client import MongoClient
from pymongo import errors
from itertools import chain
import traceback


class MongoLib:

    def __init__(self, host, port, db):
        """Pemanggilan fungsi MongoClient dan membuat cursor koneksi pada database

        :param host : (String) host database
        :param port : (Integer) port database
        :param db : (String) name database
        """
        try:
            self.connection = MongoClient('mongodb://{}:{}'.format(host, port))
        except errors.PyMongoError:
            traceback.print_exc()

        self.db = self.connection[db]

    @staticmethod
    def get_database(database, mode, address):
        city_temp = database.get('workspace', None, {})

        temp = list(map(
            lambda data: {
                int(data.get('city_id')): MongoLib(address, 27017, 'smartcity_{}'.format(data.get('city_id')))
            }, city_temp.get('data')
        ))


        db_list = dict(chain(*map(dict.items, temp)))

        try:
            if mode not in db_list and mode is not "temporary":
                raise ValueError('Database is not found {} in main server'.format(mode))
            else:
                return db_list if mode == "temporary" else db_list[mode]
        except errors.PyMongoError as e:
            raise ValueError(e)
        except Exception as arg:
            raise ValueError('Error : {}'.format(arg))

    @staticmethod
    def get_workspace_code(database):
        city_temp = database.get('topic', None, {})

        return list(map(lambda data: int(data.get('t_kode_kota')), city_temp.get('data')))

    def get(self, table, field=None, where=None, limit=None):
        """Mengambil semua data dengan kriteria tertentu sesuai parameter

        Usage

        self.get('product', {Object}, {Object}, 5)

        :param table : (String) nama tabel
        :param field : (Dictionary) field yang akan ditampilkan
        :param where : (Dictionary) criteria yang akan dipakai untuk mengambil data
        :param limit : (Integer) port database
        :return data : (Dictionary) berisi dari data hasil pencarian dan jumlah data yang ditemukan
        """

        where = {} if where is None else dict(where)
        field = None if field is None else dict(field)

        if limit is None:
            query = self.db[table].find(where, field)
            return {'data': query, 'count': query.count()}
        else:
            query = self.db[table].find(where, field).limit(limit)
            return {'data': query, 'count': query.count()}

    def get_one(self, table, field=None, where=None):
        """Mengambil satu data dengan kriteria tertentu sesuai parameter

        Usage

        self.getOne('product', {Object}, {Object})

        :param table : (String) nama tabel
        :param field : (Dictionary) field yang akan ditampilkan
        :param where : (Dictionary) criteria yang akan dipakai untuk mengambil data
        :return data : (Dictionary) berisi dari data hasil pencarian
        """

        try:
            where = {} if where is None else dict(where)
            field = None if field is None else dict(field)

            query = self.db[table].find_one(where, field)
            return {'data': query}
        except errors as e:
            traceback.print_exc()
            return {'data': [], 'message': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'data': [], 'message': str(e)}

    def update(self, table, data, key):
        """Mengubah satu data sesuai dengan parameter

        Usage

        self.updateOne('product', {Object}, {'id': ''})

        :param table : (String) nama tabel
        :param data : (Dictionary) data yang akan diubah
        :param key : (Dictionary) criteria yang akan dipakai untuk mengubah data
        :return data : (Dictionary) berisi dari data code dan pesan proses update data
        """
        try:
            if data is not None:
                try:
                    self.db[table].update_one(key, {"$set": dict(data)})
                    return {'code': 200, 'message': 'Update Success'}
                except Exception as e:
                    return {'code': 500, 'message': 'Update Error {}'.format(e)}
            else:
                return {'code': 500, 'message': 'Attribut data is not found'}
        except errors as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}

    def update_one(self, table, data, index):
        """Mengubah satu data sesuai dengan parameter

        Usage

        self.updateOne('product', {Object}, {Object})

        :param table : (String) nama tabel
        :param data : (Dictionary) data yang akan diubah
        :param index : (Dictionary) criteria yang akan dipakai untuk mengubah data
        :return data : (Dictionary) berisi dari data code dan pesan proses update data
        """
        try:
            if data is not None:
                try:
                    self.db[table].update_one({index['key']: index['value']}, {"$set": dict(data)})
                    return {'code': 200, 'message': 'Update Success'}
                except Exception as e:
                    return {'code': 500, 'message': 'Update Error {}'.format(e)}
            else:
                return {'code': 500, 'message': 'Attribut data is not found'}
        except errors as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}

    def update_all(self, table, data, index):
        """Mengubah semua data sesuai dengan parameter

        Usage

        self.updateOne('product', {Object}, {Object})

        :param table : (String) nama tabel
        :param data : (Dictionary) data yang akan diubah
        :param index : (Dictionary) criteria yang akan dipakai untuk mengubah data
        :return data : (Dictionary) berisi dari data code dan pesan proses update data
        """
        try:
            if data is not None:
                try:
                    self.db[table].update_one({index['key']: index['value']}, data)
                    return {'code': 200, 'message': 'Update Success'}
                except Exception as e:
                    return {'code': 500, 'message': 'Update Error {}'.format(e)}
            else:
                return {'code': 500, 'message': 'Attribut data is not found'}
        except errors as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}
        except Exception as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}

    def insert_one(self, table, data):
        """Menambahkan semua data sesuai dengan parameter

        Usage

        self.insertOne('product', {Object})

        :param table : (String) nama tabel
        :param data : (Dictionary) data yang akan diubah
        :return data : (Dictionary) berisi dari data code dan pesan proses insert data
        """

        try:
            self.db[table].insert_one(dict(data))
            return {'code': 200, 'message': 'Insert Success'}
        except errors as e:
            traceback.print_exc()
            return {'code': 500, 'message': str(e)}
        except Exception as e:
            return {'code': 500, 'message': 'Insert Error {}'.format(e)}
