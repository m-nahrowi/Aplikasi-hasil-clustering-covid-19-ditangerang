from orator import DatabaseManager

# ----- Skripsi Database
# config = {
#     'mysql': {
#         'driver'    : 'mysql',
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
        'host'      : '165.22.51.224',
        'database'  : 'nahrowi',
        'user'      : 'nahrowi',
        'password'  : 'cA6NRGGTmNRe3d7h',
        'prefix'    : '',
        "charset": "utf8mb4"  # <-- here
    }

}

db = DatabaseManager(config)