### Description

This is a crawler to crawl kemdiknas page and save it into mongoDB.
Required library are written below:

    - requests
    - pymongo
    - bs4
    - etc


### Usage

this application has 4 modes, that is **kecamatan**, **kabupaten**, **provinsi**, **sekolah** and **reprocess**.

```shell
$ python3 main.py -m [Mode] -c [City]
```

Mode:

    - kecamatan
    - kabupaten
    - provinsi
    - sekolah
    - reprocess

City:

    - city code based on in workspace
