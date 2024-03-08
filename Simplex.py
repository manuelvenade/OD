import numpy as np

def perform_simplex_iterations(tableau):
    m, n = tableau.shape
    num_variables, num_constraints = n - 1, m - 1
    
    iteration = 0
    while True:
        print(f"Simplex Tableau at Iteration {iteration}:")
        print(tableau)
        print("\n")
        
        # Break if there are no more opportunities to minimize (no negative coefficients in the objective function row)
        if np.all(tableau[-1, :-1] >= 0):
            break

        # Select pivot column (column with the most negative coefficient in the objective function row for minimization)
        pivot_col = np.argmin(tableau[-1, :-1])
        
        # Perform the ratio test to select the pivot row
        ratios = np.array([tableau[i, -1] / tableau[i, pivot_col] if tableau[i, pivot_col] > 0 else np.inf for i in range(num_constraints)])
        pivot_row = np.argmin(ratios)
        
        # Pivot operation
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element
        for i in range(m):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]
        
        iteration += 1

    # Extracting the solution
    solution = np.zeros(num_variables)
    for j in range(num_variables):
        col = tableau[:-1, j]
        if np.sum(col == 1) == 1 and np.sum(col) == 1:
            row_index = np.where(col == 1)[0][0]
            solution[j] = tableau[row_index, -1]

    # Objective value is taken directly from the tableau, reflecting minimized cost
    objective_value = tableau[-1, -1]
    
    return solution, objective_value

def initialize_tableau_for_minimization(cost_matrix):
    num_agents = cost_matrix.shape[0]
    c = -cost_matrix.flatten()  # Invert the sign for minimization

    # Construct the A matrix for the assignment constraints
    A = np.zeros((num_agents * 2, num_agents ** 2))
    for i in range(num_agents):
        A[i, i*num_agents:(i+1)*num_agents] = 1
    for j in range(num_agents):
        A[num_agents + j, j::num_agents] = 1
    b = np.ones(num_agents * 2)  # Constraints' RHS values
    
    # Assemble the simplex tableau
    tableau = np.vstack([
        np.hstack([A, b.reshape(-1, 1)]),  # Constraint equations
        np.hstack([c, [0]])  # Objective function row, used as is for minimization
    ])
    
    return tableau

# Example usage
cost_matrix = np.array([
    [50, 34, 62],
    [66, 81, 14],
    [29, 65, 30]
])

# Initialize the tableau for minimization
tableau = initialize_tableau_for_minimization(cost_matrix)

# Perform the simplex method iterations
solution_vector, max_profit = perform_simplex_iterations(tableau)

# Reshape the solution vector back into a matrix format
solution_matrix = solution_vector.reshape(cost_matrix.shape)

print("Optimal Assignment (Solution Matrix):\n", solution_matrix)
print("Maximum Total Profit:", max_profit)  # Note the negative sign for maximum profit
