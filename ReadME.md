<p align="center">
  <img src="https://github.com/user-attachments/assets/38ccf23a-e86d-4198-a066-f6f2f83f1a16" height="350" width="900" />
</p>


# Project BLOOM

Welcome to Project BLOOM, which stands for: BLOOM: Behavioral Learning and Outcome Observation in Microbes. This project aims to fit a machine learning model to adapt to bacteria genomes to eventually predict there properties, with an end goal of dynamic vaccine creation.

### Requirments and Install
In order to use this package, you must have conda installed on your device, instructions to install conda can be found [here](https://docs.anaconda.com/anaconda/install/) 

Once you install conda, please run:
```shell
conda init
conda create -n ncbi_datasets
conda activate ncbi_datasets
conda install -c conda-forge ncbi-datasets-cli 
```
These instructions are from the ncbi_datasets module and can be found [here](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/)

#### Dependencies
- shelx
- time
- subprocess
- pytorch
- scikit-learn

Before you run any file from our Project, make sure you have activated the conda environment: conda activate

### Usecases
Intended functionality is as follows, enter an unknown bacteria genome, then get an output of predicted genotypes and phenotypes.

### Packages
Current packages:
- Data: All data collected for the model is stored here
- Data_collection_tools: All data collection tools are in this directory
### Next Steps
Looking to add AI functionality and expand our data set


