import firebase_admin
from firebase_admin import credentials, db

# Utilisez le fichier JSON d'authentification que vous avez téléchargé depuis Firebase
cred = credentials.Certificate('epitech-data-firebase-adminsdk-1cv4i-75af237ed3.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://epitech-data-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Référence à la racine de la base de données
ref = db.reference('/')

# Effacer toutes les données
ref.set(None)

print("Toutes les données ont été effacées.")
