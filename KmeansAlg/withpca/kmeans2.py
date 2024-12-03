import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
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

# Combine tensors into one
combined_data = torch.cat(padded_tensors, dim=0)

# Create tensor_indices to track origin of data (which tensor each data point came from)
tensor_indices = []
for idx, tensor in enumerate(tensor_list):
    tensor_indices.extend([idx] * tensor.shape[0])
tensor_indices = torch.tensor(tensor_indices)  # Convert to PyTorch tensor

# Apply PCA to reduce the combined data to 2D
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(combined_data.cpu().numpy())  # Ensure tensor is on CPU

# Perform clustering on PCA-reduced data
num_clusters = len(tensor_list)  # One cluster per tensor, adjust as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(reduced_data)

# Plot clusters based on tensor origin
plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=tensor_indices.numpy(), cmap='tab10', alpha=0.7)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='X', s=200, c='red', label='Centroids')
plt.title("PCA with K-means Clustering")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend()
plt.show()
