ENV = "development"
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0

#vider le cache
SECRET_KEY="maCleSuperSecurisee"

#Configuration du serveur web
WEB_SERVER = {
    "host": "localhost",
    "port":8080,
    }

#Configuration du serveur de BDD
DB_SERVER = {
    "user": "admin",
    "password": "password",
    "host": "localhost",
    "port": 3306, #8889 si MAC
    "database": "beweb", #nom de la BDD
    "raise_on_warnings": True
    }

URL_PATHS = {
    "starlink" : ("https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle", "App/static/tle_starlink.txt"),
    "gnss" : ("https://celestrak.com/NORAD/elements/gp.php?GROUP=gnss&FORMAT=tle", "App/static/tle_gnss.txt" ), 
    "meteosat" : ("https://celestrak.com/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle", "App/static/tle_meteosat.txt")
}