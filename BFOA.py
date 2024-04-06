import numpy as np
import random
import matplotlib.pyplot as plt
import os

def distance(point1, point2):   
    return np.linalg.norm(point1 - point2)


def total_distance(route, cities):
    total = 0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i+1]])
    total += distance(cities[route[-1]], cities[route[0]])
    return total


def initialize_bacteria(num_bacteria, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(num_bacteria)]


def update_bacteria_position(bacteria, cities, step_size):
    new_bacteria = list(bacteria)
    idx1, idx2 = random.sample(range(len(bacteria)), 2)
    temp = new_bacteria[idx1]
    new_bacteria[idx1] = new_bacteria[idx2]
    new_bacteria[idx2] = temp
    if total_distance(new_bacteria, cities) < total_distance(bacteria, cities) or random.random() < step_size:
        return new_bacteria
    return bacteria


def bfoa_tsp(num_bacteria, num_cities, cities, num_iterations):
    step_size = 0.2  #
    bacteria = initialize_bacteria(num_bacteria, num_cities)
    for _ in range(num_iterations):
        for i in range(num_bacteria):
            bacteria[i] = update_bacteria_position(bacteria[i], cities, step_size)
        step_size *= 0.98  
    # Encontrando a melhor solução
    best_solution = min(bacteria, key=lambda x: total_distance(x, cities))
    return best_solution, total_distance(best_solution, cities)


#Function to read .tsp file
def read_tsp_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        # Skip the header
        while True:
            line = file.readline()
            if line.strip() == "NODE_COORD_SECTION":
                break
        # Read the coordinates
        for line in file:
            if line.strip() == "EOF":
                break
            _, x, y = line.strip().split()
            coordinates.append([float(x), float(y)])

    coordinates = np.array(coordinates)

    return coordinates


if __name__ == "__main__":
    
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #File name - file need to be in the directory of the program
    file_name = "dj38.tsp"

    file_path = os.path.join(current_directory, file_name)

    #Convert tsp file in array
    cities = read_tsp_file(file_path)

    num_cities = len(cities)
    num_bacteria = 150
    num_iterations = 1500

   
    best_solution, best_distance = bfoa_tsp(num_bacteria, num_cities, cities, num_iterations)
    
    print("Melhor solução encontrada:", best_solution)
    print("Distância total da melhor solução:", best_distance)

    
    plt.figure(figsize=(8, 6))
    plt.scatter(cities[:,0], cities[:,1], color='red', label='Cities')
    for i in range(num_cities):
        plt.annotate(i, (cities[i,0]+0.1, cities[i,1]+0.1), fontsize=12)
    best_route_cities = [cities[i] for i in best_solution]
    best_route_cities.append(best_route_cities[0]) 
    best_route_cities = np.array(best_route_cities)
    plt.plot(best_route_cities[:,0], best_route_cities[:,1], color='blue', marker='o', linestyle='-', linewidth=1, markersize=6, label='Best Route')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('BFOA')
    plt.legend()
    plt.grid(True)
    plt.show()
