from orator import DatabaseManager

# ----- Skripsi Database
# config = {
#     'mysql': {
#         'driver'    : 'mysql',
#         'host'      : 'newdemo.aplikasiskripsi.com',
#         'database'  : '',
#         'user'      : '',
#         'password'  : '',
#         'prefix'    : ''
#     }
# }

# ----- Local Database
config = {
    'mysql': {
        'driver'    : 'mysql',
        'host'      : 'localhost',
        'database'  : 'aplikasi_muhamad_nahrowi',
        'user'      : 'root',
        'password'  : '',
        'prefix'    : '',
        "charset": "utf8mb4"  # <-- here
    }

}

db = DatabaseManager(config)