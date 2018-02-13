import argparse
from modules.kecamatan import KecamatanModules
from modules.kabupaten import KabupatenModules
from modules.provinsi import ProvinsiModules
from modules.sekolah import SekolahModules
from modules.sekolah.reprocess import ReprocessModules

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main file for kemdiknas crawler")
    parser.add_argument('-m',
                        dest='mode',
                        help='mode application (kecamatan, kabupaten, provinsi, sekolah & reprocess)')
    parser.add_argument('-c',
                        dest='city',
                        help='reprocess city code (default: 3310 (Klaten))',
                        type=int,
                        default=3310)

    args = parser.parse_args()

    if args.mode == "kecamatan":
        app = KecamatanModules()
        app.run()
    elif args.mode == "kabupaten":
        app = KabupatenModules()
        app.run()
    elif args.mode == "provinsi":
        app = ProvinsiModules()
        app.run()
    elif args.mode == "sekolah":
        app = SekolahModules()
        app.run()
    elif args.mode == "reprocess":
        app = ReprocessModules(database=args.city)
        app.run()
    else:
        parser.print_help()
