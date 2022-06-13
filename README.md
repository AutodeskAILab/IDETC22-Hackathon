# IDETC-Hackathon 2022
## Introduction
Welcome to the IDETC Hackathon 2022!
Blah blah blah...


## Folder Structure

```
.
├─ sample-dataset              # A small sample of the Hackathon dataset
|  └─ ...
│ 
├─ utils                       # Utility code for generating the Hackathon dataset (you DON'T need to know or use this)
│  ├─ dataset-download.py      # Download the assembly dataset
│  ├─ dataset-filter.py        # Filter and remove OBJ and STEP files
│  └─ dataset-reduction.py     # Downsample the image files to reduce dataset size
│ 
├─ partial_algorithm           # Experiment No.2: Partial Algorithm-guided Prediction
├─ sample_data                 # A tiny subset of data sampled from the a03.10 Fusion 360 Assembly Gallery
└─ user_guided                 # Experiment No.3: User-guided Prediction
```

## Section 0: Obtaining the Dataset (important steps marked as ":exclamation:")
- **Description:** The dataset used in this Hackathon is generated from the [Fusion 360 Gallery Assembly Dataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/assembly.md), after processing steps that include feature removal and image downsampling to simplify the problem and to reduce the size of the dataset.
- :exclamation: **Download Link:** Please download the dataset from [here](), and unzip it. The dataset is roughly 3.5 GB in size.
- **Dataset Statistics:** 8251 assemblies + 154468 bodies.
- **Dataset Specifications:** Please refer to [the original documentation](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/assembly.md), and the README file in the `sample-dataset` directory.

## Section 1: Setting Up the Environment
- **Description:** Many of the tools and codes inside this directory requires Python environments that are specifically configured. In order to reconstruct the environment for compatibility, we recommend using [Anaconda](https://www.anaconda.com/) to manage your environment.
- :exclamation: **Installing Anaconda:** Please install Anaconda from the main site, as mentioned above. Follow the instructions from the main site.
