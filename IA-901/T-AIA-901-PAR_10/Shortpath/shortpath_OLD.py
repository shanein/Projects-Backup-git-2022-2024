import pandas as pd
import heapq

df = pd.read_csv('timetable_OLD.csv')

df[['from', 'to']] = df['start'].str.split(' -- ', expand=True)

df.rename(columns={'duree': 'duration'}, inplace=True)

graph = {}
for _, row in df.iterrows():
    graph.setdefault(row['from'], []).append((row['to'], row['duration']))
    graph.setdefault(row['to'], []).append((row['from'], row['duration']))

# print(graph)
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

def get_path(previous_nodes, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    path.insert(0, start)
    return path

start_station = "Gare de Paris-Gare-de-Lyon"
end_station = "Gare de Marseille-St-Charles"
distances, previous_nodes = dijkstra(graph, start_station)
path = get_path(previous_nodes, start_station, end_station)

print(f"Le chemin le plus court de {start_station} à {end_station} est : {path} avec une durée de {distances[end_station]} minutes.")