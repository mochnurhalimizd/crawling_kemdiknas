from datetime import datetime

CONST = {
    'latlng': [float(0.0), float(0.0)],
    'location': {
        'type': 'point',
        'coordinates': [float(0.0), float(0.0)]
    }
}

class InfomasiModel:
    kepsek = None
    akreditasi = None
    kurikulum = None
    waktu = None

    def __init__(self, data={}):
        if data:
            self.set_dict(data)
        else:
            self.reset()

    def get_dict(self, prefix=''):
        data = dict()
        data['{}kepsek'.format(prefix)] = self.kepsek
        data['{}akreditasi'.format(prefix)] = self.akreditasi
        data['{}kurikulum'.format(prefix)] = self.kurikulum
        data['{}waktu'.format(prefix)] = self.waktu
        return data

    def set_dict(self, data):
        self.kepsek = data.get('kepsek') if data.get('kepsek') != None else None
        self.akreditasi = data.get('akreditasi') if data.get('akreditasi') != None else None
        self.kurikulum = data.get('kurikulum') if data.get('kurikulum') != None else None
        self.waktu = data.get('waktu') if data.get('waktu') != None else None

    def reset(self):
        self.kepsek = None
        self.akreditasi = None
        self.kurikulum = None
        self.waktu = None


class FasilitasModel:
    ruang_kelas = 0
    ruang_lab = 0
    perpustakaan = 0
    akses_internet = None
    BOS = None

    def __init__(self, data={}):
        if data:
            self.set_dict(data)
        else:
            self.reset()

    def get_dict(self, prefix=''):
        data = dict()
        data['{}ruang_kelas'.format(prefix)] = self.ruang_kelas
        data['{}ruang_lab'.format(prefix)] = self.ruang_lab
        data['{}perpustakaan'.format(prefix)] = self.perpustakaan
        data['{}akses_internet'.format(prefix)] = self.akses_internet
        data['{}BOS'.format(prefix)] = self.BOS
        return data

    def set_dict(self, data):
        self.ruang_kelas = data.get('ruang_kelas')if data.get('ruang_kelas') != None else 0
        self.ruang_lab = data.get('ruang_lab')if data.get('ruang_lab') != None else 0
        self.perpustakaan = data.get('perpustakaan')if data.get('perpustakaan') != None else 0
        self.akses_internet = data.get('akses_internet') if data.get('akses_internet') != None else None
        self.BOS = data.get('BOS') if data.get('BOS') != None else None

    def reset(self):
        self.ruang_kelas = 0
        self.ruang_lab = 0
        self.perpustakaan = 0
        self.akses_internet = None
        self.BOS = None


class KontakModel:
    telepon = None
    email = None
    web = None

    def __init__(self, data={}):
        if data:
            self.set_dict(data)
        else:
            self.reset()

    def get_dict(self, prefix=''):
        data = dict()
        data['{}telepon'.format(prefix)] = self.telepon
        data['{}email'.format(prefix)] = self.email
        data['{}web'.format(prefix)] = self.web
        return data

    def set_dict(self, data):
        self.telepon = data.get('telepon') if data.get('telepon') != None else None
        self.email = data.get('email') if data.get('email') != None else None
        self.web = data.get('web') if data.get('web') != None else None

    def reset(self):
        self.telepon = None
        self.email = None
        self.web = None


class SekolahModel:
    nama = None
    alamat = None
    informasi = InfomasiModel()
    fasilitas = FasilitasModel()
    kontak = KontakModel()
    location = CONST.get('location')
    latlng = CONST.get('latlng')
    created_by = 1
    created_from = 'user_cms'
    created_time = datetime.now()
    updated_by = 1
    updated_from = 'user_cms'
    updated_time = datetime.now()
    banned = False
    banned_by = 1
    banned_from = 'user_cms'
    banned_time = datetime.now()
    source_type = 'external'

    def __init__(self, data={}):
        if data:
            self.set_dict(data)
        else:
            self.reset()

    def get_dict(self, prefix=''):
        data = dict()
        data['{}nama'.format(prefix)] = self.nama
        data['{}alamat'.format(prefix)] = self.alamat
        data['{}informasi'.format(prefix)] = self.informasi.get_dict()
        data['{}fasilitas'.format(prefix)] = self.fasilitas.get_dict()
        data['{}kontak'.format(prefix)] = self.kontak.get_dict()
        data['{}location'.format(prefix)] = self.location
        data['{}latlng'.format(prefix)] = self.latlng
        data['{}created_by'.format(prefix)] = self.created_by
        data['{}created_from'.format(prefix)] = self.created_from
        data['{}created_time'.format(prefix)] = self.created_time
        data['{}updated_by'.format(prefix)] = self.updated_by
        data['{}updated_from'.format(prefix)] = self.updated_from
        data['{}updated_time'.format(prefix)] = self.updated_time
        data['{}banned'.format(prefix)] = self.banned
        data['{}banned_by'.format(prefix)] = self.banned_by
        data['{}banned_from'.format(prefix)] = self.banned_from
        data['{}banned_time'.format(prefix)] = self.banned_time
        data['{}source_type'.format(prefix)] = self.source_type
        return data

    def set_dict(self, data):
        self.nama = data.get('nama') if data.get('nama') != None else None
        self.alamat = data.get('alamat')if data.get('alamat') != None else None
        self.informasi = InfomasiModel(data.get('informasi'))
        self.fasilitas = FasilitasModel(data.get('fasilitas'))
        self.kontak = KontakModel(data.get('kontak'))
        self.location = data.get('location') if data.get('location') is not None else CONST.get('location')
        self.latlng = data.get('latlng') if data.get('latlng') is not None else CONST.get('latlng')

    def reset(self):
        self.nama = None
        self.alamat = None
        self.informasi = InfomasiModel()
        self.fasilitas = FasilitasModel()
        self.kontak = KontakModel()
        self.location = CONST.get('location')
        self.latlng = CONST.get('latlng')
        self.created_by = 1
        self.created_from = 'user_cms'
        self.created_time = datetime.now()
        self.updated_by = 1
        self.updated_from = 'user_cms'
        self.updated_time = datetime.now()
        self.banned = False
        self.banned_by = 1
        self.banned_from = 'user_cms'
        self.banned_time = datetime.now()
        self.source_type = 'external'


if __name__ == '__main__':
    a = SekolahModel()
