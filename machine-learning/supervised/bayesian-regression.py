import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.stats import norm
import sympy as sp

def complicated_function(x):
    return np.sin(x)
num_points = 100
x_data = np.linspace(0, 3, num_points)
y_data = complicated_function(x_data) + np.random.normal(0, 0, num_points)

# Prepare JSON data structure
jsonRawData = json.dumps({
    "data": list(zip(x_data, y_data)),
    "dataSD": 0.5,
    "parameters": [0.0, 0.0, 0.0],
    "parametersSD": 2,
    "function": "p1*x^0 + p2*x^1 + p3*x^2",
    "resolution": 100,
    "domain": [0.0, 3.0],
    "confidenceIntervalCutoff": 0.99,
    "monteCarloTrials": 1000
})

# Parse JSON
rawData = json.loads(jsonRawData)
data = np.array(rawData["data"], dtype=np.float64)
dataSD= rawData["dataSD"]
parameters = np.array(rawData["parameters"], dtype=np.float64)
parametersSD= rawData["parametersSD"]
function = rawData["function"]
resolution = rawData["resolution"]
domain = rawData["domain"]
confidenceIntervalCutoff = rawData["confidenceIntervalCutoff"]
monteCarloTrials = rawData["monteCarloTrials"]

# Parse function into a callable lambda
def parse_function(func_string, num_params):
    symbols = sp.symbols(f'p1:{num_params+1}, x')
    func_expr = sp.sympify(func_string)
    return sp.lambdify(symbols, func_expr, 'numpy')

func_lambda = parse_function(function, len(parameters))

# Monte Carlo Simulation for Posterior Distribution (log normalisation for numerical stability)
params_samples = []
log_posterior_values = []

for _ in range(monteCarloTrials):
    new_params = parameters + np.random.normal(0, parametersSD, size=parameters.shape)
    log_prior = -0.5*len(parameters)*np.log(2*np.pi*parametersSD**2) - 0.5*np.sum(((new_params - parameters)/parametersSD)**2)
    log_likelihood = 0.0  # Changed from 1.0 to 0.0 for log space
    for x, t in data:
        t_pred = func_lambda(*new_params, x)
        log_likelihood += -0.5 * np.log(2 * np.pi * dataSD**2) - 0.5 * ((t - t_pred)/dataSD)**2
    log_posterior = log_likelihood + log_prior
    
    params_samples.append(new_params)
    log_posterior_values.append(log_posterior)

# Convert to NumPy arrays
params_samples = np.array(params_samples)
log_posterior_values = np.array(log_posterior_values)

# Normalize posteriors
max_log_posterior = np.max(log_posterior_values)
log_marginal = max_log_posterior + np.log(np.sum(np.exp(log_posterior_values - max_log_posterior)))

# Compute normalized posterior probabilities
posterior_values = np.exp(log_posterior_values - log_marginal)

posteriors = [(params_samples[i], posterior_values[i]) for i in range(monteCarloTrials)]

# Determine best-fit parameters
best_parameters = max(posteriors, key=lambda p: p[1])[0]

# Compute mean and variance at sampled x-values
xVals = np.linspace(domain[0], domain[1], resolution, dtype=np.float64)
means, variances = [], []
for x in xVals:
    t_mean = sum(func_lambda(*param, x) * prob for param, prob in posteriors)
    t_var = sum(((func_lambda(*param, x) - t_mean) ** 2) * prob for param, prob in posteriors)
    means.append(t_mean)
    variances.append(t_var)

# Convert results to numpy arrays
means = np.array(means, dtype=np.float64)
variances = np.array(variances, dtype=np.float64)

# Compute confidence interval bounds
z_score = norm.ppf((1 + confidenceIntervalCutoff) / 2)
y_upper = means + z_score * np.sqrt(variances)
y_lower = means - z_score * np.sqrt(variances)

# Print the best-fit parameters
print(best_parameters)
# Print performance measure (compare best fitting to mean)
best_fit_y = np.array([func_lambda(*best_parameters, x) for x in xVals], dtype=np.float64)
mse = np.linalg.norm(best_fit_y-means)/resolution
print(mse)

# Plot the results
plt.figure(figsize=(10, 6))

# Data points
plt.scatter(data[:, 0], data[:, 1], color='red', label='Data Points')


# Best fit line
plt.plot(xVals, best_fit_y, color='blue', label='Best Fit Line')

# Confidence interval
plt.fill_between(xVals, y_lower, y_upper, color='blue', alpha=0.2, label=f'{confidenceIntervalCutoff * 100}% Confidence Interval')

# Plot labels
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Bayesian Regression')
plt.legend()
plt.grid(True)
plt.show()
