from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable, LpStatusOptimal, PULP_CBC_CMD
import matplotlib.pyplot as plt

def main(points):
    # Define the points and construct the distance matrix
    points = {
        
        0: (11003.611100, 42102.500000),
        1: (11108.611100, 42373.888900),
        2: (11133.333300, 42885.833300),
        3: (11155.833300, 42712.500000),
        4: (11183.333300, 42933.333300),
        5: (11297.500000, 42853.333300),
        6: (11310.277800, 42929.444400),
        7: (11416.666700, 42983.333300),
        8: (11423.888900, 43000.277800),
        9: (11438.333300, 42057.222200),
        10: (11461.111100, 43252.777800),
        11: (11485.555600, 43187.222200),
        12: (11503.055600, 42855.277800),
        13: (11511.388900, 42106.388900),
        14: (11522.222200, 42841.944400),
        15: (11569.444400, 43136.666700),
        16: (11583.333300, 43150.000000),
        17: (11595.000000, 43148.055600),
        18: (11600.000000, 43150.000000),
        19: (11690.555600, 42686.666700),
        20: (11715.833300, 41836.111100),
        21: (11751.111100, 42814.444400),
        22: (11770.277800, 42651.944400),
        23: (11785.277800, 42884.444400),
        24: (11822.777800, 42673.611100),
        25: (11846.944400, 42660.555600),
        26: (11963.055600, 43290.555600),
        27: (11973.055600, 43026.111100),
        28: (12058.333300, 42195.555600),
        29: (12149.444400, 42477.500000),
        30: (12286.944400, 43355.555600),
        31: (12300.000000, 42433.333300),
        32: (12355.833300, 43156.388900),
        33: (12363.333300, 43189.166700),
        34: (12372.777800, 42711.388900),
        35: (12386.666700, 43334.722200),
        36: (12421.666700, 42895.555600),
        37: (12645.000000, 42973.333300)
    }
    num_points = len(points)
    
    dist = {(i, j): ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2) ** 0.5 for i in points for j in points if i != j}

    # Create the problem
    problem = LpProblem("TSP", LpMinimize)

    # Decision variables
    x = LpVariable.dicts("x", dist, cat='Binary')
    u = LpVariable.dicts("u", points, lowBound=0, cat='Continuous')  # MTZ variables without an upper bound

    # Objective function
    problem += lpSum(dist[(i, j)] * x[(i, j)] for (i, j) in dist)

    # Degree constraints
    for i in points:
        problem += lpSum(x[(i, j)] for j in points if (i, j) in dist) == 1  # Exactly one outgoing edge
        problem += lpSum(x[(j, i)] for j in points if (j, i) in dist) == 1  # Exactly one incoming edge

    # MTZ subtour elimination constraints
    # We exclude the first node from these constraints to prevent infeasibility
    for i in points:
        for j in points:
            if i != j and i != 0 and j != 0 and (i, j) in dist:
                problem += u[i] - u[j] + len(points) * x[(i, j)] <= len(points) - 1

    # Additional constraint to fix the position of the first node and prevent infeasibility
    problem += u[0] == 0

    # Solve the problem
    problem.solve(PULP_CBC_CMD(msg=0))  # Use msg=0 to disable most of the CBC output

    # Check the solution status
    if problem.status == LpStatusOptimal:
        # Extract and print the solution
        solution = [(i, j) for (i, j) in dist if x[(i, j)].varValue == 1]
        print("Optimal Tour:", solution)

        total_distance = sum(dist[(i, j)] for (i, j) in solution)
        print("Total Distance:", total_distance)

        # Plot the tour
        plt.figure(figsize=(10, 10))
        for (i, j) in solution:
            plt.plot([points[i][0], points[j][0]], [points[i][1], points[j][1]], 'b')
        for i, (x, y) in points.items():
            plt.plot(x, y, 'ro')
            plt.text(x, y, str(i), color='black')
        plt.title('Optimal TSP Tour')
        plt.show()
    else:
        print('The problem status is:', LpStatus[problem.status])

if __name__ == "__main__":
    main()
