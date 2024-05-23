import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np 

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

def compress_couples(couples):
  """
  This function takes a list of couples (size, step) and compresses couples with equal size.

  Args:
      couples: A list of tuples representing couples (size, step).

  Returns:
      A list of compressed couples with the mean step for each size.
  """
  compressed_couples = {}
  for size, step in couples:
    if size not in compressed_couples:
      compressed_couples[size] = (size, step, 1)  # Initialize with step and count
    else:
      current_size, current_step, count = compressed_couples[size]
      # Update sum of steps and occurrence count
      compressed_couples[size] = (size, current_step + step, count + 1)
  # Calculate average step for each size
  for size, (size_value, total_step, count) in compressed_couples.items():
    average_step = total_step / count
    compressed_couples[size] = (size_value, average_step)
  return list(compressed_couples.values())


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
        steps = len(times)
        data_pairs.append((size, steps))
      except ValueError:
        print(f"Error: Invalid data format in '{resource_file}' or '{result_file}'.")

  # Check if any data pairs were collected
  if not data_pairs:
    print("No valid data pairs found. Analysis aborted.")
    return

  new_pairs = compress_couples(data_pairs)
  # Separate data points into features (size) and target (time)
  X = [pair[0] for pair in new_pairs]
  y1 = [pair[1] for pair in new_pairs]

  # Transform features using basis expansion
  log_X = np.log(np.array(X))
  if log_X.ndim == 1:
    log_X = log_X.reshape(-1, 1)  # Reshape to column vector if 1D

  ones_array = np.ones((log_X.shape[0], 1), dtype=log_X.dtype)
  X_transformed = np.c_[log_X, ones_array]

  # Create linear regression model
  model = LinearRegression()
  model.fit(X_transformed, y1)  # Reshape X for compatibility

  # Print model coefficients (slope and intercept)
  print("Linear Regression Model Coefficients:")
  print(f"Coefficients: {model.coef_[0]}")  # Flatten for 1D array
  print(f"Coefficients: {model.coef_[1]}")  # Flatten for 1D array
  print(f"Intercept: {model.intercept_:.4f}")

  # Create the plot
  plt.figure(figsize=(8, 6))  # Adjust figure size as needed

  # Scatter plot with absolute differences on x-axis and labels with size
  plt.scatter(X, y1, alpha=0.7)
  #Print the regression line
  line_X = np.linspace(1,2500)
  plt.plot(line_X, model.coef_[0]*np.log(line_X) + model.intercept_)

  # Set labels and title
  plt.xlabel("Size")
  plt.ylabel("Steps")
  plt.title("Steps-Size regression")

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