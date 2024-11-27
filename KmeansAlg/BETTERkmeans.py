import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import os

# Directory containing the .pt files
directory_path = "genome_embedding"

# List to store loaded tensors
tensor_list = []

# Loop through the directory to find and load .pt files
for filename in os.listdir(directory_path):
    if filename.endswith(".pt"):
        file_path = os.path.join(directory_path, filename)
        print(f"Loading file: {file_path}")
        tensor = torch.load(file_path, map_location='cpu')
        tensor_list.append(tensor)

# Ensure at least one tensor is loaded
if not tensor_list:
    raise ValueError("No .pt files found in the directory!")

# Check shapes of all tensors
tensor_shapes = []
for i in tensor_list:
    tensor_shapes.append(i.shape[1])
max_dim = max(tensor_shapes)

# Pad tensors to match the maximum dimension
def pad_tensor(tensor, target_dim):
    current_dim = tensor.shape[1]
    if current_dim < target_dim:
        padding = (0, target_dim - current_dim)  # (left_pad, right_pad)
        tensor = F.pad(tensor, padding, mode='constant', value=0)
    return tensor

padded_tensors = [pad_tensor(tensor, max_dim) for tensor in tensor_list]

# Combine tensors into one
combined_data = torch.cat(padded_tensors, dim=0)
print(combined_data.shape[1])

# Initialize centroids randomly from combined data
num_clusters = 2  # Adjust as needed
centroids = combined_data[torch.randperm(combined_data.size(0))[:num_clusters]]

# Define the number of iterations for K-means
num_iterations = 100

# Run K-means clustering
for _ in range(num_iterations):
    # Calculate distances from data points to centroids
    distances = torch.cdist(combined_data, centroids)

    # Assign each data point to the closest centroid
    _, labels = torch.min(distances, dim=1)

    # Update centroids by taking the mean of data points assigned to each centroid
    for i in range(num_clusters):
        if torch.sum(labels == i) > 0:
            centroids[i] = torch.mean(combined_data[labels == i], dim=0)

# Visualize if the data is 2D
plt.scatter(combined_data[:, 0], combined_data[:, 1], c=labels.numpy(), cmap='viridis')
plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, color='red')
plt.show()
