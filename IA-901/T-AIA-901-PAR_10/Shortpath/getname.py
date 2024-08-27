### Fichier test ###

import requests
import pandas as pd

def get_city_from_station_osm(station_name):
    base_url = "https://nominatim.openstreetmap.org/search?addressdetails="
    params = {
        "q": station_name,
        "format": "json"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            for item in data:
                address = item.get('address', {})
                city = address.get('city')
                municipality = address.get('municipality')
                town = address.get('town')
                if city:
                    return city  # Ajuster selon le format réponse
                elif town:
                    return town  # Ajuster selon le format réponse
                elif municipality:
                    return municipality  # Ajuster selon le format réponse
                else:
                    print("Nothing found")
                    return "Nothing"
    else :
        print("Error fetch")

# # Exemple d'utilisation
# station_name = "Gare montparnasse"
# city = get_city_from_station_osm(station_name)
# print(city)

df = ["Aix-les-Bains-le-Revard",
"Bas-Monistrol",
"Basel-SBB",
"Beauvais-Gare-SNCF",
"Bellegarde-s-V. Gare",
"Bergerac",
"Bidos",
"Bédarieux",
"Cambrai Ville",
"Carmaux",
"Chambéry-Chal.-les-Eaux",
"Champagnole-PE-Victor",
"Charmes (Vosges)",
"Cluses (Hte-Savoie)",
"Contrexéville",
"Delle",
"Dijon-Porte-Neuve",
"Dives-Cabourg",
"Dormans",
"Eguzon",
"Entzheim-Aéroport",
"Franois",
"Freiburg-Breisgau",
"Hirson-Ecoles",
"Krimmeri-Meinau",
"L'Isle-Jourdain (Gers)",
"La Douzillère",
"La-Rochelle-Pt-Dauphine",
"Landau-Pfalz-Hbf",
"Le Valdahon",
"Longueville (S.-et-M.)",
"Lutterbach Tram-train",
"Lyon-Gorge-de-Loup",
"Marle-sur-Serre",
"Mazamet",
"Meroux",
"Monaco-Monte-Carlo",
"Montauban-Ville-Bourbon",
"Montréjeau-Gourdan-Pol.",
"Mullheim-Baden-Bf",
"Neustadt (Weinstr) Hbf",
"Nevers-Le-Banlay",
"Nouan-le-Fuzelier",
"Offenburg",
"Paris-Montp.3-Vaug.",
"Paris-Montparnasse 1-2",
"Pauillac",
"Port-Bou",
"Rang du Fl. Verton Ber.",
"Rethel",
"Ribécourt",
"Romans-Bourg-de-Péage",
"Sarlat",
"Sathonay-Rillieux",
"St-André-le-Gaz",
"St-Emilion",
"St-Flour-Chaudes-Aigues",
"St-Gervais-L-B-Le-Fayet",
"St-Just-SNCF",
"St-Raphaël-Valescure",
"Thann-Saint-Jacques",
"Trier-Hbf (Trèves)",
"Vallon-en-Sully",
"Vallorbe-Cff",
"Vauvert",
"Vendôme-Villiers-s-Loir",
"Ventimiglia-Stazione",
"Verneuil-sur-Serre",
"Villedieu (Gare)",
"Villefranche-Vernet-l.B",
"Villers-les-Pots",
"Voves",
"WINDEN PFALZ",
"WOERTH RHEIN"
]
stations = []
done = []
for row in df :
    if row not in done :
        city = get_city_from_station_osm(str(row))
        if city :
            stations.append(city + ";" + row)
            done.append(row)
        else :
            stations.append("Unknown" + ";" + row)
            done.append(row)
print(stations)