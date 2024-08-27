import firebase_admin
from firebase_admin import credentials, db

# fichier JSON d'authentification
cred = credentials.Certificate("dat-902-firebase-adminsdk-w81um-3682299bd4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dat-902-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Fonction pour récupérer les données de la commune spécifique
def get_commune_geoshape(commune_id):
    ref = db.reference('countries/country1/regions')
    regions = ref.get()

    for region_id, region_data in regions.items():
        departments = region_data.get('departments', {})
        for department_id, department_data in departments.items():
            communes = department_data.get('communes', {})
            if commune_id in communes:
                return communes[commune_id].get('geoshape')

    return None

# Récupérer et afficher les coordonnées de la commune 63402
commune_id = "63402"
geoshape = get_commune_geoshape(commune_id)

if geoshape:
    print(f"Geoshape for commune {commune_id}: {geoshape}")
else:
    print(f"No geoshape found for commune {commune_id}")
