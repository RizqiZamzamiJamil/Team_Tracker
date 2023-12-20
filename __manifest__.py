{
    "name"          : "Team Tracker",
    "version"       : "1.0",
    "author"        : "Rizqi Zamzami Jamil",
    "website"       : "https://github.com/RizqiZamzamiJamil",
    "category"      : "Tracker",
    "summary"       : "Ini adalah custom module untuk pembentukan tim mahasiswa",
    "description"   : """
        Membuat custom module untuk pembentukan tim mahasiswa
    """,
    "depends"       : [
        "base", "board", "sale", "web"
    ],
    "data"          : [
            'security/ir.model.access.csv',
            'views/menu.xml',
            'views/mahasiswa.xml',
            # 'views/mahasiswa_chart.xml'     gk jadi,
            'views/team.xml',
            'views/spk.xml',
            'views/minat_data.xml',
            'views/event.xml',
            'views/minat.xml',
            'views/team_tracker_board.xml',
    ],
    "test"          : [],
    "image"         : [],
    "qweb"          : [],
    "css"           : [],
    "application"   : True,
    "installable"   : True,
    "auto_install"  : False,
    'assets': {
        'web.assets_backend': [
            'owl/static/src/components/**/*.js',
            'owl/static/src/components/**/*.xml',
            'owl/static/src/components/**/*.scss',
        ],
    },
}
