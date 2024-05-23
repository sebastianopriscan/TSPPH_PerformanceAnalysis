import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures 
def parse_file_data(filepath):
  """
  Parses data from a file with the new format.

  Args:
    filepath: Path to the file containing time data.

  Returns:
    A list of tuples, where each tuple represents time values
    for solving, derivation, and reconstruction at a single recursion step.
  """
  data = []
  with open(filepath, "r") as f:
    lines = f.readlines()
    # Loop through data sections separated by recursion steps
    for i in range(2, len(lines), 3):
      step_data = lines[i]  # Extract lines for time values
      # Split and convert time values to floats
      step_data = [float(step_data.split(";")[0].strip()), float(step_data.split(";")[1].strip()), float(step_data.split(";")[2].strip())]
      data.append(np.array(step_data))  # Create a tuple for each step's data
  return data

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
    result_file = os.path.join(results_dir, f"{filename[:-4]}_times_detailed_{policy}_thr_{threshold}.txt")

    # Check if corresponding result file exists
    if not os.path.exists(result_file):
      print(f"Warning: Result file '{result_file}' not found for '{resource_file}'.")
      continue

    with open(resource_file, "r") as f_resource:
      try:
        size = float(f_resource.readline().strip())
        times = parse_file_data(result_file)
        triple = np.array([0,0,0])
        for entry in times :
          triple = triple + entry
        data_pairs.append((size, triple))
      except ValueError:
        print(f"Error: Invalid data format in '{resource_file}' or '{result_file}'.")

  # Check if any data pairs were collected
  if not data_pairs:
    print("No valid data pairs found. Analysis aborted.")
    return

  # Separate data points into features (size) and target (time)
  X = [pair[0] for pair in data_pairs]
  y1 = [pair[1][0] for pair in data_pairs]
  y2 = [pair[1][1] for pair in data_pairs]
  y3 = [pair[1][2] for pair in data_pairs]

  # Create polynomial features transformer (degree=3 for (1, x, x^2, x^3))
  transformer = PolynomialFeatures(degree=3, include_bias=True)

  # Transform features using basis expansion
  X_transformed = transformer.fit_transform(np.expand_dims(X, axis=1))  # Reshape for compatibility


  # Create linear regression model
  model1 = LinearRegression()
  model1.fit(X_transformed, y1)  # Reshape X for compatibility

  model2 = LinearRegression()
  model2.fit(X_transformed, y2)  # Reshape X for compatibility

  model3 = LinearRegression()
  model3.fit(X_transformed, y3)  # Reshape X for compatibility

  # Print model coefficients (slope and intercept)
  #  print("Linear Regression Model Coefficients:")
  #  print(f"Coefficients: {model.coef_.flatten()}")  # Flatten for 1D array
  #  print(f"Coefficients: {model.coef_[0]}")  # Flatten for 1D array
  #  print(f"Coefficients: {model.coef_[1]}")  # Flatten for 1D array
  #  print(f"Coefficients: {model.coef_[2]}")  # Flatten for 1D array
  #  print(f"Coefficients: {model.coef_[3]}")  # Flatten for 1D array
  #  print(f"Intercept: {model.intercept_:.4f}")

  # Create the plot
  plt.figure(figsize=(15, 10))  # Adjust figure size as needed

  plt.subplot(131)
  # Scatter plot with absolute differences on x-axis and labels with size
  plt.scatter(X, y1, alpha=0.7)
  #Print the regression line
  line_X = np.linspace(0,2500)
  plt.plot(line_X, PolyCoefficients(line_X, [model1.coef_[0], model1.coef_[1], model1.coef_[2], model1.coef_[3]]))

  # Set labels and title
  plt.xlabel("Size")
  plt.ylabel("Time")
  plt.title(f"Solving Time Regression - {policy}_thr_{threshold}")

  # Add legend
  plt.legend()

  # Enforce positive x-axis (optional, comment out if not desired)
  plt.xlim(xmin=0)

  # Display the plot
  plt.grid(True)

  # Create the plot
  plt.subplot(132)
  # Scatter plot with absolute differences on x-axis and labels with size
  plt.scatter(X, y2, alpha=0.7)
  #Print the regression line
  line_X = np.linspace(0,2500)
  plt.plot(line_X, PolyCoefficients(line_X, [model2.coef_[0], model2.coef_[1], model2.coef_[2], model2.coef_[3]]))

  # Set labels and title
  plt.xlabel("Size")
  plt.ylabel("Time")
  plt.title(f"Derivation Time Regression - {policy}_thr_{threshold}")

  # Add legend
  plt.legend()

  # Enforce positive x-axis (optional, comment out if not desired)
  plt.xlim(xmin=0)

  # Display the plot
  plt.grid(True)

  # Create the plot
  plt.subplot(133)

  # Scatter plot with absolute differences on x-axis and labels with size
  plt.scatter(X, y3, alpha=0.7)
  #Print the regression line
  line_X = np.linspace(0,2500)
  plt.plot(line_X, PolyCoefficients(line_X, [model3.coef_[0], model3.coef_[1], model3.coef_[2], model3.coef_[3]]))

  # Set labels and title
  plt.xlabel("Size")
  plt.ylabel("Time")
  plt.title(f"Reconstruction Time Regression - {policy}_thr_{threshold}")

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