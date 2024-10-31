# Project BLOOM
#### **This is the Juypter Branch of BLOOM (ML Models are in notebooks instead of py scripts)**

Welcome to Project BLOOM, which stands for: BLOOM: Behavioral Learning and Outcome Observation in Microbes. This project aims to fit a machine learning model to adapt to bacteria genomes to eventually predict there properties, with an end goal of dynamic vaccine creation.

### Requirments and Install
Inorder to use this package, you must have conda install on your device, instructions to install conda can be found here: https://docs.anaconda.com/anaconda/install/ Once you install conda, run:

    1 conda init
    2 conda create -n ncbi_datasets
    3 conda activate ncbi_datasets
    4 conda install -c conda-forge ncbi-datasets-cli
    
These instructions can be found here https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/
#### Dependencies
- shelx
- time
- subprocess
- pytorch
- scikit-learn
- juypter notebooks

Before you run any file from our Project, make sure you have activated the conda environment: conda activate <your-environment>

### Usecases
Intended functionality is as follows, enter an unknown bacteria genome, then get an output of predicted genotypes and phenotypes.

### Packages
Current packages:
- Data: All data collected for the model is stored here
- Data_collection_tools: All data collection tools are in this directory
  
### Next Steps
Looking to add AI functionality and expand our data set
