# feature-extractors

- **Description**: use this tool to extract features (i.e., different types of files) from the dataset.
- **Usage**:

```
# After you navigate to this directory in your Anaconda Prompt

# For extracting "assembly.json" from the dataset
# Results will be placed inside a new folder "assembly-jsons"
# "assembly.json" will be renamed to "[assembly ID].json"

python feature-extractor.py --feature assembly_json

# For extracting "assembly.jpg" from the dataset
# Results will be placed inside a new folder "assembly-thumbnails"
# "assembly.jpg" will be renamed to "[assembly ID].jpg"

python feature-extractor.py --feature assembly_thumbnail

# For extracting "[body ID].jpg" from the dataset
# Results will be placed inside a new folder "body-thumbnails"
# "[body ID].jpg" will be renamed to "[assembly ID]_sep_[body ID].jpg"

python feature-extractor.py --feature body_thumbnail

```