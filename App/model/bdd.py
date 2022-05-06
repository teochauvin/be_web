import mysql.connector 
from mysql.connector import errorcode
from ..config import DB_SERVER

# connexion au serveur de BDD
def connexion():
    cnx= ""
    
    try:
        cnx= mysql.connector.connect(**DB_SERVER)
        error= None

    except mysql.connector.Error as err:
        error= err
        if err.errno== errorcode.ER_ACCESS_DENIED_ERROR:
            print("Mauvais login ou mot de passe")
        elif err.errno== errorcode.ER_BAD_DB_ERROR:
            print("La Base de données n'existe pas.")
        else:
            print(err)

    return cnx, error # error: remonte problème connexion# fermeture de la connexion au serveur de BDDdefclose_bd(cursor, cnx):cursor.close()cnx.close()

# fermeture de la connexion au serveur de BDD
def close_bd(cursor, cnx):
    cursor.close()
    cnx.close()

# Toutes les données de la table membres
def get_membreData():

    try:
        cnx, error = connexion()
        if error is not None: 
            return error, None # Problème connexion BDD
        
        cursor= cnx.cursor(dictionary=True)
        sql= "SELECT * FROM identification"

        cursor.execute(sql)

        listeMembre= cursor.fetchall()

        close_bd(cursor, cnx)
        msg = "OKmembres"
    
    except mysql.connector.Error as err:
        listeMembre= None
        msg = "Failedgetmembres data : {}".format(err)

    return msg, listeMembre

def del_membreData(idUser): 

    try: 
        cnx, error = connexion()
        if error is not None: 
            return error, None

        cursor = cnx.cursor(dictionary=True)
        sql = "DELETE FROM identification WHERE idUser={}".format(idUser)

        cursor.execute(sql)
        cnx.commit()

        close_bd(cursor, cnx)
        msg = "suppMembreOK"
    
    except mysql.connector.Error as err: 
        msg = "Failedgetmembres data : {}".format(err)

    return msg

# add update_membreData

def add_membreData(nom, prenom, mail, login, mdp, statut, avatar): 

    try: 
        cnx, error = connexion()
        if error is not None: 
            return error, None 

        cursor = cnx.cursor(dictionary = True) 

        sql = "INSERT INTO identification (nom, prenom, mail, login, MotPasse, statut, avatar) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        param=(nom, prenom, mail, login, mdp, statut, avatar)
        cursor.execute(sql, param)

        lastId = cursor.lastrowid
        cnx.commit()

        close_bd(cursor, cnx)
        msg = "addMembreOK" 

    except mysql.connector.Error as err: 

        msg = "Fail add member : {}".format(err) 
        print(msg)
        lastId = None

    return msg, lastId 

def verifAuthData(login, mdp):

    try:
        cnx, error = connexion()
        if error is not None:
            return error, None
        
        cursor = cnx.cursor(dictionary=True)

        sql = "SELECT * FROM identification WHERE login=%s and motPasse=%s"
        param=(login, mdp)
        cursor.execute(sql, param)

        user = cursor.fetchone()
        close_bd(cursor, cnx)
        
        msg = "authOK"
    
    except mysql.connector.Error as err:
        user = None
        msg = "Failed get Auth data : {}".format(err)

    return msg, user

def get_SatelliteData(): 

    try:
        cnx, error = connexion()
        if error is not None: 
            return error, None # Problème connexion BDD
        
        cursor= cnx.cursor(dictionary=True)
        sql= "SELECT * FROM satellites"

        cursor.execute(sql)

        listeSats = cursor.fetchall()

        close_bd(cursor, cnx)
        msg = "OKsats"
    
    except mysql.connector.Error as err:
        listeMembre= None
        msg = "Failedgetmembres data : {}".format(err)

    return msg, listeMembre

def add_SatelliteData(TLE): 

    # convert TLE text into usable data

    # add them in database 

    return 1 