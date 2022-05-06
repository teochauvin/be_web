from msilib.schema import Error
from flask import Flask, redirect, render_template, render_template_string, request, redirect, session
import json


# MODULES PERSO 
from .model import bdd as bdd
from .controller import function as f
from .config import URL_PATHS
import get

app = Flask(__name__)

app.template_folder= "template"
app.static_folder= "static"
app.config.from_object('App.config')

# PAGE Index 
@app.route("/")
@app.route("/index")
@app.route("/index/<infoMsg>")
def index(infoMsg=''): 
    return render_template("index.html", info=infoMsg)

@app.route("/admin")
def admin(): 

    msg, listeMembre = bdd.get_membreData()
    return render_template("/admin.html", membre=listeMembre, UP = URL_PATHS)

# PAGE APPLICATION

@app.route("/cesium_app")
def ces():
    
    with open('C:/@T/learn_cesium/lc_one/App/static/tmp.json', 'r') as file: 
        data = json.load(file)

    info = f.is_connected()
    if info != "needAuth":
        return render_template("cesium_app.html", data=data)
    else: 
        return render_template("index.html")

# PAGE SIGNIN (prototype)

@app.route("/updateTle")
def updateTle(): 

    info = f.is_admin()
    if info != "Error": 
        
        get.updateTLE()

    return redirect("/admin")

@app.route("/editConfigFile", methods=['POST'])
def editConfigFile(): 

    info = f.is_admin()
    if info != "Error": 

        objet = list(request.form.keys())

        TLE_list = get.getTLE_List(objet)
        get.computeAllTLE(TLE_list)

    return redirect("/admin")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index")

# PAGE SIGNUP (ajoute un membre à la bdd ou reste sur la page)

@app.route("/signup") 
def signup():

    # debug pour afficher le contenu de la bdd
    # msg, listeMembre = bdd.get_membreData()

    return render_template("/signup.html")

# SIGNIN ?? 


@app.route("/connect", methods=['POST'])
def connect(): 

    login = request.form['login'] 
    password = request.form['mdp'] 
    
    msg = f.verify_user(login, password)
    print(msg)

    if "idUser" in session: 
        return redirect("/index")
    else: # echec authentification
        return redirect("/signin")


    


# AJOUTER UN MEMBRE 

@app.route("/addMembre", methods=['POST'])
def addMembre(): 
    
    nom = request.form['nom'] 
    prenom = request.form['prenom'] 
    login = request.form['login'] 
    mdp = request.form['mdp'] 
    mail = request.form['mail'] 
    avatar = request.form['avatar'] 
    statut = request.form['statut']

    msg, lastId = bdd.add_membreData(nom, prenom, mail, login, mdp, statut, avatar)

    print(msg)
    return redirect("/")
