# dataset
## Description
- In this directory, we provide a few sample assemblies (which are a small subset from the full "IDETC-Hackathon-2022" dataset). 

- When in use, you should download the entire ["IDETC-Hackathon-2022"](https://myshare.autodesk.com/:u:/g/personal/shijie_bian_autodesk_com/EaNGU_hPjUJIig61f10SlTMBZ1aCvkiMoGlIxfcIAbIfHQ?e=VXlRb0) dataset, unzip it, and place the assembly folders inside this directory. Since the sample assemblies are selected from the dataset, please feel free to delete or overwrite them with the full dataset.

---
## Folder Structures
Each folder represents an assembly design made of multiple bodies, with the folder name being the assembly's unique hash ID.

Inside each folder there are the following content:
- **"assembly.json"**: The JSON file that contains all non-visual information of the assembly and its bodies.
- **"assembly.jpg"**: The thumbnail image of the assembly.
- **"[body-id].jpg"**: The thumbnail image of the body of the assembly. Note that each body has a unique hash ID, just like the assemblies.
