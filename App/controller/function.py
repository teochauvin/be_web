from csv import excel_tab
from flask import Flask, redirect, render_template, render_template_string, request, redirect, session
from ..model import bdd

def verify_user(login, password):

    session.clear()
    msg, user = bdd.verifAuthData(login, password)

    try: 
        session["idUser"] = user["idUser"]
        session["nom"] = user["nom"] 
        session["prenom"] = user["prenom"] 
        session["mail"] = user["mail"] 
        session["login"] = user["login"]
        session["mdp"] = user["motPasse"] 
        session["statut"] = user["statut"] 
        session["avatar"] = user["avatar"]

        info = msg

    except TypeError as err:
        info="authEchec"
        print("Failed verifAuth : {}".format(err))

    return info

def is_connected(): 
    """ empecher les utilisateurs non connectés d'utiliser l'app"""

    if session.get("idUser") is None:
        return "needAuth" 
    else: 
        return "Connected"

def is_admin():

    if not session.get("idUser") is None:
        if session["statut"] == 0: 
            return "Admin"
    else: 
        return "Error"