# IDETC-Hackathon 2022
## Introduction and Logistics
Welcome to the IDETC Hackathon 2022!
[Copy some introductory content from the Google Docs]
Blah blah blah...

## Your Goal
...is to cluster the assemblies based on their similarity.

## Directory Structure

```
.
├─ sample-dataset              # A small sample of the Hackathon dataset (for demonstration purposes)
|  └─ ...
│ 
├─ utils                       # Utility code for generating the Hackathon dataset (you DON'T need to know or use this)
│  ├─ dataset-download.py      # Download the assembly dataset
│  ├─ dataset-filter.py        # Filter and remove OBJ and STEP files
│  └─ dataset-reduction.py     # Downsample the image files to reduce dataset size
│ 
├─ tools                       # Helper tools for your reference
|  ├─ feature-extractors       # [Tool 1]: extract specific files from the dataset
|  ├─ image-clustring          # [Tool 2]: unsupervised clustering of 2D thumbnail images
|  └─ image-similarity         # [Tool 3]: create fingerprints that expresses features extracted from 2D thumbnail images
│ 
└─ documents                    # Documentation for problem statement and final submission 
   ├─ Final Submission Template.pptx  # Use this to document your final results


```

## Logistics (important steps marked as :white_check_mark:)

### Section 0: Obtaining the Dataset 
- **Description:** The dataset used in this Hackathon is generated from the [Fusion 360 Gallery Assembly Dataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/assembly.md), after processing steps that include feature removal and image downsampling to simplify the problem and to reduce the size of the dataset.
- :white_check_mark: **Download Link:** Please download the dataset from [here](https://myshare.autodesk.com/:u:/g/personal/shijie_bian_autodesk_com/EaNGU_hPjUJIig61f10SlTMBZ1aCvkiMoGlIxfcIAbIfHQ?e=VXlRb0), and unzip it. The dataset is roughly 3.5 GB in size.
- **Dataset Statistics:** 8251 assemblies + 154468 bodies.
- **Dataset Specifications:** Please refer to [the original documentation](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/assembly.md), and the README file in the `sample-dataset` directory.

### Section 1: Setting Up the Environment
- **Description:** Many of the tools and codes inside this directory requires Python environments that are specifically configured. In order to reconstruct the environment for compatibility, we recommend using Anaconda to manage your environment.
- :white_check_mark: **Installing Anaconda:** Please install [Anaconda](https://www.anaconda.com/) from the official website, and follow the instructions on the website.
- :white_check_mark: **Reproducing the Environment**: We have provided a `.yml` file, and here's how to use it to reproduce the enironment:

```
# Make sure you have Anaconda installed
# If you are using Windows, open "Anaconda Prompt (Anaconda 3)" on your device

cd [path to this repository]                      # go to where you saved this repository on your local machine
conda env create --file=IDETC22-Hackathon.yml  # reproduce conda environment from .yml
conda activate IDETC22-Hackathon               # activate the created environment

# Now you should be able to use the tools and utilities in this repository through the Anaconda prompt
# Note that you would need to re-activate the environment each time you close and re-opens the Anaconda prompt
```

### Section 2: Using Helper Tool Functions
