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

# Compute the mean for each tensor
tensor_means = torch.stack([tensor.mean(dim=0) for tensor in padded_tensors])

# Plot the means of the tensors
plt.figure(figsize=(10, 8))

# Assign each tensor a unique color
colors = plt.cm.tab10(range(len(tensor_list)))

for idx, mean in enumerate(tensor_means):
    mean_point = mean.numpy()
    plt.scatter(mean_point[0], mean_point[1], label=f"Tensor {idx}", color=colors[idx], s=100)

plt.title("Means of Tensors")
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.legend()
plt.show()
