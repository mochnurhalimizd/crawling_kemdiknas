class CityModel:
    def __init__(self, database, logger):
        self.mongo = database
        self.logger = logger
        self.collection = 'diknas'
        self.seq_collection = 'sequence'

    def search_data(self, pk, item):
        find = self.mongo.get(self.collection, where={'nama': pk, 'source_type': 'external'})
        if find.get('count') > 0:
            self.update_data(item, {'nama': pk, 'source_type': 'external'})
        else:
            self.insert_data(item, pk)

    def insert_data(self, item, pk):
        seq = self.mongo.get(self.seq_collection, where={'_id': 'diknas'})
        seq['data'] = [x for x in seq.get('data')]
        if len(seq.get('data')) > 0:
            seq = int([x.get('seq') for x in seq.get('data')][0])
            self.update_sequence({'_id': 'diknas'}, {'seq': seq + 1})

            item.update({'_id': seq})
            query = self.mongo.insert_one(self.collection, item)
            if query.get('code') == 200:
                self.logger.write_log(self.get_message('success', 'insert', pk), method='INFO')
            else:
                self.insert_data(item)
        else:
            self.insert_sequence({'_id': 'diknas', 'seq': 1})
            self.insert_data(item, pk)

    def update_data(self, item, key):
        query = self.mongo.update(self.collection, item, key)
        if query.get('code') == 200:
            self.logger.write_log(self.get_message('success', 'update', key.get('nama')), method='INFO')
        else:
            self.update_data(item, key)

    def update_sequence(self, where, value):
        query = self.mongo.update(self.seq_collection, value, where)
        if query.get('code') != 200:
            self.update_data(where, value)

    def insert_sequence(self, value):
        query = self.mongo.insert_one(self.seq_collection, value)
        if query.get('code') != 200:
            self.insert_sequence(value)

    @staticmethod
    def get_message(mode, method, pk):
        result = {
            'error': lambda x: 'Error {} data : {}'.format(x.get('method'), x.get('pk')),
            'success': lambda x: 'Success {} data : {}'.format(x.get('method'), x.get('pk'))
        }

        return result.get(mode, lambda x: str('Oops key is not found'))({'method': method, 'pk': pk})


