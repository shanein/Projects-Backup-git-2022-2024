import firebase_admin
from firebase_admin import credentials, db
import json

# fichier JSON d'authentification
cred = credentials.Certificate("dat-902-firebase-adminsdk-w81um-3682299bd4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dat-902-default-rtdb.europe-west1.firebasedatabase.app/'
})

data = json.load(open('data_insee.json'))

# Mapping des départements aux nouvelles régions
new_regions = {
    "ile-de-france": {"departments": ["75", "77", "78", "91", "92", "93", "94", "95"], "color": "#03AED2"},
    "bourgogne-franche-comté": {"departments": ["21", "25", "39", "58", "70", "71", "89", "90"], "color": "#7776B3"},
    "bretagne": {"departments": ["22", "29", "35", "56"], "color": "#FDDE55"},
    "centre-val de loire": {"departments": ["18", "28", "36", "37", "41", "45"], "color": "#615EFC"},
    "corse": {"departments": ["2A", "2B"], "color": "#F3CA52"},
    "grand est": {"departments": ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"], "color": "#F6E9B2"},
    "hauts-de-france": {"departments": ["02", "59", "60", "62", "80"], "color": "#0A6847"},
    "auvergne-rhone-alpes": {"departments": ["01", "03", "07", "15", "26", "38", "42", "43", "63", "69", "73", "74"], "color": "#7aBa78"},
    "normandie": {"departments": ["14", "27", "50", "61", "76"], "color": "#028391"},
    "nouvelle-aquitaine": {"departments": ["16", "17", "19", "23", "24", "33", "40", "47", "64", "79", "86", "87"], "color": "#C39898"},
    "occitanie": {"departments": ["09", "11", "12", "30", "31", "32", "34", "46", "48", "65", "66", "81", "82"], "color": "#808836"},
    "pays de la loire": {"departments": ["44", "49", "53", "72", "85"], "color": "#FFA27F"},
    "provence-alpes-côte d'azur": {"departments": ["04", "05", "06", "13", "83", "84"], "color": "#254336"}
}

countries = {}
country_id = 'country1'
country_name = 'France'

for item in data:
    department_id = item["code_dept"]
    commune_id = item["insee_com"]
    commune_population = item["population"] * 1000

    region_id = None
    for region_name, region_data in new_regions.items():
        if department_id in region_data["departments"]:
            region_id = region_name
            break

    if region_id is None:
        continue

    if country_id not in countries:
        countries[country_id] = {
            "name": country_name,
            "population": 0,
            "averagePropertyPrice": None,
            "regions": {}
        }

    regions = countries[country_id]["regions"]
    if region_id not in regions:
        regions[region_id] = {
            "name": region_id,
            "population": 0,
            "averagePropertyPrice": None,
            "departments": {}
        }

    departments = regions[region_id]["departments"]
    if department_id not in departments:
        departments[department_id] = {
            "code": department_id,
            "name": item["nom_dept"][0],
            "population": 0,
            "averagePropertyPrice": None,
            "communes": {}
        }

    communes = departments[department_id]["communes"]
    geoshape = {
        "type": "Polygon",
        "coordinates": item["geo_shape"]["geometry"]["coordinates"]
    }
    communes[commune_id] = {
        "name": item["nom_comm"],
        "population": commune_population,
        "averagePropertyPrice": None,
        "postalCode": item["postal_code"],
        "superficie": item["superficie"],
        "geo_point_2d": item["geo_point_2d"],
        "geoshape": geoshape
    }

    # Add commune population to department population
    departments[department_id]["population"] += commune_population

    # Add department population to region population
    regions[region_id]["population"] += commune_population

    # Add region population to country population
    countries[country_id]["population"] += commune_population


# Fonction pour ajouter des données à Realtime Database (réécrit les données existantes)
def add_data_to_realtime_db(data):
    ref = db.reference('countries')
    ref.set(data)  # Utilise set() pour écraser les données existantes

# Réécrire les données structurées à Realtime Database
add_data_to_realtime_db(countries)
