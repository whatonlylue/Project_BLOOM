import torch

class KMeansTorch:
    
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4, device=None):
        """
        Initialize the KMeans model.

        :param n_clusters: Number of n_clusters
        :param max_iter: Max number of iterations
        :param tol: Tolerance for convergance
        :param device: Device to use ('cuda', 'mps', or 'cpu')
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.device = device if device else ('mps' if torch.backends.mps.is_available() else 'cpu')
        self.centeroids = None

    def fit(self, X: torch.tensor) -> torch.tensor:
        """
        Fit the KMeans model to the data.

        :param X: Input data tensor (n_samples, n_features)
        :returns: Torch tensor of all lables
        """
        X = X.to(self.device)
        n_samples, n_features = X.shape

        indices = torch.randperm(n_samples)[:self.n_clusters]
        self.centeroids = X[indices]

        for i in range(self.max_iter):

            distances = torch.cdist(X, self.centeroids)

            labels = torch.argmin(distances, dim=1)

            new_centroids = torch.vstack([X[labels == j].mean(dim=0) for j in range(self.n_clusters)])

            centeroid_shift = torch.norm(self.centeroids - new_centroids, dim=1).sum()
            self.centeroids = new_centroids
            if centeroid_shift < self.tol:
                print(f"Converged in {i+1} iterations.")
                break
        
        return labels

    def predict(self, X: torch.tensor) -> torch.tensor:
        """
        Assign new data points to nearest cluster.

        :param X: Input data tensor (n_samples, n_features)
        :returns: torch tensor of all labels
        """
        X = X.to(self.device)
        distances = torch.cdist(X, self.centeroids)
        labels = torch.argmin(distances, dim=1)
        return labels



