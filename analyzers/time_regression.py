import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures 

def PolyCoefficients(x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    o = len(coeffs)
    print(f'# This is a polynomial of order {o}.')
    y = 0
    for i in range(o):
        y += coeffs[i]*x**i
    return y

def analyze_data(resources_dir, results_dir, policy, threshold):
  """
  Analyzes data pairs from resources and results directories and performs linear regression.

  Args:
    resources_dir: Path to the directory containing data files.
    results_dir: Path to the directory for storing analysis results.
  """
  # Collect data pairs (size, time) from corresponding files
  data_pairs = []
  for filename in os.listdir(resources_dir):
    # Skip non-text files
    if not filename.endswith(".txt"):
      continue
    
    resource_file = os.path.join(resources_dir, filename)
    result_file = os.path.join(results_dir, f"{filename[:-4]}_time_{policy}_thr_{threshold}.txt")

    # Check if corresponding result file exists
    if not os.path.exists(result_file):
      print(f"Warning: Result file '{result_file}' not found for '{resource_file}'.")
      continue

    with open(resource_file, "r") as f_resource, open(result_file, "r") as f_result:
      try:
        size = float(f_resource.readline().strip())
        time = float(f_result.readline().strip())
        data_pairs.append((size, time))
      except ValueError:
        print(f"Error: Invalid data format in '{resource_file}' or '{result_file}'.")

  # Check if any data pairs were collected
  if not data_pairs:
    print("No valid data pairs found. Analysis aborted.")
    return

  # Separate data points into features (size) and target (time)
  X = [pair[0] for pair in data_pairs]
  y = [pair[1] for pair in data_pairs]

  # Create polynomial features transformer (degree=3 for (1, x, x^2, x^3))
  transformer = PolynomialFeatures(degree=3, include_bias=True)

  # Transform features using basis expansion
  X_transformed = transformer.fit_transform(np.expand_dims(X, axis=1))  # Reshape for compatibility


  # Create linear regression model
  model = LinearRegression()
  model.fit(X_transformed, y)  # Reshape X for compatibility

  # Print model coefficients (slope and intercept)
  print("Linear Regression Model Coefficients:")
  print(f"Coefficients: {model.coef_.flatten()}")  # Flatten for 1D array
  print(f"Coefficients: {model.coef_[0]}")  # Flatten for 1D array
  print(f"Coefficients: {model.coef_[1]}")  # Flatten for 1D array
  print(f"Coefficients: {model.coef_[2]}")  # Flatten for 1D array
  print(f"Coefficients: {model.coef_[3]}")  # Flatten for 1D array
  print(f"Intercept: {model.intercept_:.4f}")

  # Create the plot
  plt.figure(figsize=(8, 6))  # Adjust figure size as needed

  # Scatter plot with absolute differences on x-axis and labels with size
  plt.scatter(X, y, alpha=0.7)
  #Print the regression line
  line_X = np.linspace(0,2500)
  plt.plot(line_X, PolyCoefficients(line_X, [model.coef_[0], model.coef_[1], model.coef_[2], model.coef_[3]]))

  # Set labels and title
  plt.xlabel("Size")
  plt.ylabel("Time")
  plt.title(f"Execution Time Regression -  {policy}_thr_{threshold}")

  # Add legend
  plt.legend()

  # Enforce positive x-axis (optional, comment out if not desired)
  plt.xlim(xmin=0)

  # Display the plot
  plt.grid(True)
  plt.show()

# Set directory paths (replace with your actual paths)
resources_dir = "formatted_instances"
results_dir = "results"

analyze_data(resources_dir, results_dir, "min_min", "3")
analyze_data(resources_dir, results_dir, "max_min", "3")
analyze_data(resources_dir, results_dir, "avg_min", "3")
analyze_data(resources_dir, results_dir, "min_sav", "3")
analyze_data(resources_dir, results_dir, "max_sav", "3")
analyze_data(resources_dir, results_dir, "avg_sav", "3")

analyze_data(resources_dir, results_dir, "min_min", "10")
analyze_data(resources_dir, results_dir, "max_min", "10")
analyze_data(resources_dir, results_dir, "avg_min", "10")
analyze_data(resources_dir, results_dir, "min_sav", "10")
analyze_data(resources_dir, results_dir, "max_sav", "10")
analyze_data(resources_dir, results_dir, "avg_sav", "10")

analyze_data(resources_dir, results_dir, "min_min", "18")
analyze_data(resources_dir, results_dir, "max_min", "18")
analyze_data(resources_dir, results_dir, "avg_min", "18")
analyze_data(resources_dir, results_dir, "min_sav", "18")
analyze_data(resources_dir, results_dir, "max_sav", "18")
analyze_data(resources_dir, results_dir, "avg_sav", "18")