from time import time
from tracemalloc import start
from turtle import pos
import ephem
from ephem import degree
from datetime import datetime, timedelta

from matplotlib.pyplot import get
from jsonEditor import *

from scrapter import *
from App.config import URL_PATHS

jsonFile = jsonFileTrack("current satellite tracks", "C:/@T/learn_cesium/lc_one/App/static/tmp.json")


def give_datetime_str(date, jsonFile = False): 
    """ Ne donne pas l'heure UTC mais pour l'instant pas important 
    prend datetime en entree et retourne le format attendu par pyephem """

    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    second = date.second

    if jsonFile == True:
        return "{0}-{1:02}-{2:02}T{3:02}:{4:02}:{5:02}Z".format(year, month, day, hour, minute, second)
    else:
        return "{0}/{1:02}/{2:02} {3:02}:{4:02}:{5:02}".format(year, month, day, hour, minute, second)

def add_time_from_date(date, increment): 
    """ Retourne une date avec un increment en seconde sous le format attendu par pyephem """

    timestamp = int(datetime.timestamp(date))

    return give_datetime_str(datetime.fromtimestamp(timestamp + increment))

def create_sample(tle, nSamples, startDate, deltaT):
    """
        Calcule les positions, temps, etc ... 
        Pour un tle uniquement 
    """

    # on recupère l'objet
    trackedObject = ephem.readtle(tle[0], tle[1], tle[2]) 

    name = trackedObject.name

    position = []
    time_sequence = []

    current_date = give_datetime_str(startDate)

    for i in range(nSamples): 

        trackedObject.compute(current_date)

        position.append(((trackedObject.sublong / degree),(trackedObject.sublat / degree), (trackedObject.elevation)))
        time_sequence.append(current_date)

        current_date = add_time_from_date(startDate, i*deltaT) 

    return name, position, time_sequence, deltaT, startDate, nSamples

def computeAllTLE(TLE_list):
    """
        Edite un fichier lisible par le code javascript qui est en lien avec l'api cesium 
        Reflechir à faire varier le nombre de point de calcul de la trajectoire en fonction de la position du satellite
    """

    position_list = []
    name_list = []

    N = len(TLE_list)

    for i in range(N): 

        name, position, time_sequence, deltaT, startDate, nSamples = create_sample(TLE_list[i], 100, datetime.now(), 1000)
        name_list.append(name) 
        position_list.append(position)

    jsonFile.write(name_list, give_datetime_str(startDate, jsonFile=True), nSamples, deltaT, position_list, N)

def updateTLE(): 

    for constellation in URL_PATHS.keys():
        
        url = URL_PATHS[constellation][0]
        path = URL_PATHS[constellation][1]

        getFileFromURL(url, path) 

def getTLE_List(constellations): 

    TLE_list = []

    for const in constellations:
        objet = URL_PATHS[const]
        TLE_list += getTLEFromFile(objet[1]) 

    return TLE_list

def getSatDataFromTLE(TLE): 

    satName = TLE[0]

    l1 = TLE[1]
    l2 = TLE[2]

    inclinaison = float(l2[8:16])
    long_noeud_asc = float(l2[17:25])
    excentricite = float("0.{}".format(l2[26:33]))
    arg_peri = float(l2[34:42])
    anomalie_moyenne = float(l2[43:51])

    instant_mesure = l1[18:32]
    year = int("20{}".format(instant_mesure[:2]))
    
    Ndays = float(instant_mesure[2:])
    Nsec = (Ndays-1)*24*3600
    
    delta = timedelta(seconds=Nsec)
    date = datetime(year, 1, 1, 0, 0, 0) + delta

    print("inclinaison : {}\nlongitude noeud ascendant : {}\nexcentricite : {}\nargument du periastre : {}\nanomalie moyenne : {}\ninstant mesure : {}".format(inclinaison, long_noeud_asc, excentricite, arg_peri, anomalie_moyenne, instant_mesure))

    orbite = ""
    if excentricite == 0.0: 
        orbite = "circulaire"
    else:
        orbite = "elliptique"

    if inclinaison != 0.0: 
        orbite += " inclinée"
    else: 
        orbite += " ecliptique"

    print("orbite : {}".format(orbite))

    sat_objet = ephem.readtle(TLE[0], TLE[1], TLE[2]) 
    date_str = give_datetime_str(date)
    sat_objet.compute(date_str)

    long = sat_objet.sublong
    lat = sat_objet.sublat
    alt = sat_objet.elevation



getSatDataFromTLE(("ISS (ZARYA)","1 25544U 98067A   22123.52090565  .00011040  00000+0  20165-3 0  9994","2 25544  51.6443 197.8013 0006492  59.4449  68.9888 15.49916071338251"))          









#########################
#### CODE MANUEL POUR LE MOMENT 
##########################



