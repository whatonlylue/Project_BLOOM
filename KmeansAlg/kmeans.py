import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# Load multiple tensors
tensor_data1 = torch.load('genome_embedding/GCA_000018385.1.fna_embedding.pt', map_location='cpu')
tensor_data2 = torch.load('genome_embedding/GCA_000754375.1.fna_embedding.pt', map_location='cpu')
tensor_data3 = torch.load('genome_embedding/GCA_001623545.2.fna_embedding.pt', map_location='cpu')
tensor_data4 = torch.load('genome_embeddingGCA_000006945.2_ASM694v2_genomic_tensor.pt', map_location='cpu')

# Check shapes
tensor_shapes = [tensor_data1.shape[1], tensor_data2.shape[1], tensor_data3.shape[1], tensor_data4.shape[1]]
max_dim = max(tensor_shapes)

# Pad tensors to match max dimension
def pad_tensor(tensor, target_dim):
    current_dim = tensor.shape[1]
    if current_dim < target_dim:
        padding = (0, target_dim - current_dim)  # (left_pad, right_pad)
        tensor = F.pad(tensor, padding, mode='constant', value=0)
    return tensor

tensor_data1 = pad_tensor(tensor_data1, max_dim)
tensor_data2 = pad_tensor(tensor_data2, max_dim)
tensor_data3 = pad_tensor(tensor_data3, max_dim)
tensor_data4 = pad_tensor(tensor_data4, max_dim)

# Combine tensors into one
combined_data = torch.cat((tensor_data1, tensor_data2, tensor_data3, tensor_data4), dim=0)

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
if len(combined_data.size()) == 2:
    plt.scatter(combined_data[:, 0], combined_data[:, 1], c=labels.numpy(), cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, color='red')
    plt.show()
