import os
import matplotlib.pyplot as plt

def process_file(source_file, source_dir, results_dir, solutions_file, policy, threshold):
  """
  Processes a single file from the formatted_instances directory.

  Args:
      source_file: The name of the file in the formatted_instances directory (e.g., a280.txt).
      results_dir: The directory containing result files (e.g., results).
      solutions_file: The path to the solutions.csv file.

  Returns:
      A tuple (orig_cost, found_cost, size), or None if errors occur.
  """

  size = 0
  complete_source_file = os.path.join(source_dir, source_file)
  with open(complete_source_file, 'r') as f:
    # Read lines from the file
    lines = f.readlines()
    # Extract cost and size
    size = int(lines[0].strip().split()[0])

  # Extract the instance name from the source file (remove extension)
  instance_name = os.path.splitext(source_file)[0]

  # Construct the corresponding result file path
  result_file = os.path.join(results_dir, f"{instance_name}_adjacencies_detailed_{policy}_thr_{threshold}.txt")

  # Try to open the result file for reading
  try:
    with open(result_file, 'r') as f:
      # Read lines from the file
      lines = f.readlines()

      found_cost = None
      for line in lines:
        if line.startswith("Cost : "):
          # Extract found cost (remove colons and underscores)
          found_cost = float(line.strip().split()[2].replace(",", ""))
          break
  except FileNotFoundError:
    #print(f"Result file not found: {result_file}")
    return None
  except IndexError:
    print(f"Unexpected format in result file: {result_file}")
    return None

  # Try to find the corresponding entry in solutions.csv
  try:
    with open(solutions_file, 'r') as f:
      for line in f.readlines():
        if line.startswith(f"{instance_name};"):
          # Extract original cost (remove semicolon and underscores)
          orig_cost = float(line.strip().split(";")[1])
          return orig_cost, found_cost, size
  except FileNotFoundError:
    print(f"Solutions file not found: {solutions_file}")
    return None

  # Entry not found in solutions.csv
  print(f"Entry not found for {instance_name} in solutions.csv")
  return None

def main(source_dir, results_dir, solutions_file, policy, thr):
  """
  Processes all files in the formatted_instances directory.

  Args:
      source_dir: The path to the formatted_instances directory.
      results_dir: The path to the results directory.
      solutions_file: The path to the solutions.csv file.
  """

  # Check if source directory exists
  if not os.path.exists(source_dir):
    print(f"Source directory not found: {source_dir}")
    return

  data_set = []

  # Iterate through files in the formatted_instances directory
  for filename in os.listdir(source_dir):
    if filename.endswith(".txt"):
      result = process_file(filename, source_dir, results_dir, solutions_file, policy, thr)
      if result:
        orig_cost, found_cost, size = result
        data_set.append((orig_cost, found_cost, size))
        print(f"Instance: {filename.strip('.txt')}")
        print(f"\tOriginal Cost: {orig_cost}")
        print(f"\tFound Cost: {found_cost}")
        print(f"\tSize: {size}")

  refined_dataset = []
  for data in data_set :
    orig_cost, found_cost, size = data
    refined_dataset.append((abs(orig_cost - found_cost) / orig_cost, size))

  scatter_X = [data[0] for data in refined_dataset]
  scatter_Y = [data[1] for data in refined_dataset]

  plt.figure(figsize=(8, 6)) 
  plt.scatter(scatter_X, scatter_Y, alpha=0.7)
  plt.xlabel("|orig_cost - found_cost| / orig_cost")
  plt.ylabel("Size")
  plt.title("Cost deviation scatter plot")
  plt.legend()
  plt.xlim(xmin=0)
  plt.grid(True)
  plt.show()

if __name__ == "__main__":
  source_dir = "formatted_instances"  # Modify as needed
  results_dir = "results"            # Modify as needed
  solutions_file = "extra/solutions.csv"   # Modify as needed
  main(source_dir, results_dir, solutions_file, "min_min", "3")