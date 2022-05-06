# be_web

fichier externe à l'application : 
get -> gère les interraction avec les TLE, le site Celestrack et le module pyephem 
jsonEditor -> code temporaire qui permet d'éditer un fichier de type json pour communiquer des infos au code javascript
scrapter -> code qui permet d'aller extraire les TLE du site Celestrack et de les stocker dans des fichiers textes 
run -> lance l'application 

dans l'application : App
meme strcture que dans le cours 

Avant de lancer l'app verifier d'avoir les modules 
pyephem, urllib, matplotlib ...

## fonctionnalité 

On peut se connecter et donc créer un utilisateur 
Si l'utilisateur est 'admin' il a acces a un page web speciale ou il peut voir tous les autres utilisateurs et les satellites de la base de donnée
Présence d'un bouton Update pour actualiser les TLE mais cette fonctionnalité est temporaire puisque apres les TLE seront plutot rajoutés à la main 

## bdd et xaamp

Il faut lancer mysql et vérifier que les mdp correspondent à ceux du fichier config 

