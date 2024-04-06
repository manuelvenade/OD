import numpy as np
import matplotlib.pyplot as plt
import os

# Function to calculate the distance between two cities
def distance(city1, city2):
    return np.linalg.norm(city1 - city2)

# Function to calculate total distance of a tour
def tour_distance(tour, cities):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance(cities[tour[i]], cities[tour[i+1]])
    total_distance += distance(cities[tour[-1]], cities[tour[0]])  # Return to starting city
    return total_distance

# 2-opt local search
def two_opt(cities, tour):
    improved = True
    best_distance = tour_distance(tour, cities)
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue  # changes nothing, skip then
                new_tour = tour.copy()
                new_tour[i:j] = tour[j - 1:i - 1:-1]  # reverse segment
                new_distance = tour_distance(new_tour, cities)
                if new_distance < best_distance:
                    tour = new_tour
                    best_distance = new_distance
                    improved = True
    return  tour, best_distance


# Plot tour function
def plot_tour(cities, tour):
    tour_cities = cities[tour]
    plt.plot(tour_cities[:, 0], tour_cities[:, 1], 'co-')
    plt.plot([tour_cities[-1, 0], tour_cities[0, 0]], [tour_cities[-1, 1], tour_cities[0, 1]], 'co-')  # Return to starting city
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Best Tour')
    plt.grid(True)
    plt.show()

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

# Example usage
if __name__ == "__main__":
    np.random.seed(40) # Para poder repetir o obter mm resultados sem stress
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #File name - file need to be in the directory of the program
    file_name = "dj38.tsp"

    file_path = os.path.join(current_directory, file_name)

    #Convert tsp file in array
    cities = read_tsp_file(file_path)

    num_particles = 20
    max_iter = 10

    tour = np.random.permutation(len(cities))
    best_tour, best_distance = two_opt(cities,tour)

    print("Best tour:", best_tour)
    print("Best distance:", best_distance)

    # Plot the best tour
    plot_tour(cities, best_tour)
