from unittest import getTestCaseNames
import urllib.request


def getFileFromURL(url, path):
    """
        Peut lire une page du site celestrack et la convertir en fichier txt 
    """

    req = urllib.request.Request(url)
    
    with urllib.request.urlopen(req) as response:
        lignes = response.readlines()

    with open(path, 'w') as f:
        for ligne in lignes:
            f.write("{}".format(ligne.decode().replace("\n","")))

    print("file {} updated".format(path))

def getTLEFromFile(path): 

    liste_tle = []

    with open(path, 'r') as f:

        lines = f.readlines()
        tle = []

        for i in range(len(lines)): 

            if i % 3 == 0 and i!=0:
                liste_tle.append(tle) 
                tle = [] 

            tle.append(lines[i].replace("\n", "")) 

    return liste_tle

def getTLE(url, path): 

    getFileFromURL(url, path)

    TLE_list = getTLEFromFile(path) 

    return TLE_list