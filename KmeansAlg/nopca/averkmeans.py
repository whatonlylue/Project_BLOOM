import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans

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
tensor_shapes = [tensor.shape[1] for tensor in tensor_list]
max_dim = max(tensor_shapes)

# Pad tensors to match the maximum dimension
def pad_tensor(tensor, target_dim):
    current_dim = tensor.shape[1]
    if current_dim < target_dim:
        padding = (0, target_dim - current_dim)  # (left_pad, right_pad)
        tensor = F.pad(tensor, padding, mode='constant', value=0)
    return tensor

padded_tensors = [pad_tensor(tensor, max_dim) for tensor in tensor_list]

# Represent each tensor by its mean vector
tensor_representations = torch.stack([tensor.mean(dim=0) for tensor in padded_tensors])


# Perform clustering on tensor-level representations
num_clusters = 11  # Number of clusters = number of tensors (can adjust as needed)
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(tensor_representations)

# Plot tensor-level clusters
plt.scatter(tensor_representations[:, 0], tensor_representations[:, 1], c=cluster_labels, cmap='tab10', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='X', s=200, c='red', label='Centroids')
plt.title("Tensor-Level Clustering")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.legend()
plt.show()
