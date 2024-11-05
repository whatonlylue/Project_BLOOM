import torch
from kmean import KMeansTorch

class SpectralClustering:

    def __init__(self, n_clusters=2, similarity='rbf', gamma=1.0, device=None):
        """
        Initalizes the Spectral Clustering model.

        :param n_clusters: Number of clusters to form
        :param similarity: Type of similarity measure ('rbf' for Gaussain kernal, 'cosine' for cosine similarity)
        :param gamma: Kernal coefficient for RBF (Gaussain) similarity
        :param device: Device model will run on ('cuda', 'mps', or 'cpu')
        """
        self.n_clusters = n_clusters
        self.similarity = similarity
        self.gamma = gamma
        self.device = device if device else ('mps' if torch.backends.mps.is_available() else 'cpu')

    def compute_similarity_matrix(self, X: torch.tensor) -> torch.mm:
        """
        Computes similarity matrix based on selected similarity measure.

        :param X: Input data tensor (n_samples, n_features)
        :returns: Computed similarity matrix
        """
        if self.similarity == 'rbf':
            X_norm = (X ** 2).sum(dim=1).view(-1,1)
            dist = X_norm + X_norm.T - 2 * torch.mm(X, X.T)
            return torch.exp(-self.gamma * dist)
        
        elif self.similarity == 'cosine':
            X_normalized = X / torch.norm(X, dim=1, keepdim=True)
            return torch.mm(X_normalized, X_normalized.T)
        else:
            raise ValueError("Unsupported similartiy mesaure. Choose 'rbf' or 'cosine'.")

    def fit_predict(self, X: torch.tensor) -> torch.tensor:
        """
        Fit the spectral clustring model and predict cluster labels.

        :param X: Input data tensor (n_samples, n_features)
        :returns: Cluster labels for each point in the dataset
        """
        X = X.to(self.device)

        #Compute similarity matrix
        W = self.compute_similarity_matrix(X) 

        #Compute the normalized Laplacian
        D = torch.diag(W.sum(dim=1))
        L = D - W #Unnormalized Laplacian
        D_inv_sqrt = torch.diag(1.0 / torch.sqrt(D.diag()))
        L_norm = D_inv_sqrt @ L @ D_inv_sqrt
        
        L_norm_cpu = L_norm.to('cpu')
        # Compute eigenvalues and eigenvectors
        eigenvals, eignvecs = torch.linalg.eigh(L_norm_cpu)

        #Select the smallest `n_clusters` eigenvectors (ignore first value)
        eignvecs = eignvecs[:, 1:self.n_clusters+1].to(self.device)

        # Use Kmeans on eignvectors to cluster 
        kmeans = KMeansTorch(n_clusters=self.n_clusters, device=self.device)
        labels = kmeans.fit(eignvecs)

        return labels


