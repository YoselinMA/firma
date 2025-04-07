from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Función de Dijkstra
def dijkstra(graph, start, end):
    distances = {node: float("inf") for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[end]

# Ruta principal para cargar la página web
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para calcular la ruta más corta
@app.route('/shortest-path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    graph = {node['node']: node['neighbors'] for node in data['nodes']}
    start_node = data['start_node']
    end_node = data['end_node']

    path, total_distance = dijkstra(graph, start_node, end_node)

    return jsonify({
        'path': path,
        'total_distance': total_distance
    })

if __name__ == '__main__':
    app.run(debug=False)  

