### Fichier calculant l'itinéraire entre une ville de départ et une ville d'arrivée.
## S'appuie sur les données des gares SNCF et des versions modifiées des fichiers timetables.csv et stop_times.txt, initialement fournis dans l'énoncé.

# import pandas as pd
import heapq


def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    previous_nodes = {vertex: None for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes

def get_path(stations, previous_nodes, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.insert(0, uic_to_station(stations, current_node))
        current_node = previous_nodes[current_node]
    path.insert(0, uic_to_station(stations, start))
    return path

def uic_to_station(stations, uic) :
    return stations[str(uic)]["station"]

def city_to_uic(stations, city) :
    return {i for i in stations if stations[i]["city"]==city}

def get_best_path(graph, stations, start, end) :
    from_candidates = city_to_uic(stations, start)
    to_candidates = city_to_uic(stations, end)
    best_trip = {"distance":0}
    for candidate in from_candidates  :
        distances, previous_nodes = dijkstra(graph, int(candidate))
        # Find lowest distance with other group of stations and keep it
        for dest in to_candidates :
            if best_trip["distance"] == 0 or distances[int(dest)] < best_trip["distance"] :
                best_trip = {
                    "start_station":candidate,
                    "end_station":dest,
                    "distance":distances[int(dest)],
                    "distances":distances,
                    "previous_nodes":previous_nodes
                }
    return best_trip
#
#
# start_city = "Paris"
# end_city = "Marseille"
#
# best_trip = get_best_path(start_city, end_city)
# print(best_trip)
#
# path = get_path(best_trip["previous_nodes"], int(best_trip["start_station"]), int(best_trip["end_station"]))
# print(f"Le chemin le plus court de {start_city} à {end_city} est : {path} avec une durée de {best_trip['distance']} minutes.")
#

def format_duration(duration_minutes):
    # Calcul des heures et des minutes
    hours = duration_minutes // 60
    minutes = duration_minutes % 60

    # Construction du texte formaté
    if hours > 0:
        if hours == 1:
            hour_text = "1 heure"
        else:
            hour_text = f"{hours} heures"

        if minutes == 1:
            minute_text = "1 minute"
        else:
            minute_text = f"{minutes} minutes"

        return f"{hour_text} et {minute_text}"
    else:
        if minutes == 1:
            return "1 minute"
        else:
            return f"{minutes} minutes"

def get_shortpath(graph, stations, start_city, end_city):
    best_trip = get_best_path(graph, stations, start_city, end_city)
    # print(best_trip)

    path = get_path(stations, best_trip["previous_nodes"], int(best_trip["start_station"]), int(best_trip["end_station"]))

    formatted_duration = format_duration(best_trip['distance'])
    print(f"Le chemin le plus court de {start_city} à {end_city} est : {path} avec une durée de {best_trip['distance']} minutes.")

    ##return f"Le chemin le plus court de {start_city} à {end_city} est : \n{path} \navec une durée de {best_trip['distance']} minutes."
    return f"Le chemin le plus court de {start_city} à {end_city} est : \n{path} \navec une durée de {formatted_duration}."


#
# best_trip2 = get_best_path("Nice", "Limoges")
# print(best_trip2)
# path2 = get_path(best_trip2["previous_nodes"], int(best_trip2["start_station"]), int(best_trip2["end_station"]))
# print(f"Le chemin le plus court de Nice à Limoge est : {path2} avec une durée de {best_trip2['distance']} minutes.")
#
#


#a mettre dans le main en haut#
# df = pd.read_csv('data_sncf_shortpath/timetable_OLD.csv')
#
# graph = {}
# for _, row in df.iterrows():
#     graph.setdefault(row['from'], []).append((row['to'], row['duration']))
#     graph.setdefault(row['to'], []).append((row['from'], row['duration']))
#
# stations = pd.read_json('data_sncf_shortpath/stations.json', convert_axes=False)
###

#a mettre dans le main pour l'utilisation en bas###
# try:
#     get_shortpath(graph, stations, "Parssis", "Nice")
# except ValueError:
#     print("L'itinéraire n'a pas été trouvé, veuillez réessayer.")
# except KeyError as e:
#     print(f"L'une des villes de départ ou de destination n'a pas été trouvée dans la base SNCF. Veuillez indiquer un itinéraire de villes pris en charge par les gares SNCF de France.")

###
