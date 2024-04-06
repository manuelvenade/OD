import numpy as np
import matplotlib.pyplot as plt
import os

class Particle:
    def __init__(self, num_cities):
        self.route = np.random.permutation(num_cities)
        self.velocity = np.zeros(num_cities)
        self.best_route = np.copy(self.route)
        self.best_cost = float('inf')

def distance(city1, city2):
    # Calculate Euclidean distance between two cities
    return np.linalg.norm(city1 - city2)

def total_distance(path, cities):
    # Calculate total distance for a given path
    dist = 0
    for i in range(len(path) - 1):
        dist += distance(cities[path[i]], cities[path[i + 1]])
    dist += distance(cities[path[-1]], cities[path[0]])  
    return dist

def initialize_particles(num_particles, num_cities):
    particles = []
    for _ in range(num_particles):
        particles.append(Particle(num_cities))
    return particles

def update_velocity(particle, global_best_route, c1, c2, w):
    r1 = np.random.rand(len(particle.velocity))
    r2 = np.random.rand(len(particle.velocity))
    particle.velocity = w * particle.velocity + \
                        c1 * r1 * (particle.best_route - particle.route) + \
                        c2 * r2 * (global_best_route - particle.route)
    

def update_route(particle, cities):
    new_route = particle.route + particle.velocity
    

    particle.route = np.roll(particle.route, int(np.random.rand() * len(particle.route)))
    
    print("test")
    print (particle.route)
    print(new_route)

def update_best(particle, cities):
    current_cost = total_distance(particle.route, cities)
    if current_cost < particle.best_cost:
        particle.best_cost = current_cost
        particle.best_route = np.copy(particle.route)

def get_global_best(particles, cities):
    global_best_cost = float('inf')
    global_best_route = None
    for particle in particles:
        particle_cost = total_distance(particle.route, cities)
        if particle_cost < global_best_cost:
            global_best_cost = particle_cost
            global_best_route = np.copy(particle.route)
    return global_best_route

def particle_swarm_optimization(cities, num_particles, num_iterations, c1, c2, w):
    num_cities = len(cities)
    particles = initialize_particles(num_particles, num_cities)
    global_best_route = get_global_best(particles, cities)
    for _ in range(num_iterations):
        count=0
        for particle in particles:
            update_velocity(particle, global_best_route, c1, c2, w)
            update_route(particle, cities)
            update_best(particle, cities)
            if count == 29:
                print(count , '  '  , particle.best_cost)
            count += 1
        global_best_route = get_global_best(particles, cities)
        

    best_route = global_best_route.tolist()
    best_route.append(best_route[0])  
    best_distance = total_distance(best_route, cities)
    
    return best_route, best_distance

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
    np.random.seed(40) # Para poder repetir o obter mm resultados sem stress
    
    current_directory = os.path.dirname(os.path.abspath(__file__))

    #File name - file need to be in the directory of the program
    file_name = "dj38.tsp"

    file_path = os.path.join(current_directory, file_name)

    #Convert tsp file in array
    cities = read_tsp_file(file_path)

    num_particles=30
    num_iterations=200
    c1=2.5
    c2=1.5
    w=2
    best_route, best_distance = particle_swarm_optimization(cities, num_particles, num_iterations, c1, c2, w)
    
    print("Best route found:", best_route)
    print("Total distance of the best route:", best_distance)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(cities[:,0], cities[:,1], color='red', label='Cities')
    for i in range(len(cities)):
        plt.annotate(i, (cities[i,0]+0.1, cities[i,1]+0.1), fontsize=12)
    best_route_cities = [cities[i] for i in best_route]
    best_route_cities.append(best_route_cities[0]) 
    best_route_cities = np.array(best_route_cities)
    plt.plot(best_route_cities[:,0], best_route_cities[:,1], color='blue', marker='o', linestyle='-', linewidth=1, markersize=6, label='Best Route')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('TSP using PSO')
    plt.legend()
    plt.grid(True)
    plt.show()
